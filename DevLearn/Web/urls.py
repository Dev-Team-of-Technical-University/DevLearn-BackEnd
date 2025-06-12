from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.home_page, name='home_page'),
    path("about_us", views.about_us, name='about-us'),
    path("contact_us", views.contact_us, name='contact-us'),

    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('forget-password/', views.forget_password_request_view, name='forget-password'),
    path('forget-password-confirm/', views.forget_password_confirm_view, name='forget-password-confirm'),
]