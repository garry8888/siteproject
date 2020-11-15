from django.shortcuts import render
from django.http import HttpResponse

from grafic_matplotlib.figures import pie
from grafic_matplotlib.models import Pie


def index(request):
    return render(request, 'grafic_matplotlib/analytics.html', {})


def index_p(request):
    pie_view = pie()

    return render(request, 'grafic_matplotlib/pie.html',
                  context={'pie': pie_view})

    """
    pie_view = Pie.objects.all()

    return render(request, 'grafic_matplotlib/pie.html',
                  context={'pie': [view.figure for view in pie_view]})
    """

