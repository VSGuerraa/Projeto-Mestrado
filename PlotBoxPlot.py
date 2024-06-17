import matplotlib.pyplot as plt
import numpy as np
import csv
import statistics as st

with open('data_raw.csv', 'r') as file:
    reader = csv.reader(file)
    data = list(reader)
    
values_box = []

for graph in range(int(len(data)/101)):
    graph *= 101
    results = []     
    for i in range(graph, graph + 100):
        results.append(float(data[i][-13]))
    results.sort()          
    values_box.append(results)
    
        
# Create a boxplot
plt.figure(figsize=(12, 6))
plt.boxplot(values_box, vert=True, patch_artist=True)
plt.tick_params(axis='y', labelsize=16)
plt.tick_params(axis='x', labelsize=16)

# Set title and labels

plt.xlabel('Topologies', fontsize=18)
plt.ylabel('Values', fontsize=18)
plt.ylim(0, 800)

# Show the plot
plt.grid()
plt.savefig('boxplot_general.pdf', format='pdf')

with open('data_BestWorst.csv', 'r') as file:
    reader = csv.reader(file)
    data = list(reader)


values_bars = []

for graph in range(int(len(data)/101)):
    graph *= 101
    if graph > 6000:
        break
    results = []    
    for i in range(graph, graph + 100):
        results.append(float(data[i][-13]))
    results.sort()          
    values_bars.append(results)


mean_array = []
stdev_array = []
mean_values = []
stdev_values = []    
for index in range(len(values_bars)):
    mean_array.append(st.mean(values_bars[index]))
    stdev_array.append(st.stdev(values_bars[index]))
    if index != 0 and (index + 1) % 3 == 0:
        mean_values.append(st.mean(mean_array))
        stdev_values.append(st.mean(stdev_array))
        mean_array = []
        stdev_array = []     
        
fix_part_mean = []
fix_pos_mean = []
fix_part_stdev = []
fix_pos_stdev = []

for index in range(len(mean_values)):
    if index % 2 == 0:
        fix_part_mean.append(mean_values[index])
        fix_part_stdev.append(stdev_values[index])
    else:
        fix_pos_mean.append(mean_values[index])
        fix_pos_stdev.append(stdev_values[index])
        
top3 = []
bottom3 = []        
for i in range(len(values_box)):
    top3.append(st.mean(values_box[i][-3:]))
    bottom3.append(st.mean(values_box[i][:3]))

dataset_mean = [st.mean(fix_part_mean), 502.54,  st.mean(top3),  st.mean(bottom3), 482.79,  st.mean(fix_pos_mean)]
dataset_stdev = [st.mean(fix_part_stdev), 65.02, st.stdev(top3), st.stdev(bottom3), 59.41, st.mean(fix_pos_stdev)]
labels = ['Fix Part', 'Fix Pos', 'Ref Top 3', 'Ref Bottom 3' ,'Fix Part', 'Fix Pos']
indexes = list(range(len(labels)))

plt.figure(figsize=(22, 6))
plt.bar(indexes,dataset_mean, yerr=dataset_stdev, color='tab:green', capsize=2, width=0.5) 
for spine in plt.gca().spines.values():
    spine.set_linewidth(2)
plt.xticks(indexes, labels, fontsize=32)
plt.ylabel("Values", fontsize=30)
plt.tick_params(axis='y', labelsize=22)
plt.ylim(bottom=0) 

plt.savefig('Comparison_Values_Variation.pdf', format='pdf')