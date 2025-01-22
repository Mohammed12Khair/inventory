"""dms URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from home.views import *


urlpatterns = [
    path('admin/', admin.site.urls),
    #path('home/', index),
    path('logout/', logout_page,name="logout_page"  ),
    path('login/', login_page),
    path('', Home),
    path('add_user/', add_user),
    path('add_user/<str:username>', remove_user),
    path('import/', import_stock,name='import_page'),
    path('export/', export,name='export_page'),
    #path('nav/', test),
    path('request/', request_view,name="request_page"),
    path('request_user/', request_view_user,name="request_page_user"),
    path('import_req/', import_req,name="import_req"),
    path('stock_req/', stock_req,name="stock_req"),
    path('export_req/', export_req,name="export_req"),
    path('export_req_2/', export_req_2,name="export_req_2"),
    path('report_req/', report_page,name="report_page"),
]