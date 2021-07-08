from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name="my_index"),
    path('success/', views.success, name="my_success"),
    path('register/', views.register, name="my_register"),
    path('login/', views.login, name="my_login"),
    path('homepage/', views.homepage, name="my_homepage"),
    path('wall/', views.wall, name="my_wall"),
    path('post_message/', views.post_message, name="my_post_message"),
    path('del_message/', views.del_message, name="my_del_message"),
    path('post_comment/', views.post_comment, name="my_post_comment"),
    path('del_comment/', views.del_comment, name="my_del_comment"),
    path('about/', views.about, name="my_about"),
    path('logout/', views.logout, name="my_logout"),
]