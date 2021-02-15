from datetime import datetime, date
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from grafic_matplotlib.core.forms import Calendar, UserChoice
from grafic_matplotlib.models import Pie, Diagram
from grafic_matplotlib.figures import pie_figure, get_plot
from grafic_matplotlib.analytics.query_data import amount_expenses, sum_expenses


def sum_transactions(u, s, e):

    if s is None and e is None:
        u = [1, 2]
        s = '2020-11-01'
        e = '2020-11-30'
    list_amount_expenses = amount_expenses(users=u, start=s, end=e)
    expenses = []

    for percent in list_amount_expenses:
        expenses.append(percent['total_amount'])

    return sum(expenses)


def expenses_per_category(u, s, e):
    if s is None and e is None:
        u = [1, 2]
        s = '2020-11-01'
        e = '2020-11-30'
    list_amount_expenses = amount_expenses(users=u, start=s, end=e)
    amnt_expenses = []

    for amount in list_amount_expenses:
        amnt_expenses.append({amount['type_expenses_ru']: amount['total_amount']})

    return amnt_expenses


@login_required(login_url='/users/login/')
def index(request):
    return render(request, 'grafic_matplotlib/analytics.html', {})


@login_required(login_url='/users/login/')
def index_p(request):
    pie_p = Pie.figure.source

    if request.method == 'POST':
        form_cal = Calendar(request.POST)
        form_user = UserChoice(request.POST)

        if form_cal.is_valid() and form_user.is_valid():
            s = form_cal.cleaned_data['date_field_start']
            e = form_cal.cleaned_data['date_field_end']
            choice_user = [i.id for i in form_user.cleaned_data['user_field']]
            print(choice_user)
            data_update = expenses_per_category(choice_user, s, e)
            pie_update = get_plot(choice_user, s, e)
            return render(request, 'grafic_matplotlib/pie.html', {'pie_fig': pie_update,
                                                                  'sum_expenses': sum_transactions(u=choice_user, s=s, e=e),
                                                                  'amount_expenses': data_update, 'form_cal': form_cal,
                                                                  'form_user': form_user}
                          )

    else:
        form_cal = Calendar()
        form_user = UserChoice()
    return render(request, 'grafic_matplotlib/pie.html', {'pie_fig': pie_p,
                                                          'sum_expenses': sum_transactions(u=None, s=None, e=None),
                                                          'amount_expenses': expenses_per_category(u=None, s=None, e=None),
                                                          'form_cal': form_cal, 'form_user': form_user})


@login_required(login_url='/users/login/')
def index_d(request):
    diagram = Diagram.figure.source

    if request.method == 'POST':
        form_cal = Calendar(request.POST)
        form_user = UserChoice(request.POST)

        if form_cal.is_valid() and form_user.is_valid():
            s = form_cal.cleaned_data['date_field_start']
            e = form_cal.cleaned_data['date_field_end']
            choice_user = [i.id for i in form_user.cleaned_data['user_field']]
            data_update = expenses_per_category(u=choice_user, s=s, e=e)
            return render(request, 'grafic_matplotlib/pie.html', {'sum_expenses': sum_transactions(u=choice_user, s=s, e=e),
                                                                  'amount_expenses': data_update,
                                                                  'form_cal': form_cal, 'form_user': form_user})

    else:
        form_cal = Calendar()
        form_user = UserChoice()

    return render(request, 'grafic_matplotlib/diagram.html', {'diagram_fig': diagram,
                                                              'sum_expenses': sum_transactions(u=None, s=None, e=None),
                                                              'amount_expenses': expenses_per_category(u=None, s=None, e=None),
                                                              'form_cal': form_cal, 'form_user': form_user})


@login_required(login_url='/users/login/')
def index_plan(request):
    if request.method == 'POST':
        form_cal = Calendar(request.POST)
        form_user = UserChoice(request.POST)

        if form_cal.is_valid() and form_user.is_valid():
            s = form_cal.cleaned_data['date_field_start']
            e = form_cal.cleaned_data['date_field_end']
            choice_user = [i.id for i in form_user.cleaned_data['user_field']]
            data_update = expenses_per_category(u=choice_user, s=s, e=e)
            return render(request, 'grafic_matplotlib/pie.html', {'sum_expenses': sum_transactions(s=s, e=e),
                                                          'amount_expenses': data_update,
                                                                  'form_cal': form_cal, 'form_user': form_user})

    else:
        form_cal = Calendar()
        form_user = UserChoice()

    return render(request, 'grafic_matplotlib/planning.html', {'sum_expenses': sum_transactions(u=None, s=None, e=None),
                                                               'amount_expenses': expenses_per_category(u=None, s=None, e=None),
                                                               'form_cal': form_cal, 'form_user': form_user})
