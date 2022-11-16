from django.contrib.auth.models import User
from django.db import models


# bank statement in original view
class BankStatementsData(models.Model):
    purpose = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=20, decimal_places=2)
    date_operation = models.DateField()
    date_created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    bank = models.ForeignKey('finance.Bank', on_delete=models.CASCADE, null=True)


class Mcc(models.Model):
    mcc = models.PositiveIntegerField()
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=100)
    type_expenses = models.ForeignKey('finance.TypeExpenses', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.mcc} - {self.name}: ({self.category} - {self.type_expenses})'


""""
class CatalogPlacesExpenses(models.Model):
    name = models.CharField(max_length=100)
    pos = models.CharField(max_length=20)
    city = models.CharField(max_length=30)
    mcc = models.ForeignKey(Mcc, on_delete=models.CASCADE)
"""


class Document(models.Model):
    bank = models.ForeignKey('finance.Bank', on_delete=models.CASCADE)
    description = models.CharField(max_length=255, blank=False)
    document = models.FileField(blank=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)
