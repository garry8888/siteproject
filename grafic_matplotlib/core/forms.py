from django import forms
from django.contrib.auth.models import User


#Календарь
from finance.models import BankStatements


class DateInput(forms.DateInput):
    input_type = 'date'


class Calendar(forms.Form):
    date_field_start = forms.DateField(label='С', widget=DateInput)
    date_field_end = forms.DateField(label='по', widget=DateInput)


class CalendarModelForms(forms.Form):

    class Meta:
        widgets = {'date_field_start': DateInput()}


#выбор пользователя для отображения данных
class UserInput(forms.CheckboxSelectMultiple):
    input_type = 'checkbox'
    #template_name = 'django/forms/widgets/checkbox_select.html'
    #option_template_name = 'django/forms/widgets/checkbox_option.html'


class UserChoice(forms.Form):
    user_field = forms.ModelMultipleChoiceField(label='Пользователи', queryset=User.objects.all(), widget=UserInput)

    class Meta:
        widgets = {'user_field': UserInput()}


#выбор года для гистограммы
class YearInput(forms.Select):
    input_type = 'select'


class ChoiceYear(forms.Form):
    years = [('2020', '2020'), ('2021', '2021')]
    year_field = forms.ChoiceField(
        label='Год',
        required=False,
        widget=YearInput,
        choices=years,
    )
