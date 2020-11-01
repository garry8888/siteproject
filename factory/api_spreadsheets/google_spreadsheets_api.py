from finance.models import Currency, Countries, TypeExpenses
from factory.models import BankStatementsData, Mcc
from django.core.exceptions import ObjectDoesNotExist
import json
import requests
from datetime import datetime
from decimal import *

# api_spreadsheets gsx2json
#TODO оптимизировать код, убрать повторяющиеся path

# parse spreadsheets data
def json_get(path='http://gsx2json.com/api?id=1BRDrKF9anTLPBBN5e3n_g2S0FTiiCFfPG5UuD2cnuPQ&sheet=4'):
    response = requests.get(path)
    data_spreadsheet = json.loads(response.text)
    data_db = data_spreadsheet['rows']
    return data_db


# write currency catalogue in the model Currency
def append_currency(func=json_get()):
    data = func
    d = []

    for i in data:
        d.append(dict(
            name=i["название"],
            abbreviation=i["код10"],
            #symbol=i["знак9"],
            index=i["index"]
        ))

    Currency.objects.bulk_create([Currency(**r) for r in d])


# create country catalogue in the model Countries
def append_country(func=json_get()):
    data = func

    for i in data:
        try:
            country = Countries.objects.get(country_ru=i["наименование"])
            country.country_en = i["наанглийском"]
            country.abbreviation = i["alpha2"]
            country.iso = i["iso"]
            country.save()
        except ObjectDoesNotExist:
            pass

# create BankStatements list in the model BankStatementsData
def load_bank_statements_data(path='http://gsx2json.com/api?id=1BRDrKF9anTLPBBN5e3n_g2S0FTiiCFfPG5UuD2cnuPQ&sheet=2'):
    response = requests.get(path)
    data_spreadsheet = json.loads(response.text)
    data_db = data_spreadsheet['rows']

    def numbers(data):              #TODO не убирает пробелы из числа: 1 000 000
        if type(data) == int:
            nums = Decimal(data)
        if type(data) == str:
            nums = Decimal(data.replace(',', '.'))
        return nums

    d = []
    for i in data_db:
        d.append(dict(
            purpose=i["призначення"],
            amount=numbers(i["сума"]),
            date_operation=datetime.strptime(i["датаоперації"], "%d.%m.%Y")
        ))

    BankStatementsData.objects.bulk_create([BankStatementsData(**r) for r in d])


# create TypeExpenses catalogue in the model TypeExpenses
def create_expenses(path='http://gsx2json.com/api?id=1BRDrKF9anTLPBBN5e3n_g2S0FTiiCFfPG5UuD2cnuPQ&sheet=3'):
    response = requests.get(path)
    data_spreadsheet = json.loads(response.text)
    data_db = data_spreadsheet['rows']
    d = []
    for i in data_db:
        d.append(dict(
            type_expenses_ua=i["ua"],
            type_expenses_ru=i["ru"],
            type_expenses_en=i["en"]
        ))

    TypeExpenses.objects.bulk_create([TypeExpenses(**r) for r in d])


# create MCC catalogue in the model Mcc
def create_mcc(path='http://gsx2json.com/api?id=1BRDrKF9anTLPBBN5e3n_g2S0FTiiCFfPG5UuD2cnuPQ&sheet=5'):
    response = requests.get(path)
    data_spreadsheet = json.loads(response.text)
    data_db = data_spreadsheet['rows']
    d = []

    for i in data_db:
        expenses = TypeExpenses.objects.get(type_expenses_ru=i["typeexpenses"])
        d.append(dict(
            mcc=i["mcc"],
            name=i["название"],
            category=i["категория"],
            type_expenses_id=expenses.pk
        ))

    Mcc.objects.bulk_create([Mcc(**r) for r in d])



