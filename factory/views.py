from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render

from factory.api_spreadsheets.handler import load_bank_statements_data
from factory.data_processor.bankstatements_data_handler import create_bank_statements
from factory.forms import UrlInput, PdfForm
from factory.pdf_reader.pdf_data_handler import load_bank_statement
from gsite.settings import MEDIA_ROOT
from users.core.get_user import user_from_session_key


@login_required(login_url='/users/login/')
def update_bank_statements_data(request):   #обновление данных по банковской выписке BankStatementsData
    session_k = request.session.session_key
    user = user_from_session_key(session_k)

    if request.method == 'POST':
        form_url = UrlInput(request.POST)

        if form_url.is_valid():
            url = form_url.cleaned_data['url_field']
            page_number = form_url.cleaned_data['sheet_number']
            update_bankstatementsdata = load_bank_statements_data(url=url, sheet_numb=page_number, user_id=user.id)

            if update_bankstatementsdata == 0:
                confirmation = 'Информация не загружена. Документ опубликован в интернете?'
                confirm = 'Ошибка. Выписка не обновлена'
            elif update_bankstatementsdata == 1:
                confirmation = 'Информация не загружена. Удалите из документа ранее загруженную информацию'
                confirm = 'Ошибка. Выписка не обновлена'
            else:
                confirmation = 'Информация загружена.'

                try:
                    update_bankstatements = create_bank_statements(user_id=user.id)
                    confirm = 'Выписка обновлена'

                except Exception:
                    confirm = 'Ошибка. Выписка не обновлена'

            return render(request, 'factory/google_api_spreadsheet/update_bankstatements.html',
                          {'form_url': form_url, 'confirmation': confirmation, 'confirm': confirm})

    else:
        form_url = UrlInput(request.POST)

    return render(request, 'factory/google_api_spreadsheet/update_bankstatements.html', {'form_url': form_url})

def handle_uploaded_file(f):
    with open('media/["file"]', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


@login_required(login_url='/users/login/')
def update_bank_statements_data_pdf(request):
    session_k = request.session.session_key
    user = user_from_session_key(session_k)

    if request.method == 'POST':
        form_pdf = PdfForm(request.POST, request.FILES)
        file = request.FILES['document']
        print(type(file))

        if form_pdf.is_valid(): # TODO убрать POST при перезагрузке страницы
            form_pdf.save()
            update_bankstatementsdata = load_bank_statement(pdf_file="%s\%s" % (MEDIA_ROOT, str(file)), user_id=user.id)

            if update_bankstatementsdata == 0:
                confirmation = 'Информация не загружена. Документ опубликован в интернете?'
                confirm = 'Ошибка. Выписка не обновлена'
            elif update_bankstatementsdata == 1:
                confirmation = 'Информация не загружена. Удалите из документа ранее загруженную информацию'
                confirm = 'Ошибка. Выписка не обновлена'
            else:
                confirmation = 'Информация загружена.'

                try:
                    update_bankstatements = create_bank_statements(user_id=user.id)
                    confirm = 'Выписка обновлена'

                except Exception:
                    confirm = 'Ошибка. Выписка не обновлена'

            return render(request, 'factory/pdf_update/update_pdf.html',
                          {'form_pdf': form_pdf, 'confirmation': confirmation, 'confirm': confirm})

    else:
        form_pdf = PdfForm(request.POST)

    return render(request, 'factory/pdf_update/update_pdf.html', {'form_pdf': form_pdf})
