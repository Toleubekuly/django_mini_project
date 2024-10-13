from django.urls import path
from Users import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('profile/<str:username>/', views.profile_detail, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('follow/<str:username>/', views.follow_user, name='follow_user'),
    path('unfollow/<str:username>/', views.unfollow_user, name='unfollow_user'),
]
