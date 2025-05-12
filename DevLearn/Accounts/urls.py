from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),

    path('forgot-password/request/', views.ForgetPasswordRequestView.as_view()),
    path('forgot-password/confirm/', views.ForgetPasswordConfirmView.as_view()),

]
