from django.contrib import admin
from .models import TypeExpenses, BankStatements, MoneyTransaction

admin.site.register(TypeExpenses)
admin.site.register(BankStatements)
admin.site.register(MoneyTransaction)