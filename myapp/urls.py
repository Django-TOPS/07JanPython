from django.contrib import admin
from django.urls import path
from myapp import views

urlpatterns = [
    path('',views.index),
    path('notes/',views.notes,name='notes'),
    path('updateprofile/',views.updateprofile),
    path('userlogout/',views.userlogout),
]
