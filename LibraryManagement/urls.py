"""LibraryManagement URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from books_management import views
from books_management.tools import fileUpload

urlpatterns = [
    path('admin/', admin.site.urls),
    path('bookInfo',views.books_info),
    path('userInfo',views.user_info),
    path('adminInfo',views.admin_info),
    path('classifyInfo',views.classify_info),
    path('vercode', views.vercode),
    path('fileInfo',fileUpload.upLoad),
    path('login',views.admin_login),
    path('finance_info',views.financeInfos),
]

from django.conf import settings
from django.conf.urls.static import static
urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)