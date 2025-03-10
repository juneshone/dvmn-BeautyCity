"""
URL configuration for BeautyCity project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.contrib.auth.views import LogoutView
from django.urls import path
from beauty_salons import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path('service/', views.service, name='service'),
    path('serviceFinally/', views.serviceFinally, name='serviceFinally'),
    path('notes/', views.notes, name='notes'),
    path('save_pay/', views.save_pay, name='save_pay'),
    path('', views.index, name='index'),
    path('account/', views.account, name='account'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('appointment/', views.appointment, name='appointment'),
]

#
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
