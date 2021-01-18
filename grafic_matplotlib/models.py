from django.db import models
from django_matplotlib import MatplotlibFigureField


class Diagram(models.Model):
    figure = MatplotlibFigureField(figure='test_figure')


class Pie(models.Model):
    figure = MatplotlibFigureField(figure='pie')


class Line(models.Model):
    figure = MatplotlibFigureField(figure='line_chart')
