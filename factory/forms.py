from django import forms


# загрузка данных с гуглдок
from django.forms import ModelForm

from factory.models import Document
from finance.models import Bank


class UrlForm(forms.URLInput):
    input_type = 'url'


class SheetNumber(forms.NumberInput):
    input_type = 'int'


class UrlInput(forms.Form):
    url_field = forms.URLField(label='Введите URL', widget=UrlForm)
    sheet_number = forms.IntegerField(label='Введите номер страницы', widget=SheetNumber)


# загрузка данных из PDF файла
class PdfForm(ModelForm):
    class Meta:
        model = Document
        fields = ('bank', 'description', 'document', )


"""
class PdfForm(forms.FileInput):
    input_type = 'file'


class FileInput(forms.Form):
    file_field = forms.FileField(label='Введите файл', widget=PdfForm)
"""
