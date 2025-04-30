import csv
import matplotlib.pyplot as plt
import numpy as np
import statistics as st



def read_csv_data(file_path):
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        data = list(reader)
    return data

def extract_data(data_raw):

    array_fixpos = []
    array_fixpart = []

    plot_full = []
    plot_fixpos = []
    plot_fixpart = []

    count = 0

    for data in data_raw:

        if data[0] == 'Full':
            full = (float(data[1]))
        elif data[0] == 'FixPos':
            array_fixpos.append(float(data[1]))
            count += 1
        elif data[0] == 'FixPart':
            array_fixpart.append(float(data[1]))
            count += 1
        else:
            continue

        if count == 30:
            count = 0

            # Calculate statistics
            mean_fixpos = st.mean(array_fixpos)
            mean_fixpart = st.mean(array_fixpart)
            std_dev_fixpos = st.pstdev(array_fixpos)
            std_dev_fixpart = st.pstdev(array_fixpart)

            plot_full.append(full)
            plot_fixpos.append([mean_fixpos, std_dev_fixpos])
            plot_fixpart.append([mean_fixpart, std_dev_fixpart])

            array_fixpos = []
            array_fixpart = []

    return plot_full, plot_fixpos, plot_fixpart

def plot_data(plot_full, plot_fixpos, plot_fixpart):
    #Extracting means and standard deviations and ploting 3 different figures each 10 times

    means_fixpos = [x[0] for x in plot_fixpos]
    std_dev_fixpos = [x[1] for x in plot_fixpos]
    means_fixpart = [x[0] for x in plot_fixpart]
    std_dev_fixpart = [x[1] for x in plot_fixpart]
    means_full = plot_full

    for idx in range(10,31,10):
        indexes = list(range(1, 11))
        x = np.arange(len(indexes))  # the label locations
        width = 0.25  # the width of the bars
        plt.bar(x - width, means_full[(idx-10):idx], width, label='Full', color='tab:green', capsize=2)
        plt.bar(x, means_fixpos[(idx-10):idx], width, yerr=std_dev_fixpos[(idx-10):idx], label='FixPos', color='tab:blue', capsize=2)
        plt.bar(x + width, means_fixpart[(idx-10):idx], width, yerr=std_dev_fixpart[(idx-10):idx], label='FixPart', color='tab:orange', capsize=2)
    

        plt.xticks(x, indexes)
        plt.legend(fontsize=12)
        plt.ylabel("Values", fontsize=12)
        plt.tick_params(axis='y', labelsize=12)
        plt.ylim(bottom=0) 
        plt.show()
        
def main():
    # Read data from CSV
    data_raw = read_csv_data('ILP_Compare.csv')
    # Extract data from CSV
    plot_full, plot_fixpos, plot_fixpart = extract_data(data_raw)

    # Plot the data
    plot_data(plot_full, plot_fixpos, plot_fixpart)


if __name__ == "__main__":
    main()