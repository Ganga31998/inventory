from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate

from django.views import View
from django.conf import settings

from .models import *
from .forms import *
# Create your views here.
def index(request):
    return render(request, "index.html")

class Home(View):
    def get(self,request):
        return render(request,"login.html")

def registerPage(request):
    form = createuserform()
    cust_form = createcustomerform()
    if request.method == 'POST':
        form = createuserform(request.POST)
        cust_form = createcustomerform(request.POST)
        if form.is_valid() and cust_form.is_valid():
            user = form.save()
            customer = cust_form.save(commit=False)
            customer.user = user
            customer.save()
            return redirect('login')
    context = {
        'form': form,
        'cust_form': cust_form,
    }
    return render(request, 'register.html', context)

def loginPage(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user_type = request.POST.get('user_type')
        user = authenticate(request, username=username, password=password, user_type = user_type)
        print(user)
        if user is not None:
            qs=User.objects.filter(is_staff=True,username=username)
            if qs:
                login(request,user)
                return redirect('Home')
            elif(username == 'vedha'):
                login(request, user)
                return redirect('Display')

            else:
                login(request, user)
                return redirect('Home')

    context = {}
    return render(request, 'Login.html', context)



class AdminpageView(View):
    def get(self, request):
        return render(request, 'admin.html')

class HomeView(View):
    def get(self,request):
        return render(request,'home.html')

class InsertInput(View):
    def get(self,request):
        return render(request,'productinput.html')
class InserView(View):
    def get(self,request):
        p_id=int(request.GET["t1"])
        p_name=request.GET["t2"]
        p_cost=float(request.GET["t3"])
        p_mfdt=request.GET["t4"]
        p_expdt=request.GET["t5"]
        p1=Product(pid=p_id,pname=p_name,pcost=p_cost,pmfdt=p_mfdt,pexpdt=p_expdt)
        p1.save()
        resp=HttpResponse("product inserted successfully")
        return resp

class DisplayView(View):
    def get(self,request):
        qs=Product.objects.all()
        con_dic={"records":qs}
        return render(request,"display.html",con_dic)

class DeleteInputView(View):

    def get(self,request):
        return render(request,"deleteinput.html")
class DeleteView(View):
    def get(self,request):
        P_id=int(request.GET["t1"])
        prod=Product.objects.filter(pid=P_id)
        prod.delete()
        resp = HttpResponse("product deleted successfully")
        return resp
class UpdateInputView(View):
    def get(self,request):
        return render(request,"updateinput.html")
class UpdateView(View):
    def post(self,request):
        P_id=int(request.POST["t1"])
        p_name = request.POST["t2"]
        p_cost = float(request.POST["t3"])
        p_mfdt = request.POST["t4"]
        p_expdt = request.POST["t5"]
        prod=Product.objects.get(pid=P_id)
        prod.pname=p_name
        prod.pcost=p_cost
        prod.pmfdt=p_mfdt
        prod.pexpdt=p_expdt
        prod.save()
        resp = HttpResponse("product updated successfully")
        return resp

def logoutPage(request):
    logout(request)
    return redirect('/')

