from django.conf.urls.static import static
from django.urls import path

from gsite.settings import settings
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('pie/', views.index_p, name='index_p'),
    path('diagram/', views.index_d, name='index_d'),
    path('planning/', views.index_plan, name='index_plan'),
    path('manual-input/', views.manual_input, name='manual_input'),
    path('change/', views.get_expenses_list, name='get_expenses_list'),
    path('change/post/', views.update_expenses, name='update_expenses')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
