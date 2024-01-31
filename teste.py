import matplotlib.pyplot as plt
import numpy as np

def plot_graph(mean_values, std_dev_values):
    # Convert the keys and values to lists for plotting
    x = list(map(int, mean_values.keys()))
    y = [val[0] for val in mean_values.values()]
    yerr = [val[0] for val in std_dev_values.values()]

    # Create the plot
    plt.figure()
    plt.grid()
    plt.plot(x, y, 'o-', color='red')
    plt.errorbar(x, y, yerr=yerr, fmt='o', color='black',
                 ecolor='red', elinewidth=1, capsize=1)

    # Add labels
    plt.xlabel('Number of Nodes')
    plt.ylabel('Mean Values')
    plt.title('Invalid Allocations')

    # Show the plot
    plt.show()
    plt.savefig('Invalid_ratio.png')

mean_values = {
    "5": [0.021610664067324755],
    "10": [0.028862386808896887],
    "15": [0.016624158977507894],
    "20": [0.013919379310163835],
    "25": [0.015179314825087577],
    "30": [0.030556742196120246]
}

std_dev_values = {
    "5": [0.04266902133723109],
    "10": [0.03959859762699004],
    "15": [0.019321821843933114],
    "20": [0.02106847355296831],
    "25": [0.020581015915324536],
    "30": [0.026956570715675157]
}

plot_graph(mean_values, std_dev_values)