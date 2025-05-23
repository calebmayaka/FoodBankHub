from django.urls import path
from . import views

app_name = 'AuthApp'

urlpatterns = [
    path('register/donor/', views.donor_register_view, name='donor_register'),
    path('register/foodbank/', views.foodbank_register_view, name='foodbank_register'),
    path('register/recipient/', views.recipient_register_view, name='recipient_register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/donor/', views.donor_dashboard_view, name='donor_dashboard'),
    path('dashboard/foodbank/', views.foodbank_dashboard_view, name='foodbank_dashboard'),
    path('dashboard/recipient/', views.recipient_dashboard_view, name='recipient_dashboard'),
]
