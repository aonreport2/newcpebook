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
from django.core.paginator import Paginator,EmptyPage,InvalidPage


# Create your views here.
def hello (request):
    tags =['น้ำตก','ฝนตก','ตากหมอก']
    ratting = 3
    return render(request,'index.html',
                  {'name':'Thanapat Nantasiriyothin','tags':tags,'rat':ratting
                   }

                )

def page1(request):
    openserver = 1
    if openserver == 1:

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
    else:
        return render(request,'errorlayout1.html')

def page2(request):
    return render(request,'contract.html')
def page3(request):
    openserver = 1
    if openserver == 1:
        return render(request,'login1.html')
    else:
        return  render(request,'errorlayout1.html')

def adduser(request):
    return render(request,'confirm1.html')

@login_required (login_url='page1')
def adduser_admin(request):
    useradminor = request.user.is_superuser
    if useradminor == 1:


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
    else:
        return  redirect(page1)

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

        paginator = Paginator(oders, 50)

        try:
           page = int (request.GET.get('page','1'))
        except:
            page = 1
        try :
            productperPage = paginator.page(page)
        except(EmptyPage,InvalidPage) :
            productperPage = paginator.page(paginator.num_pages)



        contxt = {"oders":productperPage,"test":test}



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
        command = "น้องเคยขอลายเซ็นคนนี้ไปแล้วนะ"
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
            error_x= "เราจะกรอก ID ตัวเองไม่ได้น้าเว้ย เราจะปั้มยอดลายเซ็นหรอ  "
            return render(request,'error.html',{"error1":error_x})



@login_required (login_url='page1')
def confirmlicn(request):
    if request.user.is_authenticated:
        idcpe = str(request.user.id)
        oders = OderCommand.objects.filter(idcpeto=idcpe)
        test = UserProfile.objects.all()

        paginator = Paginator(oders, 50)

        try:
            page = int(request.GET.get('page', '1'))
        except:
            page = 1
        try:
            productperPage = paginator.page(page)
        except(EmptyPage, InvalidPage):
            productperPage = paginator.page(paginator.num_pages)

    return render(request,'confirmlic.html',{"oders":productperPage,"test":test})

def confirmsend(request,oder_id):
    if request.user.is_authenticated:
        oder = OderCommand.objects.filter(id=oder_id)
        oder.update(status=True)
    return redirect(confirmlicn)

def removeodercheck(request,oder_id):
    if request.user.is_authenticated:
        oder = oder_id
        requestsend = {'id':oder}
    return render(request,'removeoder.html',requestsend)

def removeoder(request,oder_id):
    if request.user.is_authenticated:
        oder = OderCommand.objects.filter(id=oder_id)
        oder.delete()
    return redirect('appsend')

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
    return  redirect(page1)

@login_required (login_url='page1')
def admincheckinput (request):
    useradminor = request.user.is_superuser
    if useradminor == 1:
        return render(request,'admincheckinput.html')
    else:
        return redirect(page1)


@login_required (login_url='page1')
def admincheck (request):
    useradminor = request.user.is_superuser
    if useradminor == 1:
        stdsend = request.POST['std']
        userprofilestd = UserProfile.objects.filter(std=stdsend)
        for i in userprofilestd:
            userid = i.user_id
            edu = i.edu
            nickname = i.nickname
            cpenumber = i.cpenumber
            count = i.count
        test = UserProfile.objects.all()
        oders = OderCommand.objects.filter(idcpesend=userid)

        odercout = 0
        for k in oders :
            if k.idcpesend == userid:
                odercout += 1

        contxt = {"oders": oders, "test": test,"nickname":nickname,"cpenumber":cpenumber,"userid":userid,"odercout":odercout}
        return render(request,'admincheck.html',contxt)
    else:
        return redirect(page1)

@login_required(login_url='page1')
def checklicense (request):
    if request.user.is_authenticated:
        edumy = request.user.userprofile.edu
        if edumy == "1":

            idcpe = int(request.user.id)
            oders = OderCommand.objects.filter(idcpesend=idcpe)
            countall = 0
            #เซ็นให้แล้ว
            edu1a =0
            edu2a =0
            edu3a =0
            edu4a =0
            #ยังไม่เซ็น
            edu1s =0
            edu2s =0
            edu3s =0
            edu4s =0






            for i in oders:
                test = UserProfile.objects.filter(user_id = i.idcpeto)
                if i.idcpesend == idcpe:
                    countall += 1
                for k in test :
                    if k.edu == "1":
                        if i.status == True:
                            edu1a += 1
                        else:
                            edu1s += 1
                    elif k.edu == "2":
                        if i.status == True:
                            edu2a += 1
                        else:
                            edu2s += 1
                    elif k.edu == "3":
                        if i.status == True:
                            edu3a += 1
                        else:
                            edu3s += 1
                    else :
                        if i.status == True:
                            edu4a += 1
                        else:
                            edu4s += 1


            #จำนวนลายเซ็นต์ทั้งหมด
            edu1 = edu1s+edu1a
            edu2 = edu2s+edu2a
            edu3 = edu3s+edu3a
            edu4 = edu4s+edu4a

            #จำนวนลายเซ็นต์ที่ยังขาด
            sumedu1 = 106-edu1a
            sumedu2 = 50 -edu2a
            sumedu3 = 30 -edu3a
            sumedu4 =  20- edu4

            if sumedu1 < 0:
                sumedu1 = 0
            if sumedu2 < 0 :
                sumedu2 = 0
            if sumedu3 < 0 :
                sumedu3 = 0
            if sumedu4 <= 0 :
                sumedu4 = 0


            contxt = {"countall":countall,"edu1":edu1,"edu2":edu2,"edu3":edu3,"edu4":edu4,"sumedu1":sumedu1,
                      "sumedu2":sumedu2,"sumedu3":sumedu3,"sumedu4":sumedu4,
                      "edu1a":edu1a,"edu2a":edu2a,"edu3a":edu3a,"edu4a":edu4a,
                      "edu1s":edu1s,"edu2s":edu2s,"edu3s":edu3s,"edu4s":edu4s}
            return render(request,'checklicense.html',contxt)
        else:
            return render(request,'errorlayout2.html')

@login_required(login_url='page1')
def adminchecklicense(request,userid):
    useradminor = request.user.is_superuser
    if useradminor == 1:
        idcpe = userid
        oders = OderCommand.objects.filter(idcpesend=idcpe)
        countall = 0
        #เซ็นให้แล้ว
        edu1a =0
        edu2a =0
        edu3a =0
        edu4a =0
        #ยังไม่เซ็น
        edu1s =0
        edu2s =0
        edu3s =0
        edu4s =0






        for i in oders:
            test = UserProfile.objects.filter(user_id = i.idcpeto)
            if i.idcpesend == idcpe:
                countall += 1
            for k in test :
                if k.edu == "1":
                    if i.status == True:
                        edu1a += 1
                    else:
                        edu1s += 1
                elif k.edu == "2":
                    if i.status == True:
                        edu2a += 1
                    else:
                        edu2s += 1
                elif k.edu == "3":
                    if i.status == True:
                        edu3a += 1
                    else:
                        edu3s += 1
                else :
                    if i.status == True:
                        edu4a += 1
                    else:
                        edu4s += 1


            #จำนวนลายเซ็นต์ทั้งหมด
        edu1 = edu1s+edu1a
        edu2 = edu2s+edu2a
        edu3 = edu3s+edu3a
        edu4 = edu4s+edu4a

            #จำนวนลายเซ็นต์ที่ยังขาด
        sumedu1 = 106-edu1a
        sumedu2 = 50 -edu2a
        sumedu3 = 30 -edu3a
        sumedu4 =  20- edu4

        if sumedu1 < 0:
            sumedu1 = 0
        if sumedu2 < 0 :
            sumedu2 = 0
        if sumedu3 < 0 :
            sumedu3 = 0
        if sumedu4 <= 0 :
            sumedu4 = 0


        contxt = {"countall":countall,"edu1":edu1,"edu2":edu2,"edu3":edu3,"edu4":edu4,"sumedu1":sumedu1,
                      "sumedu2":sumedu2,"sumedu3":sumedu3,"sumedu4":sumedu4,
                      "edu1a":edu1a,"edu2a":edu2a,"edu3a":edu3a,"edu4a":edu4a,
                      "edu1s":edu1s,"edu2s":edu2s,"edu3s":edu3s,"edu4s":edu4s}
        return render(request,'adminchecklicense.html',contxt)


        return render(request,adminchecklicense)

    else:
        return redirect(page1)




















