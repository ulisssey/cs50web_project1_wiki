from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>/", views.show_wiki, name='show'),
    path("search/", views.search, name='search'),
    path("create/", views.create_page, name='create'),
    path("edit/<str:title>/", views.edit, name='edit'),
    path("random/", views.random_page, name='random')
]
