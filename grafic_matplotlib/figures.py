from decimal import Decimal

import matplotlib.pyplot as plt

from grafic_matplotlib.analytics.query_data import sum_expenses


def test_figure():
    figure, ax = plt.subplots()
    ax.plot([1, 3, 4, 6, 8], [3, 2, 5, 10, 8])
    return figure


def pie():
    data = sum_expenses()
    labels = []
    sizes = []

    for i in data:
        labels.append(i['type_expenses_ru'])
        sizes.append(i['total_amount'])

   #explode = (0, 0.1, 0, 0, 0, 0, 0, 0, 0, 0, 0)  # only "explode" the 2nd slice (i.e. 'Hogs')

    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, labels=labels, autopct='%1.1f%%',
            shadow=False, startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    return fig1
