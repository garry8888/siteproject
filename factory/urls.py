from django.conf.urls.static import static
from django.urls import path

from gsite.settings import settings
from . import views

urlpatterns = [
    path('factory/', views.update_bank_statements_data, name='update_bank_statements_data'),
    path('update_pdf/', views.update_bank_statements_data_pdf, name='update_bank_statements_data_pdf'),
    path('success_update/', views.update_bank_statements_data_pdf, name='success_update_pdf')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
