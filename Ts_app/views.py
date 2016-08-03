# coding:utf-8
from django.shortcuts import render
from django.http import JsonResponse
from Ts_app.form import AddForm, AddUser, StreamForm, RentForm
from Ts_app.models import user_info, RentDB
# from django.views.generic.edit import CreateView, FormView
from switch_stream_Worker import switch_stream_Worker
from datetime import datetime


# Ts_app页面的逻辑函数
def indexview(request):
    if request.method == 'POST':  # 注释
        form = AddForm()
        form_user = AddUser()
        form_stream = StreamForm()
        user_obj = user_info.objects.all()
        if 'switch_file' in request.POST:
            form_stream = StreamForm(request.POST)
            if form_stream.is_valid():
                host_name = form_stream.cleaned_data['host_name']
                stream_path = form_stream.cleaned_data['stream_path']
                connect_obj = switch_stream_Worker()
                result_num = connect_obj.run_switch_one(
                    r"%s" % host_name, stream_path)
                return render(request, 'Ts_app/index.html', {
                    'form_stream': form_stream, 'form': form,
                    'result_num': result_num, 'form_user': form_user,
                    'user_obj': user_obj})
        if 'switch' in request.POST:
            form = AddForm(request.POST)
            if form.is_valid():
                host_name = form.cleaned_data['host_name']
                stream_path = form.cleaned_data['stream_path']
                modulation = form.cleaned_data['modulation']
                frame_mode = form.cleaned_data['frame_mode']
                code_rate = form.cleaned_data['code_rate']
                band_width = form.cleaned_data['bandwidth']
                connect_obj = switch_stream_Worker()
                result_num = connect_obj.run_switch(
                    r"%s" % host_name, stream_path, modulation,
                    frame_mode, code_rate, band_width)
                return render(request, 'Ts_app/index.html', {
                    'form_stream': form_stream, 'form': form,
                    'result_num': result_num, 'form_user': form_user,
                    'user_obj': user_obj})
        if 'rent' in request.POST:
            form_user = AddUser(request.POST)
            if form_user.is_valid():
                servername = form_user.cleaned_data['server_name']
                print servername
                try:
                    form_user = AddUser(
                        request.POST, instance=user_info.objects.get(
                            server_name=servername))
                except:
                    pass
                form_user.save()
                return render(request, 'Ts_app/index.html', {
                    'form_stream': form_stream, 'form': form,
                    'form_user': form_user, 'user_obj': user_obj})

        if 'check_box_list_bak' in request.POST:
            print "fff"
            radio = request.POST.get('check_box_list')
            radio = int(radio)-1
            host_name = request.POST.get('host_name')
            print host_name
            modulation = ['3', '2', '3', '3', '3', '5', '4']
            frame_mode = ['1', '2', '1', '2', '3', '3', '2']
            code_rate = ['1', '3', '2', '3', '3', '2', '3']
            carrier_mode = ['1', '2', '1', '2', '1', '1', '2']
            print host_name, modulation[radio],\
                frame_mode[radio], code_rate[radio]
            connect_obj = switch_stream_Worker()
            result_num = connect_obj.run_switch_mode(
                r"%s" % host_name, modulation[radio],
                frame_mode[radio], code_rate[radio], carrier_mode[radio])
            return render(request, 'Ts_app/index.html', {
                'form_stream': form_stream, 'form': form,
                'result_num': result_num, 'form_user': form_user,
                'user_obj': user_obj})
    else:
        form = AddForm()
        form_stream = StreamForm()
        form_user = AddUser()
        user_obj = user_info.objects.all()
    return render(request, 'Ts_app/index.html', {
        'form_stream': form_stream, 'form': form,
        'form_user': form_user, 'user_obj': user_obj})


# equipment页面的逻辑函数
def rentview(request):
    rent_obj = RentDB.objects.all()
    if request.method == 'POST':
        print "b"
        form2 = RentForm()
        if 'rent' in request.POST:
            print "c"
            form2 = RentForm(request.POST or None, request.FILES)
            if form2.is_valid():
                device_id = form2.cleaned_data['d_id']
                try:
                    form2 = RentForm(
                        request.POST, request.FILES,
                        instance=RentDB.objects.get(d_id=device_id))
                except:
                    pass
                form2.save()
                return render(request, 'Ts_app/rent.html', {
                    'form2': form2, 'rent_obj': rent_obj})

    else:
        form2 = RentForm()

    return render(request, 'Ts_app/rent.html', {
        'form2': form2, 'rent_obj': rent_obj})


# 用ajax请求动态内容的逻辑函数
def ajaxview(request):
    a = range(30)
    return JsonResponse(a, safe=False)


def ajaxdicview(request):
    name_dict = {'twz': 'Love python and Django', 'zqxt': datetime.now()}
    return JsonResponse(name_dict)


def radioview(request):
        # print request.GET['radio_id']
        if request.method == 'GET':
            radio = int(request.GET['radio_id'])-1
            host_name = request.GET['host_id']
            modulation = ['3', '2', '3', '3', '3', '5', '4']
            frame_mode = ['1', '2', '1', '2', '3', '3', '2']
            code_rate = ['1', '3', '2', '3', '3', '2', '3']
            carrier_mode = ['1', '2', '1', '2', '1', '1', '2']
            connect_obj = switch_stream_Worker()
            result_num = connect_obj.run_switch_mode(
                r"%s" % host_name, modulation[radio],
                frame_mode[radio], code_rate[radio], carrier_mode[radio])
            print 1
            return JsonResponse(result_num, safe=False)
        else:
            print "no find check box in request"
            print request.method
