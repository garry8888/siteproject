from datetime import datetime, date

from django.shortcuts import render

from grafic_matplotlib.core.forms import Calendar
from grafic_matplotlib.models import Pie, Diagram
from grafic_matplotlib.figures import pie_figure, get_plot
from grafic_matplotlib.analytics.query_data import amount_expenses, sum_expenses


def sum_transactions(s, e):

    if s is None and e is None:
        s = '2020-11-01'
        e = '2020-11-30'
    list_amount_expenses = amount_expenses(start=s, end=e)
    expenses = []

    for percent in list_amount_expenses:
        expenses.append(percent['total_amount'])

    return sum(expenses)


def expenses_per_category(s, e):
    if s is None and e is None:
        s = '2020-11-01'
        e = '2020-11-30'
    list_amount_expenses = amount_expenses(start=s, end=e)
    amnt_expenses = []

    for amount in list_amount_expenses:
        amnt_expenses.append({amount['type_expenses_ru']: amount['total_amount']})

    return amnt_expenses



def index(request):
    return render(request, 'grafic_matplotlib/analytics.html', {})


def index_p(request):
    pie_p = Pie.figure.source

    if request.method == 'POST':
        form = Calendar(request.POST)

        if form.is_valid():
            s = form.cleaned_data['date_field_start']
            e = form.cleaned_data['date_field_end']
            data_update = expenses_per_category(s=s, e=e)
            pie_update = get_plot(s, e)
            return render(request, 'grafic_matplotlib/pie.html', {'pie_fig': pie_update,
                                                                  'sum_expenses': sum_transactions(s=s, e=e),
                                                          'amount_expenses': data_update, 'form': form})

    else:
        form = Calendar()
    return render(request, 'grafic_matplotlib/pie.html', {'pie_fig': pie_p, 'sum_expenses': sum_transactions(s=None, e=None),
                                                          'amount_expenses': expenses_per_category(s=None, e=None),
                                                          'form': form})


def index_d(request):
    diagram = Diagram.figure.source

    if request.method == 'POST':
        form = Calendar(request.POST)

        if form.is_valid():
            s = form.cleaned_data['date_field_start']
            e = form.cleaned_data['date_field_end']
            data_update = expenses_per_category(s=s, e=e)
            return render(request, 'grafic_matplotlib/pie.html', {'sum_expenses': sum_transactions(s=s, e=e),
                                                          'amount_expenses': data_update, 'form': form})

    else:
        form = Calendar()

    return render(request, 'grafic_matplotlib/diagram.html', {'diagram_fig': diagram, 'sum_expenses': sum_transactions(s=None, e=None),
                                                          'amount_expenses': expenses_per_category(s=None, e=None),
                                                          'form': form})


def index_plan(request):
    if request.method == 'POST':
        form = Calendar(request.POST)

        if form.is_valid():
            s = form.cleaned_data['date_field_start']
            e = form.cleaned_data['date_field_end']
            data_update = expenses_per_category(s=s, e=e)
            return render(request, 'grafic_matplotlib/pie.html', {'sum_expenses': sum_transactions(s=s, e=e),
                                                          'amount_expenses': data_update, 'form': form})

    else:
        form = Calendar()

    return render(request, 'grafic_matplotlib/planning.html', {'sum_expenses': sum_transactions(s=None, e=None),
                                                               'amount_expenses': expenses_per_category(s=None, e=None),
                                                               'form': form})
