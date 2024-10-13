from django.urls import path
from Users import views

urlpatterns = [
    path('', views.registration, name='post_list'),
]
