from django.db.models import Sum
from finance.models import BankStatements, TypeExpenses


def sum_expenses(users, start, end):
    expenses = TypeExpenses.objects.all()
    t_expenses = []
    total_expenses = BankStatements.objects.filter(type_transaction_id=1, date_of_trans__range=[start, end]).\
        aggregate(sum_t=Sum('sum_transaction'))

    for exp in expenses:
        all_expenses = BankStatements.objects.filter(user_id__in=users, type_expenses=exp.id, type_transaction_id=1,
                                                     date_of_trans__range=[start, end]).\
            aggregate(sum_t=Sum('sum_transaction'))

        if all_expenses['sum_t'] is not None:
            t_expenses.append(dict(
                type_expenses_ru=exp.type_expenses_ru,
                total_amount=round((all_expenses['sum_t'] / total_expenses['sum_t']) * 100)
            ))

    return t_expenses


def amount_expenses(users, start, end):
    expenses = TypeExpenses.objects.all()
    t_expenses = []

    for exp in expenses:
        all_expenses = BankStatements.objects.filter(user_id__in=users, type_expenses=exp.id, type_transaction_id=1,
                                                     date_of_trans__range=[start, end]).\
            aggregate(sum_t=Sum('sum_transaction'))

        if all_expenses['sum_t'] is not None:
            t_expenses.append(dict(
                type_expenses_ru=exp.type_expenses_ru,
                total_amount=all_expenses['sum_t']
            ))

    return t_expenses
