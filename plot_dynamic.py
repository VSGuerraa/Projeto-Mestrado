import csv
import matplotlib.pyplot as plt
import numpy as np
import statistics as st


def read_csv(file_path):
    data = []
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            data.append(row)
    return data


def main():

    batch_size = 4
    sizes = 4
    # Read the CSV file
    file_path = 'Dynamic_alocation_compare.csv'
    data = read_csv(file_path)
    
    tamanho_topologia_full = []
    tamanho_topologia_part = []
    tamanho_topologia_aloc_func = []

    for row in data:
        if row[0][:3] == 'Cha':
            tamanho_topologia_part.append(float(row[1]))
        elif row[0] == 'Full':
            tamanho_topologia_full.append(float(row[1]))
        elif row[0][:3] == 'New':
            tamanho_topologia_aloc_func.append(float(row[1]))
        
        if len(tamanho_topologia_aloc_func) == 480:
            break
        

    # Constants
    n_topos = 3
    n_repeats = 10
    n_sizes = 4
    n_batches = 4

    # Reshape: [topo][repeat][size][batch]
    dataset_part = np.array(tamanho_topologia_part).reshape(n_topos, n_repeats, n_sizes, n_batches)
    dataset_aloc = np.array(tamanho_topologia_aloc_func).reshape(n_topos, n_repeats, n_sizes, n_batches)
    dataset_full = np.array(tamanho_topologia_full).reshape(n_topos, n_repeats)
    
    fig, axs = plt.subplots(3, 1, figsize=(10, 14), sharex=True)
    fig.suptitle("Percentage Difference per Batch between ILPs", fontsize=16)

    colors = ['tab:blue', 'tab:orange', 'tab:green', 'tab:red']
    labels = ['Small Functions', 'Medium Functions', 'Large Functions', 'Equal Functions']

    for topo_idx in range(n_topos):
        ax = axs[topo_idx]
        max_diff = 0  # For per-topology y-axis scaling

        for size_idx in range(n_sizes):
            means_part = dataset_part[topo_idx, :, size_idx, :].mean(axis=0)
            means_aloc = dataset_aloc[topo_idx, :, size_idx, :].mean(axis=0)
            means_full = dataset_full[topo_idx, :].mean(axis=0)

            # Compute percentage difference and avoid divide-by-zero
            diff_percent = np.where(means_aloc != 0,
                                    (means_part - means_aloc) / means_aloc * 100,
                                    0)
            diff_percent = np.insert(diff_percent, 0, 0)
            
            max_diff = max(max_diff, np.max(np.abs(diff_percent)))  # track for axis scaling

            ax.plot(range(1, n_batches+2), diff_percent, '-o', color=colors[size_idx], label=labels[size_idx])

        ax.set_title(f"Topology {(topo_idx+2)*5}")
        ax.set_ylabel("Δ (%)")
        ax.set_xticks(range(1, n_batches+2))
        ax.axhline(0, color='gray', linestyle='--', linewidth=1)
        ax.set_ylim(-max_diff * 0.2, max_diff * 1.2)  # ±20% margin around local max diff

    axs[-1].set_xlabel("Batch")
    axs[0].legend(loc='upper right', bbox_to_anchor=(1.2, 1), ncol=1)

    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.show()
    plt.savefig("Images/Dynamic_alocation_compare.pdf", dpi=300, bbox_inches='tight',format='pdf')






if __name__ == "__main__":
    main()