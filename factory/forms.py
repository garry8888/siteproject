from django import forms


class UrlForm(forms.URLInput):
    input_type = 'url'


class SheetNumber(forms.NumberInput):
    input_type = 'int'


class UrlInput(forms.Form):
    url_field = forms.URLField(widget=UrlForm)
    sheet_number = forms.IntegerField(widget=SheetNumber)
