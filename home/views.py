from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from home.models import catgories
from django.contrib import messages
import json
import requests
import transformers
from transformers import pipeline
# Create your views here.
summarizer=pipeline("summarization")
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
    print("function call ke phele")    
    mlinfo(request)
    Mail(request)
    # if(sports!="on" and healthandmedicine!="on" and education!="on" and technology!="on" and  entertainment!="on" and tradeandprofessional !="on"):
        # return HttpResponse("ERROR")
    
    return redirect('home')    

def mlinfo(request):
    myuser=request.user
    userr=catgories.objects.filter(user=myuser).first() #not showing the latest setted category shows the category first selected by user
    if userr:
        if userr.sports==True:
            sportscon=requests.get('https://newsapi.org/v2/everything?q=sports&from=2023-01-04&sortBy=publishedAt&apiKey=d0d6a37ff82c44eaac677b2062890bcd').json()
            # sportstring=json.dumps(sportscon)
            print(sportscon)
            print("hello-------------------")
            print(type(sportscon))
            # print(sportstring[1])
            # print(sportstring[2])
            # print(sportstring[3])
            # print(sportstring[4])
            # print(sportstring[5])
            
            for i in range (0,len(sportscon["articles"])):
                print("number of article",len(sportscon["articles"]))
                print("for ke andar")
                conten_t=sportscon["articles"][i]["content"]
                print("content accessed") 
                print("length of content", len(conten_t))
                if (len(conten_t)>100):
                    print("if ke andar")
                    summarized=summarizer(conten_t,min_length=101,max_length=150)
                    print(summarized)        
                    break
            
            
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
    
    
    #this is mail function
   def Mail(request):
       import smtplib
       from email.mime.multipart import MIMEMultipart
       from email.mime.text import MIMEText
       from email.mime.base import MIMEBase
       from email import encoders
       fromaddr = "predict.io.2k22@gmail.com"
       toaddr = f"{email}"   

       msg = MIMEMultipart() 
       msg['From'] = fromaddr

       # storing the receivers email address 
       msg['To'] = toaddr

       # storing the subject 
       msg['Subject'] = "Your daily article summary :)"

       # string to store the body of the mail
       body = f"Hello {users.request}, Here is your daily sports article with its summary, Keep reading : ) {summary}"

       # attach the body with the msg instance
       msg.attach(MIMEText(body, 'plain'))

       # instance of MIMEBase and named as p
       p = MIMEBase('application', 'octet-stream')

       # To change the payload into encoded form
       p.set_payload((attachment).read())

       # encode into base64
       encoders.encode_base64(p)

       # creates SMTP session
       s = smtplib.SMTP('smtp.gmail.com', 587)

       # start TLS for security
       s.starttls()

       # Authentication
       s.login(fromaddr, "merwuzzcsxlpzjve")

       # Converts the Multipart msg into a string
       text = msg.as_string()

       # sending the mail
       s.sendmail(fromaddr, toaddr, text)

       # terminating the session
       s.quit()

           
