from django.shortcuts import render
from django.http import HttpResponse

from grafic_matplotlib.figures import pie
from grafic_matplotlib.models import Pie


def index(request):
    return render(request, 'grafic_matplotlib/analytics.html', {})


def index_p(request):
    pie_view = pie()

    return render(request, 'grafic_matplotlib/pie.html',
                  context={'index_p': pie_view})


def index_d(request):
    return render(request, 'grafic_matplotlib/diagram.html', {})


def index_plan(request):
    return render(request, 'grafic_matplotlib/planning.html', {})
