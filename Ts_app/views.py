# coding:utf-8
from django.shortcuts import render
from django.http import JsonResponse
from Ts_app.form import AddForm, AddUser, StreamForm, RentForm, TestlinkForm
from Ts_app.models import user_info, RentDB, TestlinkDB, TestlinkCase
# from django.views.generic.edit import CreateView, FormView
from Ts_app.switch_stream_Worker import switch_stream_Worker
from datetime import datetime
from Ts_app.XML_CSV import XML_CSV


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
        # 注释掉了，暂时不用
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
 

def testlinkview(request):
    test_case_list = TestlinkCase.objects.all()
    if request.method == 'POST':
        form_obj = TestlinkForm(request.POST, request.FILES)
        if form_obj.is_valid():
            file_name = form_obj.cleaned_data['filepath']
            print file_name
            # 返回一个文件对象
            file_obj = request.FILES['filepath']
            print file_obj
            #print file_obj.read()
            print hasattr(file_obj, "read")
            xml_obj = XML_CSV()
            test_case = xml_obj.read_xml(file_obj)
            print test_case
            #suite_root = test_case[0][0]
            #TestlinkDB.objects.create(parent_suite_name="root", suite_name=suite_root[1], suite_detail=suite_root[2])
            for suite in test_case[0]:
                #suite_ins = TestlinkDB.objects.get(suite_name=suite[0])
                TestlinkDB.objects.get_or_create(parent_suite_name=suite[0], suite_name=suite[1], suite_detail=suite[2])
            for case in test_case[1]:
                suite_ins = TestlinkDB.objects.get(suite_name=case[0])
                #result = TestlinkCase.objects.get_or_create(case_name=case[1], case_sum=case[2], case_step=case[3], case_except=case[4], case_suite=suite_ins)
                #if result[1] == False:
                if TestlinkCase.objects.filter(internalid=case[5]):
                    print case[1]
                    print "get !!!!!!!!!!"
                    TestlinkCase.objects.filter(internalid=case[5]).update(case_name=case[1], case_sum=case[2], case_step=case[3], case_except=case[4], internalid=case[5], case_suite=suite_ins)
                else:
                    print case[1]
                    print case[4]
                    print "not find!!!!!"
                    TestlinkCase.objects.create(case_name=case[1],case_sum=case[2], case_step=case[3], case_except=case[4], internalid=case[5], case_suite=suite_ins)
                        
            return render(request, 'Ts_app/testlink.html',
                          {'form_obj': form_obj, 'file_name': file_name, 'test_case_list':test_case_list})

    else:
        form_obj = TestlinkForm()
    
    return render(request, 'Ts_app/testlink.html', {'form_obj': form_obj, 'test_case_list':test_case_list})
