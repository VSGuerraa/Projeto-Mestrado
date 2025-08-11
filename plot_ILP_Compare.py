import csv
import matplotlib.pyplot as plt
import numpy as np
import statistics as st
from matplotlib import gridspec



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
    # Separando os dados em grupos de 10 para cada topologia
    def group(data, size=10):
        return [data[i*size:(i+1)*size] for i in range(3)]
    
    full_groups = group(plot_full)
    fixpos_means_groups = group([x[0] for x in plot_fixpos])
    fixpart_means_groups = group([x[0] for x in plot_fixpart])

    # Cálculo das médias e desvios padrão por topologia
    means_full = [np.mean(g) for g in full_groups]
    std_full = [np.std(g, ddof=0) for g in full_groups]

    means_fixpos = [np.mean(g) for g in fixpos_means_groups]
    std_fixpos = [np.std(g, ddof=0) for g in fixpos_means_groups]

    means_fixpart = [np.mean(g) for g in fixpart_means_groups]
    std_fixpart = [np.std(g, ddof=0) for g in fixpart_means_groups]

    # Dados para o gráfico
    labels = ['10 Nodes', '15 Nodes', '20 Nodes']
    x = np.arange(len(labels))
    width = 0.25

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(x - width, means_full, width, label='Flex', color='tab:green', capsize=5, edgecolor='black')
    ax.bar(x, means_fixpos, width, label='FixPos', color='tab:blue', capsize=5, edgecolor='black')
    ax.bar(x + width, means_fixpart, width, label='FixPart', color='tab:orange', capsize=5, edgecolor='black')

    ax.set_ylabel('Objective Value', fontsize=18)
    ax.set_xlabel('Topology Size', fontsize=16)
    ax.set_xticks(x)
    ax.set_xticklabels(labels, fontsize=16)
    ax.tick_params(axis='y', labelsize=16)
    ax.legend(fontsize=16, loc='upper left')
    ax.set_ylim(0, 1.2 * max(means_full + means_fixpos + means_fixpart))

    #ax.set_title('Average ILP Objective Value per Topology', fontsize=20)

    plt.tight_layout()
    plt.savefig('ILP_Compare_Mean.pdf', format='pdf', bbox_inches='tight')
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