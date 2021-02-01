from decimal import Decimal

import matplotlib.pyplot as plt
import base64
from io import BytesIO
from matplotlib.lines import Line2D

from grafic_matplotlib.analytics.query_data import sum_expenses

#тест
def test_figure():
    figure, ax = plt.subplots()
    ax.plot([1, 3, 4, 6, 8], [3, 2, 5, 10, 8])
    return figure


#статический пирог в админке джанго
def pie_figure(s_day='2020-10-01', e_day='2020-10-20'):
    data = sum_expenses(start=s_day, end=e_day)
    labels = []
    sizes = []

    for i in data:
        labels.append(i['type_expenses_ru'])
        sizes.append(i['total_amount'])

   #explode = (0, 0.1, 0, 0, 0, 0, 0, 0, 0, 0, 0)  # only "explode" the 2nd slice (i.e. 'Hogs')

    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, labels=labels, autopct='%1.1f%%',
            shadow=False, startangle=120)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    return fig1


#статическая диаграмма в админке джанго
def line_chart():
    cmap = plt.cm.coolwarm

    custom_lines = [Line2D([0], [0], color=cmap(0.), lw=4),
                    Line2D([0], [0], color=cmap(.5), lw=4),
                    Line2D([0], [0], color=cmap(1.), lw=4)]

    fig, ax = plt.subplots()
    ax.set_xlabel('$mounth$')
    ax.set_ylabel('$amount$')
    ax.plot([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], [3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], [2, 3.5, 3.5, 3, 4, 4, 3, 2, 3.5, 3.5, 3, 4],
            [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], [5, 6, 5, 8, 7, 5, 6, 7.5, 8.2, 8.8, 9, 8.5]
            )
    ax.legend(custom_lines, ['Cold', 'Medium', 'Hot'])
    return fig


#интерактивный вывод пирога
def get_pie():
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    graph = base64.b64encode(image_png)
    graph = graph.decode('utf-8')
    buffer.close()

    return graph


def get_plot(s_day, e_day):
    plt.switch_backend('AGG')

    data = sum_expenses(start=s_day, end=e_day)
    labels = []
    sizes = []

    for i in data:
        labels.append(i['type_expenses_ru'])
        sizes.append(i['total_amount'])

    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, labels=labels, autopct='%1.1f%%',
            shadow=False, startangle=120)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    graph = get_pie()

    return graph

