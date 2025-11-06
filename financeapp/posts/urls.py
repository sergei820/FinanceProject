from django.urls import path

from . import views


urlpatterns = [
    path('', views.home, name='index'),
    path('about', views.about, name='about'),
    path('posts/', views.index, name='posts'),
    path('posts/<int:post_id>', views.post, name='post'),
    path('posts/search', views.search, name='search'),

]
