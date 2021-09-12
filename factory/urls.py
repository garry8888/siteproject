from django.urls import path
from . import views

urlpatterns = [
    path('factory/', views.update_bank_statements_data, name='update_bank_statements_data'),
    path('update_pdf/', views.update_bank_statements_data_pdf, name='update_bank_statements_data_pdf')
]