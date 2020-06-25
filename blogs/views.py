from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from blogs.models import OderCommand, UserProfile
from blogs.form import signUpForm
from django.contrib.auth.models import Group,User
from django.contrib.auth.forms import AuthenticationForm
from  django.contrib.auth import login,authenticate,logout
from django.contrib.auth.decorators import login_required
from .form import UserProfileForm
from django.contrib.auth.hashers import make_password

# Create your views here.
def hello (request):
    tags =['น้ำตก','ฝนตก','ตากหมอก']
    ratting = 3
    return render(request,'index.html',
                  {'name':'Thanapat Nantasiriyothin','tags':tags,'rat':ratting
                   }

                )

def page1(request):

    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username = username, password = password)
            if user is not None:
                login(request,user)
                return redirect('appsend')
            else:
                return redirect('index')


    else:
        form =AuthenticationForm()

    return render(request,'page1.html',{'form':form})

def page2(request):
    return render(request,'contract.html')
def page3(request):
    return render(request,'login1.html')

def adduser(request):
    return render(request,'confirm1.html')

def adduser_admin(request):

    if request.method =='POST':
        form = signUpForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        if form.is_valid() and profile_form.is_valid():
            # บันทึกข้อมูล
            user = form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()




            # บันทึก GROUP
            # ดึง username มาใช้
            username = form.cleaned_data.get('username')
            #คิวรี่
            signUpUser =User.objects.get(username=username)
            user_group = Group.objects.get(name = "user")

            user_group.user_set.add(signUpUser)

            #--------

    else:
        form = signUpForm()
        profile_form = UserProfileForm()
    context = {'form':form ,'profile_form':profile_form}
    return render(request,'adduser.html',context)

def resualt (request):
    username = request.POST['user2']
    std = request.POST['std']
    firstname = request.POST['firstname']
    lastname = request.POST['lastname']
    edu = request.POST['edu']
    user = User.objects.create_user(
        username = username,
        password= "0000",
        #std = std ,
        first_name = firstname,
        last_name = lastname,
        #edu = edu

    )
    user.save()
    return render(request,'resualt.html')



@login_required (login_url='page1')
def appsend(request):
    if request.user.is_authenticated:
        idcpe = str(request.user.id)
        test = UserProfile.objects.all()
        oders = OderCommand.objects.filter(idcpesend=idcpe)
        contxt = {"oders":oders,"test":test}

    return render(request,'appsend.html',contxt)

def _card_id(request):
    card = request.session.session_key
    if not card :
        card = request.session.create()

    return  card
def signOutView(request):
    logout(request)
    return  redirect('index')

@login_required (login_url='page1')
def license (request):
    edumy =request.user.userprofile.edu
    if edumy == "1":
        return render(request, 'license.html')
    else:
        x = "เราปีสูงแล้ว จะไปขอลายเซ็นต์น้องไม่ได้น้าา"
        return render(request,'error.html',{"error1":x})

def final (request):
    if request.user.is_authenticated:
        idsend =request.POST['iduser']
        idmy = request.user.id
        name = User.objects.all()
        idrequestsendmy = OderCommand.objects.filter(idcpesend = idmy)
        idsend = int(idsend)
        boolen = False
        # บันทึกข้อมูล
        command = "แกเคยขอลายเซ็นต์คนนี้ไปแล้วอ่ะ T_T"
        if idsend != request.user.id:
            if boolen == False:
                for i in OderCommand.objects.filter(idcpesend = idmy):
                    if i.idcpeto == idsend:
                        return render(request, 'error.html', {'x': command})
                    else:
                        boolen =True
                else:
                    oder = OderCommand.objects.create \
                            (
                            idcpesend=request.user.id,
                            idcpeto=idsend,
                            status=False
                        )
                    oder.save()
                    return render(request, 'final.html', {'name': name, 'id': idsend,'idrequestsendmy':idrequestsendmy})



        else:
            error_x= "เราจะกรอก ID ตัวเองไม่ได้น้าเว้ย เราจะปั้มยอดลายเซ็นต์หรอ เสียใจนะ "
            return render(request,'error.html',{"error1":error_x})



@login_required (login_url='page1')
def confirmlicn(request):
    if request.user.is_authenticated:
        idcpe = str(request.user.id)
        oders = OderCommand.objects.filter(idcpeto=idcpe)
        test = UserProfile.objects.all()

    return render(request,'confirmlic.html',{"oders":oders,"test":test})

def confirmsend(request,oder_id):
    if request.user.is_authenticated:
        oder = OderCommand.objects.filter(id=oder_id)
        oder.update(status=True)
    return redirect(appsend)

def error(request):
    return render(request,'error.html')

def findstd(request):
    stdsend =request.POST['std']
    userprofilestd = UserProfile.objects.filter(std = stdsend )
    for i in userprofilestd:
        userid = i.user_id
        edu = i.edu
        nickname = i.nickname
        cpenumber = i.cpenumber
        count = i.count
    object_user = User.objects.filter(id = userid)
    for k in object_user:
        username = k.username

    if count == "0":
        userprofilestd.update(count=1)
        requestsend = {"userid":userid,"edu":edu,"nickname":nickname,"username":username,"cpenumber":cpenumber}
        return render(request,'login1_2.html',requestsend)
    else:
        return render(request, 'errori.html')


def setpassword (request):
    password =request.POST['password']
    iduser = request.POST['userid']
    hashed_pass = make_password(password)
    oder = User.objects.filter(id = iduser)
    oder.update(password = hashed_pass)
    return  redirect('page1')










