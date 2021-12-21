#encoding:utf-8

from django.urls import path
from django.contrib import admin
from main import views

urlpatterns = [
    path('', views.index),
    path('populate/', views.populateDB),
    path('loadRS', views.loadRS),
     path('recommendBooks/', views.recommendedBooks),
    # path('recommendedFilmsUserItem', views.recommendedFilmUserItems),
    # path('recommendedUserFilm', views.recommendedUser),
    # path('similarFilms', views.similarFilms),
    # path('search', views.search),
    path('admin/', admin.site.urls),
]