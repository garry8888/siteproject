from django.db import models


class Currency(models.Model):
    name = models.CharField(max_length=100)
    abbreviation = models.CharField(max_length=50)
    #symbol = models.CharField(max_length=100, null=True)
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


class MoneyTransaction(models.Model):
    type_transaction_en = models.CharField(max_length=50)
    type_transaction_ru = models.CharField(max_length=50, null=True)
    type_transaction_ua = models.CharField(max_length=50)


class BankStatements(models.Model):
    transaction_place = models.CharField(max_length=200)
    type_place = models.ForeignKey(Places, on_delete=models.CASCADE, null=True)
    type_transaction = models.ForeignKey(MoneyTransaction, on_delete=models.CASCADE)
    sum_transaction = models.DecimalField(max_digits=20, decimal_places=2)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    country = models.ForeignKey(Countries, on_delete=models.CASCADE)
    date_of_trans = models.DateField(null=True)
    date_created = models.DateTimeField(auto_now_add=True)


