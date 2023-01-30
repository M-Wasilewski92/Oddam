from django.urls import path

from . import views

app_name = 'projectapp'

urlpatterns = [
    path('', views.LandingPage.as_view(), name='landingpage'),
    path('add/', views.AddDonation.as_view(), name='add'),
    path('login/', views.Login.as_view(), name='login'),
    path('register/', views.Register.as_view(), name='register'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('donation/', views.SuccessDonation.as_view(), name='donation'),
    path('profile/', views.UserProfile.as_view(), name='profile'),
    path('settings/', views.UserSettings.as_view(), name='settings'),
    path('password_reset/', views.PasswordResetRequest.as_view(), name='password_reset'),


]
