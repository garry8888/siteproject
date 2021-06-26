from json import JSONDecodeError

from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

from factory.models import BankStatementsData
import json
import requests
from datetime import datetime, date
from decimal import *

# api_spreadsheets gsx2json


# исключение дублей
def check_last_update_spreadsheet(new_data):  # проверка последней даты обновленной выписки
    data_length = len(new_data) - 1
    data = new_data[data_length]
    new_date = data['date_operation']
    new_amount = data['amount']
    user = data['user_id']
    try:
        exclude_duplicates = BankStatementsData.objects.get(date_operation=new_date.date(), user=user, amount=new_amount)
    except ObjectDoesNotExist:
        exclude_duplicates = 0

    return exclude_duplicates


# create BankStatements list in the model BankStatementsData path='http://gsx2json.com/api?id=1t3iHjR_pPDyV3PL4MyIxX287NqsyiiaBMWogQ9JEh00&sheet=2'
def load_bank_statements_data(url, sheet_numb, user_id):
    try:
        uri = url.split('/')  # ['https:', '', 'docs.google.com', 'spreadsheets', 'd', '1t3iHjR_pPDyV3PL4MyIxX287NqsyiiaBMWogQ9JEh00', 'edit#gid=885799634']

        path = 'http://gsx2json.com/api?id=%s&sheet=%s' % (uri[5], sheet_numb)

        response = requests.get(path)
        data_spreadsheet = json.loads(response.text)
        data_db = data_spreadsheet['rows']

        def numbers(data):
            if type(data) == int:
                nums = Decimal(data)
            if type(data) == str:
                nums_d = data.replace(' ', '')    # убирает пробелы из числа: 1 000 000
                nums = Decimal(nums_d.replace(',', '.'))

            return nums

        d = []
        for i in data_db:

            d.append(dict(
                purpose=i["призначення"],
                amount=numbers(i["сума"]),
                date_operation=datetime.strptime(i["датаоперації"], "%d.%m.%Y"),
                user_id=user_id  # User.objects.get(id=i['user']).id
            ))
        print(d[0]['date_operation'].date())
        find_duplicates = check_last_update_spreadsheet(d)

        if find_duplicates == 0:
            BankStatementsData.objects.bulk_create([BankStatementsData(**r) for r in d])
            print('LOAD')
        else:
            print('NOT LOAD')
            return 1
    except JSONDecodeError:
        return 0
