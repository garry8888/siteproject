from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('pie/', views.index_p, name='index_p')
]
