from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column
from django import forms
from django.contrib.auth.models import User


# Календарь
from finance.models import BankStatements


class DateInput(forms.DateInput):
    input_type = 'date'


class Calendar(forms.Form):
    date_field_start = forms.DateField(label='', widget=DateInput)
    date_field_end = forms.DateField(label='', widget=DateInput)


class CalendarModelForms(forms.Form):

    class Meta:
        widgets = {'date_field_start': DateInput()}


# выбор пользователя для отображения данных
class UserInput(forms.CheckboxSelectMultiple):
    input_type = 'checkbox'
    # template_name = 'django/forms/widgets/checkbox_select.html'
    # option_template_name = 'django/forms/widgets/checkbox_option.html'


class UserChoice(forms.Form):
    user_field = forms.ModelMultipleChoiceField(label='', queryset=User.objects.all(), widget=UserInput)

    class Meta:
        widgets = {'user_field': UserInput()}


# ручной ввод расходов
class ManualInput(forms.Form):
    query = BankStatements.objects.all()
    transaction_place = forms.CharField(label='Место', widget=forms.TextInput)
    type_expenses = forms.ModelMultipleChoiceField(label='Тип расходов',
                                                   queryset=query,
                                                   widget=forms.Select)
    type_transaction = forms.ModelMultipleChoiceField(label='Тип транзакции',
                                                      queryset=query, widget=forms.Select)


# выбор года для гистограммы
class YearInput(forms.Select):
    input_type = 'select'


class ChoiceYear(forms.Form):
    years = [('2020', '2020'), ('2021', '2021')]
    year_field = forms.ChoiceField(
        label='',
        required=False,
        widget=YearInput,
        choices=years,
    )
