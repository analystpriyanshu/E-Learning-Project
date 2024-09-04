from django.shortcuts import render,HttpResponse,HttpResponseRedirect,redirect
from django.contrib.auth.models import User,auth
from app.models import Userdetails,category,video,Test,Testsoulution,Certificate,Payment,Usercourse
from django.contrib import messages
from time import time
from django.views.decorators.csrf import csrf_exempt
from websol.settings import *
import razorpay
client = razorpay.Client(auth=("rzp_test_TZMz05AomJrJ1", "WX3ZB4mIwsgmTVTp0UH004MS"))
#7

# from app.models import 
# Create your views here.
def indexpage(request):
    a=category.objects.all()
    print(a)
   

    return render(request,'index.html',{'a':a})
def indexpage2(request,slug):
    print(request.user)
    print(request.user.is_authenticated)
    if request.user.is_authenticated is True:


        cour=category.objects.get(slug=slug)
        print(slug)
        serial_number=request.GET.get('lecture')
        print(serial_number)
        if serial_number is None:
            serial_number=1
        vid=video.objects.get(serial_num=serial_number,select_course=cour)
        print(vid)
        return render(request,'videos.html',{'cour':cour,'vid':vid})
    return render(request,'form.html')

def indexpage3(request,slug):
    
    if not request.user.is_authenticated :
          return render(request,'form.html')
    cour=category.objects.get(slug=slug)    
    profile=Userdetails.objects.get(user=request.user) 
    action=request.GET.get('action') 
    order = None   
    payment = None
    error=None
    if action == 'create_payment':
        try:
            user_course=Usercourse.objects.get(user=profile,select_course=cour)
            error="you are already enrolled in this course"
        except:    
            pass
        if error is  None:
            amount= (cour.price - (cour.price * cour.offer * 0.01))*100
            currency = "INR"
            notes={
                "email" : profile.email,
                "name" : f'{profile.first_name} {profile.last_name}'
            }
            
            order = client.order.create(
                {
                    
            'notes' : notes,
            'amount' : amount,
            'currency' : currency
            }
            )
            payment=Payment()
            payment.user=profile
            payment.course=cour
            payment.order_id=order.get('id')
            payment.save()
            
            print(order)
    return render(request,'check.html',{'cour':cour,'order':order,'payment':payment,'error':error})

@csrf_exempt
def verify_payment(request):
     if request.method=="POST":
        data=request.POST 
        print(data)
        try:
            client.utility.verify_payment_signature(data)
            razorpay_order_id = data['razorpay_order_id']
            razorpay_payment_id = data['razorpay_payment_id']
            payment = Payment.objects.get(order_id=razorpay_order_id)
            payment.payment_id = razorpay_payment_id
            payment.status = True
            usercourse = Usercourse(user=payment.user , select_course=payment.course)
            usercourse.save()
            payment.user_course = usercourse
            payment.save()
            return redirect('mycourses')

        except:
           return HttpResponse("invalid payment details")   

def mycourses(request):
    if request.user.is_authenticated:
        user=request.user
        user_course=Usercourse.objects.filter(user=user)
        print(user_course)
        return render(request,'mycourses.html',{'user_course':user_course})


    return redirect('form')          
def about(request):
    return render(request,'index1.html')
def gallery(request):
    return render(request,'gallary.html')
def address(request):
    return render(request,'address.html')
def form(request):
    if request.method=="POST":
        uname=request.POST['username']
        passw=request.POST['password']
        print(uname,passw)
        user=auth.authenticate(username=uname,password=passw)
        print(user)
        if user is not None:
            print("yes")
            auth.login(request,user)
            if request.user.is_authenticated:
                print("yes ")
                return HttpResponseRedirect('/')
        else:
            
            print("no")
            # messages.info(request,"password or username is incorrect or createaccount first")
            return render(request,'form.html')
    return render(request,'form.html')
    
def signup(request):
    try:
        if request.method=="POST":
            n=request.POST['f_name']
            l=request.POST['l_name']
            e=request.POST['email']
            u=request.POST['username']
            p=request.POST['password']
            ph=request.POST['phone']
            print(n,u)
            if User.objects.filter(username=u).exists():
                print("hai bhai")
                messages.info(request,"Username already exist")
                
            else:
                print("nhi hai ")    
                user=Userdetails.objects.create_user(username=u,first_name=n,password=p,email=e,last_name=l,phone=ph)
                user.save()
        
        return render(request,'signup.html')
    except:
         return render(request,'signup.html')

def logout(request):
    auth.logout(request)
    return redirect('/')
def test(request):
    if Test.objects.filter(user=request.user):
        tes=Test.objects.all()
        
        return render(request,'test2.html',{'tes':tes})
    else:
        return HttpResponse('not foud')
def profile(request):
        
        profile=Userdetails.objects.get(user=request.user)
        return render(request,'profile.html',{'profile':profile})
        
def edit(request):
    if request.user.is_authenticated:
        profile = Userdetails.objects.get(user=request.user)
        if request.method=='POST':
            print(request.POST)
            f_name=request.POST['firstname']
            l_name=request.POST['lastname']
         
            email=request.POST['email']
            phone1=request.POST['phone']

            print(f_name)
            usra=Userdetails.objects.get(user=request.user)
            usra.first_name=f_name
            usra.last_name=l_name
            usra.phone=phone1
            usra.email=email
            
            usra.save()
            return HttpResponseRedirect('profile') 
        return render(request,'editprofile.html',{'profile':profile})
    return render(request,'login.html')
  
def certificate(request):
   
            if Certificate.objects.filter(user=request.user):
                certificate=Certificate.objects.all
                print(certificate)

                return render(request,'certificate.html',{'certificate':certificate})

            else:
                return HttpResponse('after course')

def uploadsolution(request):
    if Userdetails.objects.filter(user=request.user):
        u=Userdetails.objects.get(user=request.user)
        if request.method=="POST":
            f=request.POST['file']
            obj=Testsoulution(doc=f,user=u)
            obj.save()
    return render(request,'test.html')    