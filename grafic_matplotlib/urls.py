from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('pie/', views.index_p, name='index_p'),
    path('diagram/', views.index_d, name='index_d'),
    path('planning/', views.index_plan, name='index_plan')
]
