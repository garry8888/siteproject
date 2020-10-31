from django.db import models


class BankStatementsData(models.Model):
    purpose = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=20, decimal_places=2)
    date_operation = models.DateField()
    date_created = models.DateTimeField(auto_now_add=True)
