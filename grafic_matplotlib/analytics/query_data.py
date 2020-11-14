from django.db.models import Sum
from finance.models import BankStatements, TypeExpenses


def sum_expenses():
    expenses = TypeExpenses.objects.all()
    t_expenses = []
    total_expenses = BankStatements.objects.filter(type_transaction_id=1).aggregate(sum_t=Sum('sum_transaction'))

    for exp in expenses:
        all_expenses = BankStatements.objects.filter(type_expenses=exp.id, type_transaction_id=1).aggregate(sum_t=Sum('sum_transaction'))
        if all_expenses['sum_t'] is not None:
            t_expenses.append(dict(
                type_expenses_ru=exp.type_expenses_ru,
                total_amount=round((all_expenses['sum_t'] / total_expenses['sum_t']) * 100)
            ))

    return t_expenses
