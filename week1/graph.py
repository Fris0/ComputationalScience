"""
Author: Mark Jansen (13385569)

This file is used to plot the data obtained from running simulate.py and simulate_random.py
with different parameters.
"""


import matplotlib.pyplot as plt
import numpy as np
import csv

data_files = ["low_width.csv", "mid_width.csv", "high_width.csv", "random_result.csv"]  # Names depends on choice of {name}.csv file name.
data = []

for file_name in data_files:
    reader = csv.reader(open(file_name, 'r'), delimiter=',')
    temp = None

    for row in reader:
        temp = row

    data.append(list(map(float, temp[:-1])))

low_width, mid_width, high_width, data_random = data

x = [i for i in range(0, 256)]

plt.scatter(x, low_width, c="red", label="Width: 25", s=10)
plt.scatter(x, mid_width, c="green", label="Width: 50", s=10)
plt.scatter(x, high_width, c="blue", label="Width: 75", s=10)
plt.xlabel("Rule")
plt.ylabel("Avg Cycle")
plt.title("Average Cycles With Different Widths")
plt.legend()
plt.savefig('avg_cycles_width.png', dpi=300)

plt.clf()  # Clear the current figure.

plt.scatter(x, mid_width, c="red", label="Random: False", s=10)
plt.scatter(x, data_random, c="blue", label="Random: True", s=10)
plt.xlabel("Rule")
plt.ylabel("Avg Cycles")
plt.title("Average Cycles None Random vs Random")
plt.legend()
plt.savefig('avg_cycles_random.png', dpi=300)


fig, ax = plt.subplots(1, 2, figsize=(12, 7))


zeros = [[low_width.count(0), mid_width.count(0), high_width.count(0)], [mid_width.count(0), data_random.count(0)]]

bar_labels_width = ['Width Small (25)', 'Width Medium (50)', 'Width Large (75)']
bar_colors_width = ['tab:red', 'tab:blue', 'tab:red']

bar_labels_random = ['None Random', 'Random Large']
bar_colors_random = ['tab:red', 'tab:blue']

ax[0].bar(bar_labels_width, zeros[0], label=bar_labels_width, color=bar_colors_width)
ax[1].bar(bar_labels_random, zeros[1], label=bar_labels_random, color=bar_colors_random)

ax[0].set_ylabel('Number of rules without cycle')
ax[1].set_ylabel('Number of rules without cycle')

ax[0].set_title('Number of Rules Without Cycle (Width)')
ax[1].set_title('Number of Rules Without Cycle (Random = True / False)')

ax[0].legend()
ax[1].legend()

plt.tight_layout()
plt.savefig('error_plot.png', dpi=300)