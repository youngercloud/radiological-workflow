"""workflow URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
import radiological.views as app_views

urlpatterns = [
    path('', app_views.index),
    path('/', app_views.index),
    path('home/', app_views.index),
    path('order/', app_views.order),
    path('checkin/', app_views.checkin),
    path('report/', app_views.report),
    path('booking/', app_views.booking),
    path('sendOrder/', app_views.OrderView.as_view()),
    path('sendBooking/', app_views.BookingView.as_view()),
]
