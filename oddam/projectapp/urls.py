from django.urls import path

from . import views

app_name = 'projectapp'

urlpatterns = [
    path('', views.LandingPage.as_view(), name='landingpage'),
    path('add', views.AddDonation.as_view(), name='add'),
    path('login', views.Login.as_view(), name='login'),
    path('register', views.Register.as_view(), name='register'),

]
