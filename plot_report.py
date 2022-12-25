import matplotlib.pyplot as plt
import numpy as np


def plot_pie(d):
    plt.style.use('_mpl-gallery-nogrid')

    # make data
    x = []
    labels = []
    for k, v in d.items():

        x.append(v)
        labels.append(k)

    colors = plt.get_cmap('Purples')(np.linspace(0.2, 0.7, len(x)))

    # plot
    fig, ax = plt.subplots()
    ax.pie(x, colors=colors, radius=3, center=(4, 4), labels=labels,
           wedgeprops={"linewidth": 1, "edgecolor": "white"}, frame=True)

    ax.set(xlim=(0, 8), xticks=np.arange(1, 8),
           ylim=(0, 8), yticks=np.arange(1, 8))

    plt.show()


def plot_bar(d, month, year):

    # x-coordinates of left sides of bars
    left = [1, 2, 3, 4]
    height = []
    labels = []

    for k, v in d.items():

        height.append(v)
        labels.append(k)

    # plotting a bar chart
    plt.bar(left, height, tick_label=labels,
            width=0.8, color=['purple', 'orange'])

    # naming the x-axis
    plt.xlabel('Classes')
    # naming the y-axis
    plt.ylabel('Attendance')
    # plot title
    plt.title('{}/{} Monthly Report'.format(year, month))

    plt.yticks(list(range(1, 6)))

    # function to show the plot
    plt.show()
