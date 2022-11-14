from factory.models import BankStatementsData
from factory.pdf_reader.data_from_pdf import get_pdf_data, bnp_paribas_delete_headers
from decimal import Decimal, InvalidOperation
from datetime import datetime

from factory.pdf_reader.pdf_data_handler import check_last_update


# BNP Paribas bank: uploading rough finance data from pdf payslip


# get rough transaction details(description) for uploading
def get_purpose(new_pdf_data):
    purpose = []
    rough_transaction_details = [i[2].replace('\n', ' ').split('  ') for i in new_pdf_data]
    rough_transaction_details[1].pop(0)

    transaction_details = rough_transaction_details[0] + rough_transaction_details[1]

    for item in transaction_details:
        if item != '':
            purpose.append(item)

    return purpose


# get transaction amount in decimals
def get_amount(new_pdf_data):
    amount = new_pdf_data[0][3].replace(',', '.')
    try:
        decimal_amount = Decimal(amount)

    except InvalidOperation:
        decimal_amount = Decimal(amount.replace('\xa0', ''))

    return decimal_amount


# upload rough finance data from pdf payslip
def bnp_paribas_load_bank_statement(pdf_file, user_id=1, bank=2):
    new_rough_data = get_pdf_data(pdf_file)
    new_data = bnp_paribas_delete_headers(new_rough_data)

    if new_data == 'Incorrect format':
        return 0

    uploading_data = []
    for item in new_data:
        uploading_data.append(dict(
            purpose=get_purpose(item),
            amount=get_amount(item),
            date_operation=datetime.strptime(item[0][1], "%d.%m.%Y"),
            user_id=user_id,
            bank_id=bank
        ))

    # TODO create separate function "uploading_data"
    find_duplicates = check_last_update(uploading_data)

    if find_duplicates == 0:
        BankStatementsData.objects.bulk_create([BankStatementsData(**r) for r in uploading_data])
        print('LOAD')
    else:
        print('NOT LOAD')
        return 1

    return uploading_data
