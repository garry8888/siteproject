from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required(login_url='/users/login/')
def update_bank_statements_data(request):  #обновление данных по банковской выписке BankStatementsData
    return render(request, 'factory/google_api_spreadsheet/update_bankstatements.html', {})
