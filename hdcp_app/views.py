from django.shortcuts import render
from hdcp_app.models import test_table
# Create your views here.
def test(request):
    test_obj = test_table.objects.all()
    return render(request,'hdcp_app/index.html',{'test_obj':test_obj})
    #return HttpResponse("hello world")

def login(request):
    pass