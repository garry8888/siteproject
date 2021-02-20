from django import forms


# загрузка данных с гуглдок
class UrlForm(forms.URLInput):
    input_type = 'url'


class SheetNumber(forms.NumberInput):
    input_type = 'int'


class UrlInput(forms.Form):
    url_field = forms.URLField(label='Введите URL', widget=UrlForm)
    sheet_number = forms.IntegerField(label='Введите номер страницы', widget=SheetNumber)
