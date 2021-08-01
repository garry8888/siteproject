from django.contrib.auth.models import User
from django.db import models

from factory.models import BankStatementsData


class Currency(models.Model):
    name = models.CharField(max_length=100)
    abbreviation = models.CharField(max_length=50)
    # symbol = models.CharField(max_length=100, null=True)
    index = models.PositiveIntegerField(null=True)


class Countries(models.Model):
    country_ru = models.CharField(max_length=100)
    country_ua = models.CharField(max_length=100, null=True)
    country_en = models.CharField(max_length=100, null=True)
    abbreviation = models.CharField(max_length=50, null=True)
    iso = models.PositiveIntegerField(null=True)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)


class Places(models.Model):
    type_place_ua = models.CharField(max_length=100)
    type_place_ru = models.CharField(max_length=100)
    type_place_en = models.CharField(max_length=100)


class TypeExpenses(models.Model):
    type_expenses_ua = models.CharField(max_length=100)
    type_expenses_ru = models.CharField(max_length=100, null=True)
    type_expenses_en = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.id} - {self.type_expenses_ru}'


class MoneyTransaction(models.Model):
    type_transaction_en = models.CharField(max_length=50)
    type_transaction_ru = models.CharField(max_length=50, null=True)
    type_transaction_ua = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.id} - {self.type_transaction_ru}'


class BankStatements(models.Model):
    transaction_place = models.CharField(max_length=200)
    type_expenses = models.ForeignKey(TypeExpenses, on_delete=models.CASCADE, null=True)
    type_transaction = models.ForeignKey(MoneyTransaction, on_delete=models.CASCADE)
    sum_transaction = models.DecimalField(max_digits=20, decimal_places=2)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE, null=True)
    country = models.ForeignKey(Countries, on_delete=models.CASCADE, null=True)
    date_of_trans = models.DateField(null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    original = models.ForeignKey(BankStatementsData, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f'{self.id} - {self.transaction_place}'


