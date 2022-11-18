from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from factory.api_spreadsheets.handler import load_bank_statements_data
from factory.data_processor.bankstatements_data_handler import create_bank_statements, \
    bnp_paribas_upload_clear_financial_data
from factory.forms import UrlInput, PdfForm
from factory.pdf_reader.bnp_paribas_pdf_data_hadler import bnp_paribas_load_bank_statement
from factory.pdf_reader.pdf_data_handler import load_bank_statement
from gsite.settings import MEDIA_ROOT
from users.core.get_user import user_from_session_key


# uploading bank statement data from google spreadsheet
@login_required(login_url='/users/login/')
def update_bank_statements_data(request):
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
                confirm = 'Выписка не обновлена'
            elif update_bankstatementsdata == 1:
                confirmation = 'Удалите из документа ранее загруженную информацию'
                confirm = 'Выписка не обновлена'
            else:
                confirmation = 'Информация загружена'

                try:
                    update_bankstatements = create_bank_statements(user_id=user.id)
                    confirm = 'Выписка обновлена'

                except Exception:
                    confirm = 'Выписка не обновлена'

            return render(request, 'factory/google_api_spreadsheet/update_bankstatements.html',
                          {'form_url': form_url, 'confirmation': confirmation, 'confirm': confirm})

    else:
        form_url = UrlInput()

    return render(request, 'factory/google_api_spreadsheet/update_bankstatements.html', {'form_url': form_url})


# uploading data from PDF bank statement
@login_required(login_url='/users/login/')
def update_bank_statements_data_pdf(request):
    session_k = request.session.session_key
    user = user_from_session_key(session_k)

    if request.method == 'POST':
        form_pdf = PdfForm(request.POST, request.FILES)
        file = request.FILES['document']

        if form_pdf.is_valid():
            bank = form_pdf.cleaned_data['bank']
            form_pdf.save()

            # load Alfa-Bank bank statement
            if bank.bank_short_name == 'Alfa-Bank':
                update_bankstatementsdata = load_bank_statement(
                    pdf_file="%s/%s" % (MEDIA_ROOT, str(file)),
                    user_id=user.id,
                    bank=bank.id
                )

            # load BNP Paribas Bank bank statement
            if bank.bank_short_name == 'BNP Paribas':
                update_bankstatementsdata = bnp_paribas_load_bank_statement(
                    pdf_file="%s/%s" % (MEDIA_ROOT, str(file)),
                    user_id=user.id,
                    bank=bank.id
                )

            if update_bankstatementsdata == 0:
                confirmation = 'Формат файла не поддерживается'
                confirm = 'Выписка не обновлена'
            elif update_bankstatementsdata == 1:
                confirmation = 'Удалите из документа ранее загруженную информацию'
                confirm = 'Выписка не обновлена'
            else:
                confirmation = 'Информация загружена.'

                try:
                    if bank.bank_short_name == 'Alfa-Bank':
                        update_bankstatements = create_bank_statements(user_id=user.id, bank_id=bank.id)

                    if bank.bank_short_name == 'BNP Paribas':
                        update_bankstatements = bnp_paribas_upload_clear_financial_data(user_id=user.id, bank_id=bank.id)

                    confirm = 'Выписка обновлена'

                except Exception:
                    confirm = 'Выписка не обновлена'

            return render(request, 'factory/pdf_update/success_update.html',
                          {'confirmation': confirmation, 'confirm': confirm})

    else:
        form_pdf = PdfForm()

    return render(request, 'factory/pdf_update/update_pdf.html', {'form_pdf': form_pdf})
