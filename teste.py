import statistics
import csv

# Read data_random_ilp.csv and calculate the average of the values and the standard deviation from the -13th column

# Open the file data_random_ilp.csv
with open('data_compare_heuristic.csv', 'r') as csv_file:
    csv_reader = csv.reader(csv_file)
    csv_data = list(csv_reader)
    
    fix_pos =[]
    fix_part = []
    sim_aneal = []
    remove_index = []
    data = []
    
    for row in range(len(csv_data)):
        if 'Id' in csv_data[row][0]:
            remove_index.append(row)
        
    remove_index = sorted(remove_index, reverse=True)
    for index in remove_index:
        csv_data.pop(index)
        
    for row in range(len(csv_data)):
        data.append(csv_data[row][-13])
    
    for i in range(0, len(data), 10):
        print(data[i:i+10])
      
    for row in range(0,len(csv_data),30):
        fix_part.extend(csv_data[row:row+10])
        fix_pos.extend(csv_data[row+10:row+20])
        sim_aneal.extend(csv_data[row+20:row+30])
        
    for i in range(len(fix_pos)):
        fix_part[i] = float(fix_part[i][-13])
        fix_pos[i] = float(fix_pos[i][-13])
        sim_aneal[i] = float(sim_aneal[i][-13])
            
    for i in range(0, len(fix_pos), 10):
        position = sorted(fix_pos[i:i+10])
        partition = sorted(fix_part[i:i+10])
        simulated = sorted(sim_aneal[i:i+10])
        
        mean_position = statistics.mean(position)
        mean_partition = statistics.mean(partition)
        mean_simulated = statistics.mean(simulated)
        std_position = statistics.stdev(position)
        std_partition = statistics.stdev(partition)
        std_simulated = statistics.stdev(simulated)
        
        
        print(f'Fix Partitioning: {partition}, Mean: {mean_partition}, Std Dev: {std_partition:.3}')
        print(f'Fix Positioning: {position}, Mean: {mean_position}, Std Dev: {std_position:.3}')
        print(f'Simulated Annealing: {simulated}, Mean: {mean_simulated}, Std Dev: {std_simulated:.3}\n')
        
    

            