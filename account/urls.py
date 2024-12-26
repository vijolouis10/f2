from django.urls import path
from . import views

urlpatterns = [
    path('register/',views.register,name='register'),
    path('actiavte/<uidb64>/<token>/',views.activate,name='activate'),
    path('login/',views.user_login,name='login'),
     path('otp/',views.otp_verify,name='otp'),
    path('forgot_password/',views.forgot_password,name='forgot_password'),
    path('reset_password_validation/<uidb64>/<token>/',views.reset_password_validation,name='reset_password_validation'),
    path('reset_password/',views.reset_password,name='reset_password'),
    path('logout/',views.user_logout,name='logout'),

    path('',views.dashboard,name='dashboard'),
    path('my_orders/',views.my_orders,name='my_orders'),
    path('order_detail/<int:order_id>/',views.order_detail,name='order_detail'),
    path('edit_profile/',views.edit_profile,name='edit_profile'),
    path('change_password/',views.change_password,name='change_password'),
    
    path('order_tracking/<int:id>/',views.OrderTrack,name='order_tracking'),
]
