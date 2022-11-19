from finance.models import Currency, Countries, TypeExpenses
from factory.models import BankStatementsData, Mcc
from django.core.exceptions import ObjectDoesNotExist
import json
import requests
from gsite.settings.env import env


# api_spreadsheets gsx2json parse spreadsheets data
def json_get(path=env.str('URL')):
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
            country.abbreviation = i["alpha3"]
            country.iso = i["iso"]
            country.save()
        except ObjectDoesNotExist:
            pass


# create TypeExpenses catalogue in the model TypeExpenses
def create_expenses(path=env.str('URL')):
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
def create_mcc(path=env.str('URL')):
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


