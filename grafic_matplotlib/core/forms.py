from django import forms


class DateInput(forms.DateInput):
    input_type = 'date'


class Calendar(forms.Form):
    date_field_start = forms.DateField(label='С', widget=DateInput)
    date_field_end = forms.DateField(label='по', widget=DateInput)


class CalendarModelForms(forms.Form):

    class Meta:
        widgets = {'date_field_start': DateInput()}
