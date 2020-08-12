"""cpe URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from blogs import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.hello,name="index"),
    path('page1',views.page1,name = "page1"),
    path('page2',views.page2),
    path('page3',views.page3),
    path('adduseradmin',views.adduser_admin),
    path('resualt',views.resualt),
    # path('appsend',views.appsend,name="appsend"),
    path('appsend',views.checklicense,name="appsend"),
    path('account/logout',views.signOutView,name="signout"),
    path('license',views.checklicense,name="license"),
    # path('license',views.license,name="license"),
    path('final',views.final,name="final"),

    path('confirmlic',views.checklicense,name = "confirmlic"),
    # path('confirmlic',views.confirmlicn,name = "confirmlic"),

    path('confirmsend/<int:oder_id>',views.confirmsend,name="confirmsend"),

    path('error',views.error,name="error"),
    path('findstd',views.findstd,name="findstd"),
    path('setpassword',views.setpassword),
    path('admincheckinput',views.admincheckinput),
    path('admincheck',views.admincheck),
    path('checklicense',views.checklicense),
    path('adminchecklicense/<int:userid>',views.adminchecklicense,name="adminchecklicense"),
    path('removeodercheck/<str:oder_id>',views.removeodercheck,name="removeodercheck"),
    path('removeoder/<int:oder_id>',views.removeoder,name="removeoder"),
    #path('order/<int:oder_id',views.viewOrder,name="oder")

]
