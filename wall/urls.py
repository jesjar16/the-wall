from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name="my_index"),
    path('success/', views.success, name="my_success"),
    path('register/', views.register, name="my_register"),
    path('login/', views.login, name="my_login"),
    path('homepage/', views.homepage, name="my_homepage"),
    path('about/', views.about, name="my_about"),
    path('logout/', views.logout, name="my_logout"),
]