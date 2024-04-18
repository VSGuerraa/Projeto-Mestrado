import numpy as np
import matplotlib.pyplot as plt

def plot_resource_comparison_ILP(used_thro_ILP, total_thro_ILP, used_thro_ILP_std_dev, total_thro_ILP_std_dev):

    # Define topology sizes
    topology_sizes = np.array([5, 10, 15, 20, 25, 30, 35, 40])
    topology_sizes = topology_sizes[:len(used_thro_ILP)]
    fig, ax = plt.subplots()

    bar_width = 0.8
    opacity = 1

    
    rects1 = ax.bar(topology_sizes - bar_width/2, used_thro_ILP, bar_width,
                    label='Used Throughput', yerr=used_thro_ILP_std_dev,
                    alpha=opacity, color='tab:orange', error_kw=dict(capsize=5))

    rects2 = ax.bar(topology_sizes + bar_width/2, total_thro_ILP, bar_width,
                    label='Total Throughput', yerr=total_thro_ILP_std_dev,
                    alpha=opacity, color='tab:blue', error_kw=dict(capsize=5))


    ax.set_xlabel('Topology Size')
    ax.set_ylabel('Values (Gbps)')
    ax.set_title(f'Comparison of Used and Total Throughput in ILP-aware Placement')
    ax.set_xticks(topology_sizes)
    ax.set_xticklabels([str(size) for size in topology_sizes])
    ax.legend()

    plt.tight_layout()
    plt.savefig(f'Resources_Comparison_ILP_aware_Bars_Throughput.png')
    plt.show()

def plot_resource_comparison_ILP_unaware(used_thro, total_thro, used_thro_std_dev, total_thro_std_dev):

    # Define topology sizes
    topology_sizes = np.array([5, 10, 15, 20, 25, 30, 35, 40])
    topology_sizes = topology_sizes[:len(used_thro)]
    fig, ax = plt.subplots()

    bar_width = 0.8
    opacity = 1

    
    rects1 = ax.bar(topology_sizes - bar_width/2, used_thro_ILP, bar_width,
                    label='Used Throughput', yerr=used_thro_std_dev,
                    alpha=opacity, color='tab:orange', error_kw=dict(capsize=5))

    rects2 = ax.bar(topology_sizes + bar_width/2, total_thro, bar_width,
                    label='Total Throughput', yerr=total_thro_std_dev,
                    alpha=opacity, color='tab:blue', error_kw=dict(capsize=5))


    ax.set_xlabel('Topology Size')
    ax.set_ylabel('Values (Gbps)')
    ax.set_title(f'Comparison of Used and Total Throughput in ILP-unaware Placement')
    ax.set_xticks(topology_sizes)
    ax.set_xticklabels([str(size) for size in topology_sizes])
    ax.legend()

    plt.tight_layout()
    plt.savefig(f'Resources_Comparison_ILP_unaware_Bars_Throughput.png')
    plt.show()
    
    
total_thro_ILP=[1500,  2800,  4100,  5400,  6700,  8000]
used_thro_ILP=[1217,  2325,  3264,  4755,  5441,  6789]
total_thro_ILP_std_dev=[54,  102,  158,  133,  189,  178]
used_thro_ILP_std_dev=[36,  78,  99,  143,  126,  153]

total_thro_ILP_unaware=[1324,  2951,  3862,  6012,  6843,  8447]
used_thro_ILP_unaware=[857,  2136,  2691,  5234,  5347,  7838]
total_thro_ILP_unaware_std_dev=[95,  186,  242,  215,  324,  318]
used_thro_ILP_unaware_std_dev=[122,  137,  274,  233,  197,  301]


plot_resource_comparison_ILP(used_thro_ILP, total_thro_ILP, used_thro_ILP_std_dev, total_thro_ILP_std_dev)
plot_resource_comparison_ILP_unaware(used_thro_ILP_unaware, total_thro_ILP_unaware, used_thro_ILP_unaware_std_dev, total_thro_ILP_unaware_std_dev)