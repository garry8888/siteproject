import calendar
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render

from finance.models import BankStatements, MoneyTransaction, TypeExpenses
from grafic_matplotlib.core.forms import Calendar, UserChoice, ChoiceYear, ManualInput
from grafic_matplotlib.models import Pie
from grafic_matplotlib.figures import get_plot, get_bar_chart
from grafic_matplotlib.analytics.query_data import amount_expenses, expenses_per_month
from users.core.get_user import user_from_session_key


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


def month_expenses(u, y):
    if u is None:
        u = [1, 2]
        y = '2020'
    list_month_expenses = expenses_per_month(users=u, year=y)
    mnth_expenses = []

    for amount in list_month_expenses:
        mnth_expenses.append({calendar.month_abbr[int(amount['month'])]: amount['total_amount']})

    return mnth_expenses


@login_required(login_url='/users/login/')
def index(request):
    return render(request, 'grafic_matplotlib/analytics.html')


@login_required(login_url='/users/login/')
def index_p(request):
    pie_update = get_plot(users=[1, 2], s_day='2021-08-01', e_day='2021-08-31')

    if request.method == 'POST':
        form_cal = Calendar(request.POST)
        form_user = UserChoice(request.POST)
        #form_manual_input = ManualInput(request.POST)

        if form_cal.is_valid() and form_user.is_valid():
            s = form_cal.cleaned_data['date_field_start']
            e = form_cal.cleaned_data['date_field_end']
            choice_user = [i.id for i in form_user.cleaned_data['user_field']]
            data_update = expenses_per_category(choice_user, s, e)
            pie_update = get_plot(choice_user, s, e)
            return render(request, 'grafic_matplotlib/pie.html', {'pie_fig': pie_update,
                                                                  'sum_expenses': sum_transactions(u=choice_user, s=s, e=e),
                                                                  'amount_expenses': data_update, 'form_cal': form_cal,
                                                                  'form_user': form_user})
                                                                  # 'form_manual_input': form_manual_input})

    else:
        form_cal = Calendar()
        form_user = UserChoice()
        # form_manual_input = ManualInput(request.POST)
    return render(request, 'grafic_matplotlib/pie.html', {'pie_fig': pie_update,
                                                          'sum_expenses': sum_transactions(u=None, s=None, e=None),
                                                          'amount_expenses': expenses_per_category(u=None, s=None, e=None),
                                                          'form_cal': form_cal, 'form_user': form_user})
                                                          # 'form_manual_input': form_manual_input})


@login_required(login_url='/users/login/')
def index_d(request):   #TODO сделать возможность ввести год
    bar_char = get_bar_chart(users=[1, 2], year='2020')

    if request.method == 'POST':
        form_year = ChoiceYear(request.POST)
        form_user = UserChoice(request.POST)

        if form_year.is_valid() and form_user.is_valid():
            choice_year = form_year.cleaned_data['year_field']
            choice_user = [i.id for i in form_user.cleaned_data['user_field']]
            data_update = month_expenses(choice_user, choice_year)
            bar_char = get_bar_chart(choice_user, choice_year)
            return render(request, 'grafic_matplotlib/diagram.html', {'bar_char': bar_char,
                                                                  'amount_expenses': data_update,
                                                                      'form_year': form_year, 'form_user': form_user})

    else:
        form_year = ChoiceYear()
        form_user = UserChoice()

    return render(request, 'grafic_matplotlib/diagram.html', {'bar_char': bar_char,
                                                              'amount_expenses': month_expenses(u=None, y=None),
                                                              'form_year': form_year, 'form_user': form_user})


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


@login_required(login_url='/users/login/')
def manual_input(request):
    session_k = request.session.session_key
    user = user_from_session_key(session_k)

    if request.method == 'POST':
        form_manual_input = ManualInput(request.POST)

        if form_manual_input.is_valid():
            trans_place = form_manual_input.cleaned_data['transaction_place']
            type_expenses = form_manual_input.cleaned_data['type_expenses']
            type_transaction = form_manual_input.cleaned_data['type_transaction']
            sum_transaction = form_manual_input.cleaned_data['sum_trans']
            date_of_trans = form_manual_input.cleaned_data['date_trans']
            user = user
            confirm = 'Данные успешно сохранены'
            new_data = BankStatements(
                transaction_place=trans_place,
                type_expenses_id=type_expenses.id,
                type_transaction_id=type_transaction.id,
                sum_transaction=sum_transaction * -1
                if type_transaction.id == 1 and sum_transaction > 0 else sum_transaction, # TODO не дать добавить -1 грн. для Зачисления
                date_of_trans=date_of_trans, user=user)
            new_data.save()

            return render(request, 'grafic_matplotlib/success_input.html', {'confirm': confirm})

    else:
        form_manual_input = ManualInput(request.POST)
        return render(request, 'grafic_matplotlib/manual_input.html', {'form_manual_input': form_manual_input})
