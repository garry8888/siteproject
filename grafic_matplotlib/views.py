from django.shortcuts import render
from grafic_matplotlib.models import Pie, Diagram


def index(request):
    return render(request, 'grafic_matplotlib/analytics.html', {})


def index_p(request):
    pie_p = Pie.figure.source

    return render(request, 'grafic_matplotlib/pie.html', {'pie_fig': pie_p})


def index_d(request):
    diagram = Diagram.figure.source

    return render(request, 'grafic_matplotlib/diagram.html', {'diagram_fig': diagram})


def index_plan(request):
    return render(request, 'grafic_matplotlib/planning.html', {})
