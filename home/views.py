from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from home.models import catgories
from django.contrib import messages
import json
import requests
# Create your views here.
def home(request):
    return render(request,'home/home.html')


def cat(request):
    return render(request,'home/Categories.html')

def log(request):
    return render(request,'home/login2.html')

def loginn(request):
     if request.method=='POST':
        username=request.POST['name']
        email=request.POST['email']
        pass1=request.POST['password']
        pass2=request.POST['cnfpassword']
        
        #check for user details.
        if User.objects.filter(username=username).first():
            messages.error(request,"Username already exists !!")
            return redirect('home')
        
        if User.objects.filter(email=email).first():
            messages.error(request,"Email already registered  !!")
            return redirect('home')
        
        if len(username)>10:
            messages.error(request,"username must be less than 10 char")
            return redirect('home')
        
        if not username.isalnum() :
            messages.error(request,"username sholud contain letters and numbers only")
            return redirect('home')
        
        if pass1 !=pass2:
            messages.error(request,"password donot match")
            return redirect('home')
        
        myuser=User.objects.create_user(username,email,pass1)
        myuser.save()
        messages.success(request,"You have sucessfully login")
        #return redirect('choose') this will call choose and choose will redirect it to home as choose is returing home 
        return render(request,'home/login2.html') 
    
     else:
        return HttpResponse("404-NOT FOUND")
    
def mainlogin(request) :
    if request.method=='POST':
        loginame=request.POST['emaill']
        loginpass=request.POST['passwordd']
        user=authenticate(username=loginame,password=loginpass)
        if user is not None:
            login(request,user)
            messages.success(request,"sucefully login")
            return render(request,'home/Categories.html')  
        
        else:
            messages.error(request,"invalid crenditals")
            return render(request,'home/login2.html')
    else:
        return HttpResponse("404-ERROR")    

def logoutt(request):
    logout(request)
    messages.success(request,"sucessfully logout")
    return redirect('home')

def choose(request):
    user=request.user
    sports=request.POST.get('Sports','off')
    healthandmedicine=request.POST.get('Health','off')
    education=request.POST.get('Education','off')
    technology=request.POST.get('Technology','off')
    entertainment=request.POST.get('Entertainment','off')
    tradeandprofessional=request.POST.get('Trade','off')
    
    obj=catgories.objects.create(user=user)
    
    if sports=="on":
        obj.sports=True
        obj.save()
        
    if healthandmedicine=="on":
        obj.healthandmedicine=True
        obj.save()    
        
    if education=="on":
        obj.education=True
        obj.save()
        
    if technology=="on":
        obj.technology=True
        obj.save()
        
    if entertainment=="on":
        obj.entertainment=True
        obj.save() 
          
    if tradeandprofessional=="on":
        obj.tradeandprofessional=True
        obj.save()
    
    obj.save()    
    mlinfo(request)
    # if(sports!="on" and healthandmedicine!="on" and education!="on" and technology!="on" and  entertainment!="on" and tradeandprofessional !="on"):
        # return HttpResponse("ERROR")
    
    return redirect('home')    

def mlinfo(request):
    myuser=request.user
    userr=catgories.objects.filter(user=myuser).first() #not showing the latest setted category shows the category first selected by user
    if userr:
        if userr.sports==True:
            sportscon=requests.get('https://newsapi.org/v2/everything?q=sports&from=2023-01-04&sortBy=publishedAt&apiKey=d0d6a37ff82c44eaac677b2062890bcd').json()
            sportstring=json.dumps(sportscon)
            print(sportstring)
            
            
        if userr.healthandmedicine==True:
            healthcon=requests.get('https://newsapi.org/health').json()
        
        
        if userr.education==True:
            educon=requests.get('https://newsapi.org/education').json()    
        
        if userr.technology==True:
            techcon=requests.get('https://newsapi.org/technology').json()
        
        if userr.entertainment==True:
            entertainmentcon=requests.get('https://newsapi.org/entertainment').json()   
            
        if userr.tradeandprofessional==True:
            tradecon=requests.get('https://newsapi.org/trade').json()     
    
    else:
        return HttpResponse("Please select categories")        
    
    