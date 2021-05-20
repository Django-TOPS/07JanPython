from django.shortcuts import render,redirect
from .forms import signupForm,notesForm
from .models import signup,notes
from django.contrib.auth import logout
from django.core.mail import send_mail
from BatchProject import settings
import random
import requests
import json

# Create your views here.

def index(request):
    if request.method=='POST':
        if request.POST.get('signup')=='signup':
            signupfrm=signupForm(request.POST)
            if signupfrm.is_valid():
                signupfrm.save()
                print("Signup Sucessfully!")

                otp=random.randint(11111,99999)
                #Send Mail
                subject="Account Confirmation!Enjoy"
                msg=f"Hello User, \nYour account has been created successfully! \nPlease use {otp} varifaction code for account activation."
                #from_email='djangomail2021@gmail.com'
                from_email=settings.EMAIL_HOST_USER
                to_email=['sonagarapraful2510@gmail.com','brijesh.br1808@gmail.com']
                #to_email=[request.POST["username"]]

                send_mail(subject,msg,from_email,to_email)
                return redirect('notes')
            else:
                print(signupfrm.errors)
        elif request.POST.get("login")=='login':
            email=request.POST['username']
            password=request.POST['password']
            uid=signup.objects.get(username=email)

            userdata=signup.objects.filter(username=email,password=password)
            if userdata:
                print("Login Successfully!")

                #SMS Sending
                # mention url
                url = "https://www.fast2sms.com/dev/bulk"

                otp=random.randint(11111,99999)
                
                # create a dictionary
                my_data = {
                    # Your default Sender ID
                    'sender_id': 'FSTSMS', 
                    
                    # Put your message here!
                    'message': f'Hello, \nYou have successfully login! \nYour one time password is {otp}', 
                    
                    'language': 'english',
                    'route': 'p',
                    
                    # You can send sms to multiple numbers
                    # separated by comma.
                    'numbers': '7046717098,9106002965'    
                }
                headers = {
                    'authorization': '0PObtHc6ZSVgMqnsLGpUQlyrWmjaxd5AXK27vDwCEi3FeTzY1o5RnmEPAlK6NFVZHWYXegBGpuLdv1Cz',
                    'Content-Type': "application/x-www-form-urlencoded",
                    'Cache-Control': "no-cache"
                }
                # make a post request
                response = requests.request("POST",
                                            url,
                                            data = my_data,
                                            headers = headers)
                returned_msg = json.loads(response.text)
                
                # print the send message
                print(returned_msg['message'])

                request.session['user']=email
                request.session['uid']=uid.id
                return redirect('notes')
            else:
                print("Error...Username or Password is invalid!")
    else:
        signupfrm=signupForm()
    return render(request,'index.html')

def notes(request):
    user=request.session.get('user')
    if request.method=='POST':
        notefrm=notesForm(request.POST, request.FILES)
        if notefrm.is_valid():
            notefrm.save()
            print("Your notes has been uploaded!")
        else:
            print(notefrm.errors)
    else:
        notefrm=notesForm()
    return render(request,'notes.html',{'user':user})

def updateprofile(request):
    user=request.session.get('user')
    userid=request.session.get('uid')
    if request.method=='POST':
        signupfrm=signupForm(request.POST)
        id=signup.objects.get(id=userid)
        if signupfrm.is_valid():
            signupfrm=signupForm(request.POST, instance=id)
            signupfrm.save()
            print("Your profile has been updated!")
            return redirect('notes')
        else:
            print(signupfrm.errors)
    else:
        signupfrm=signupForm()
    return render(request,'updateprofile.html',{'user':user,'userdata':signup.objects.get(id=userid)})

def userlogout(request):
    logout(request)
    return redirect('/')

