from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.register, name='register'),
    path('home/<int:pk>',views.home,name='home'),
    path('addfunds/<int:pk>',views.addfunds,name='addfunds'),
    path('postfunds/<int:pk>',views.postfunds,name='postfunds'),
    path('game_home/<int:pk>',views.game_home,name='game_home'),
    path('redeempoints/<int:pk>', views.redeempoints, name='redeempoints'),

    path('create_wallet_request/<int:pk>',views.create_wallet_request,name='create_wallet_request'),
    path('create_wallet_post/<int:pk>', views.create_wallet_post, name='create_wallet_post'),
    path('all_transactions/<int:pk>',views.all_transactions,name='all_transactions'),
    path('login_redirect/',views.login_redirect,name='login_redirect'),
    path('login/',auth_views.LoginView.as_view(template_name='userwallet/login.html'),name='login'),
    path('logout/',auth_views.LogoutView.as_view(template_name='userwallet/logout.html'),name='logout'),
]