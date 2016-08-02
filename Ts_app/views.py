#coding:utf-8
from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from Ts_app.form import AddForm,AddUser,StreamForm,RentForm
from Ts_app.models import user_info,RentDB
from django.views.generic.edit import CreateView, FormView
from switch_stream_Worker import switch_stream_Worker
from datetime import datetime
 
def indexview(request):
    if request.method == 'POST':# ...... 

        form = AddForm()
        form_user = AddUser()
        form_stream = StreamForm()
        user_obj = user_info.objects.all()        
        if request.POST.has_key('switch_file'):
            form_stream = StreamForm(request.POST) #  form .......     
            if form_stream.is_valid():# .........
                host_name = form_stream.cleaned_data['host_name']
                stream_path = form_stream.cleaned_data['stream_path']
                connect_obj = switch_stream_Worker()
                result_num = connect_obj.run_switch_one(r"%s"%host_name,stream_path)
                return render(request, 'index.html', {'form_stream':form_stream,'form': form,'result_num':result_num,'form_user':form_user,'user_obj':user_obj})
        if request.POST.has_key('switch'):
            form = AddForm(request.POST) # form ....... 
            if form.is_valid():# .........
                host_name = form.cleaned_data['host_name']
                stream_path = form.cleaned_data['stream_path']
                modulation  = form.cleaned_data['modulation']
                frame_mode = form.cleaned_data['frame_mode']
                code_rate = form.cleaned_data['code_rate']
                band_width = form.cleaned_data['bandwidth']
                connect_obj = switch_stream_Worker()
                result_num = connect_obj.run_switch(r"%s"%host_name,stream_path,modulation,frame_mode,code_rate,band_width)
                return render(request, 'index.html', {'form_stream':form_stream,'form': form,'result_num':result_num,'form_user':form_user,'user_obj':user_obj})
        if request.POST.has_key('rent'):
            form_user = AddUser(request.POST)
            if form_user.is_valid():
                servername = form_user.cleaned_data['server_name']
                print servername
                #try �������ڵ�һ�����ݿ� AddUser����û�����ݵ�ʱ��form_user = AddUser(�������ᱨ��û���ҵ�����
                try:
                    form_user = AddUser(request.POST,instance=user_info.objects.get(server_name=servername))
                except:
                    pass
                form_user.save() 
                return render(request, 'index.html', {'form_stream':form_stream,'form': form,'form_user':form_user,'user_obj':user_obj})
        if request.POST.has_key('check_box_list'):
            print "fff"
            radio = request.POST.get('check_box_list')
            radio = int(radio)-1
            host_name = request.POST.get('host_name')
            print host_name
            modulation  = ['3','2','3','3','3','5','4']
            frame_mode = ['1','2','1','2','3','3','2']
            code_rate = ['1','3','2','3','3','2','3']
            carrier_mode = ['1','2','1','2','1','1','2']
            print host_name,modulation[radio],frame_mode[radio],code_rate[radio]
            connect_obj = switch_stream_Worker()
            result_num = connect_obj.run_switch_mode(r"%s"%host_name,modulation[radio],frame_mode[radio],code_rate[radio],carrier_mode[radio])
            return render(request, 'index.html', {'form_stream':form_stream,'form': form,'result_num':result_num,'form_user':form_user,'user_obj':user_obj})
    else:# ......
        form = AddForm()
        form_stream = StreamForm()
        form_user = AddUser()
        user_obj = user_info.objects.all()        
    return render(request, 'index.html', {'form_stream':form_stream,'form': form,'form_user':form_user,'user_obj':user_obj})

def rentview(request):
    rent_obj = RentDB.objects.all()
    if request.method == 'POST':
        print "b"
        form2 = RentForm()
        if request.POST.has_key('rent'):
            print "c"
            form2 = RentForm(request.POST or None,request.FILES)
            if form2.is_valid():
                device_id = form2.cleaned_data['d_id']
                #try �������ڵ�һ�����ݿ� AddUser����û�����ݵ�ʱ��form_user = AddUser(�������ᱨ��û���ҵ�����
                try:
                    form2 = RentForm(
                    request.POST,request.FILES,instance=RentDB.objects.get(d_id=device_id))
                except:
                    print '1'
                    pass
                print "d"
                form2.save()
                return render(request,'Ts_app/rent.html',{'form2':form2,'rent_obj':rent_obj})
            
    else:
        form2 = RentForm()
        print "e"
    print "aaa"
    return render(request,'Ts_app/rent.html',{'form2':form2,'rent_obj':rent_obj})

def ajaxview(request):
    a = range(30)   
    return JsonResponse(a,safe=False)

def ajaxdicview(request):
    name_dict = {'twz': 'Love python and Django', 'zqxt': datetime.now()}
    return JsonResponse(name_dict)