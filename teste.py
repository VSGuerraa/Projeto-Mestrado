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
    plt.ylabel("Mean Value (%) - Resource Related")
    plt.title('Invalid Allocations')

    # Show the plot
    plt.show()
    plt.savefig('Invalid_ratio.png')


import matplotlib.pyplot as plt


def plot_ILP_value(dataset_ILP_ciente, dataset_std_ILP_ciente, dataset_ILP_naociente, dataset_std_ILP_naociente):
    fig = plt.figure() 
    ax = fig.add_subplot(111) 
    nodes = [5,10,15,20,25,30,35,40]
    nodes = nodes[:len(dataset_ILP_ciente)]
    
    # Plot for ciente
    ax.errorbar(nodes, dataset_ILP_ciente, yerr=dataset_std_ILP_ciente, fmt='-o', color='tab:green', label='Aware')
    
    # Plot for naociente
    ax.errorbar(nodes, dataset_ILP_naociente, yerr=dataset_std_ILP_naociente, fmt='-o', color='tab:red', label='Unaware')
    ax.set_ylim(bottom=0)  # Set the starting point of y-axis to 0
    ax.grid() 
    ax.set_xlabel("Nodes") 
    ax.set_ylabel("Mean Value - Resource Related") 
    ax.legend()  # Add a legend
    
    plt.savefig('Grafico_ILP.png')
    plt.show()
    

#call the function
    
mean_ilp_ciente = [489.2,859.1, 1252.900000091183,1798.6, 2354.3, 2351.5]
std_ilp_ciente = [175.09357498206495,258.81767713971936, 301.00529893520184, 392.80636451055625, 451.45864705419035,369.97939131794897]
mean_ilp_naociente = [612.1,1215.3,1582.7000001814554,2312.5,2767.0,2907.5]
std_ilp_naociente = [186.51056270356378,368.6463210178558,419.1874403005365,484.7147099067657,521.7740890462078,270.09211391671545]

mean_values = {
    "5": [0.06611989420434235],
    "10": [0.053243040743658133],
    "15": [0.034450248211283944],
    "20": [0.0489234464783541],
    "25": [0.03130609064601918],
    "30": [0.03205885855229854]
}

std_dev_values = {
    "5": [0.04523750118623533],
    "10": [0.033218236037810885],
    "15": [0.021519950093666532],
    "20": [0.025038558080973196],
    "25": [0.017878967703590837],
    "30": [0.012928403073412576]
}


plot_graph(mean_values, std_dev_values)
#plot_ILP_value(mean_ilp_ciente, std_ilp_ciente, mean_ilp_naociente, std_ilp_naociente)