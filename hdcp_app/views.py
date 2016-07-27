from django.shortcuts import render
from django.http import HttpResponse
from .models import test_table
# Create your views here.
def test(request):
    test_obj = test_table.objects.all()
    return render(request,'index.html',{'test_obj':test_obj})
    #return HttpResponse("hello world")
    