from django.shortcuts import render
from grafic_matplotlib.models import Pie, Diagram
from grafic_matplotlib.analytics.query_data import amount_expenses


def sum_transactions():
    list_amount_expenses = amount_expenses()
    expenses = []

    for percent in list_amount_expenses:
        expenses.append(percent['total_amount'])

    return sum(expenses)


def expenses_per_category():
    list_amount_expenses = amount_expenses()
    amnt_expenses = []

    for amount in list_amount_expenses:
        amnt_expenses.append({amount['type_expenses_ru']: amount['total_amount']})

    return amnt_expenses

def index(request):
    return render(request, 'grafic_matplotlib/analytics.html', {})


def index_p(request):
    pie_p = Pie.figure.source

    return render(request, 'grafic_matplotlib/pie.html', {'pie_fig': pie_p, 'sum_expenses': sum_transactions(), 'amount_expenses': expenses_per_category()})


def index_d(request):
    diagram = Diagram.figure.source

    return render(request, 'grafic_matplotlib/diagram.html', {'diagram_fig': diagram, 'sum_expenses': sum_transactions(), 'amount_expenses': expenses_per_category()})


def index_plan(request):
    return render(request, 'grafic_matplotlib/planning.html', {'sum_expenses': sum_transactions(), 'amount_expenses': expenses_per_category()})
