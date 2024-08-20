import random
import math
import gerador_topologia as gt
import ILP_ciente as ilp_solver
import time
import Projeto
import json

def simulated_annealing(initial_temperature, cooling_rate, stopping_temperature, fixed_parameter=None, initial_solution = None):

    current_solution = initial_solution
    current_value = objective_function()
    best_value = current_value[0]
    current_value = current_value[0]
    
    temperature = initial_temperature
    
    while temperature > stopping_temperature:
        
        if fixed_parameter == 1:
            scrumble_positioning()
        elif fixed_parameter == 2:
            scrumble_partitioning()
        else:
            neighbor_function(current_solution)
            
        local_result = objective_function()
        neighbor_value = local_result[0]
        
        delta = neighbor_value - current_value
        acceptance_probability = math.exp(-delta / temperature) if delta > 0 else 1.0
        
        if random.random() < acceptance_probability:
            current_value = neighbor_value
            
            # Update the best solution found
            if current_value >= best_value:
                best_value = current_value
                
                with open('topologia.json', 'r', encoding='utf-8') as file:
                    data = file.read()
                
                with open('topologia_bestvalue.json', 'w', encoding='utf-8') as file:
                    file.write(data)
        
        # Cool down the temperature
        temperature *= cooling_rate
    
    return  best_value

def objective_function():
    value = ilp_solver.main()
    return value

def neighbor_function(current_solution = None):
    if current_solution is None:
        with open('topologia.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
        nr_nodos = len(data)
    else:
        nr_nodos = len(list(current_solution.nodes))
    nr_links = nr_nodos * 1.3
    neighbor_solution = gt.gerador_Topologia(nr_nodos, nr_links, current_solution)
    return neighbor_solution
    
    
def scrumble_positioning():
    with open('topologia.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
    nodes_with_fpga = []    
    for index_node,node in enumerate(data.values()):
        if node['FPGA'] == []:
            continue
        else:
            nodes_with_fpga.append(index_node)
        
    new_sort_fpga = random.sample(range(len(data)), len(nodes_with_fpga))
    fpgas_to_remove = [value for value in nodes_with_fpga if value not in new_sort_fpga]
    
    for fpga in new_sort_fpga:
        for index_node, node in enumerate(data.values()):
            if index_node == fpga:
                data[f'Nodo{fpga}']['FPGA'] = data[f'Nodo{nodes_with_fpga[0]}']['FPGA']
                nodes_with_fpga.pop(0)
    for index_node, node in enumerate(data.values()):
        if index_node in fpgas_to_remove:
            node["FPGA"] = []
    
    with open('topologia.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4)

def scrumble_partitioning():
   
    fpga_M=[
            {   "Modelo": 'M',
                "Part0": {
                        "CLBs": 19200,
                        "BRAM": 480,
                        "DSP": 192
                    },
                    "Part1": {
                        "CLBs": 20160,
                        "BRAM": 480,
                        "DSP": 192
                    },
                    "Part2": {
                        "CLBs": 10440,
                        "BRAM": 288,
                        "DSP": 144
                    },
                    
                    "Part3": {
                        "CLBs": 3060,
                        "BRAM": 108,
                        "DSP": 0
                    },
                    "Part4": {
                        "CLBs": 3060,
                        "BRAM": 144,
                        "DSP": 72
                    },
                    "Part5": {
                        "CLBs": 3060,
                        "BRAM": 72,
                        "DSP": 72
                    }
            },
            {   "Modelo": 'M',
                "Part0": {
                        "CLBs": 10800,
                        "BRAM": 240,
                        "DSP": 96
                    },
                    "Part1": {
                        "CLBs": 10440,
                        "BRAM": 288,
                        "DSP": 144
                    },
                    "Part2": {
                        "CLBs": 10800,
                        "BRAM": 300,
                        "DSP": 144
                    },
                    "Part3": {
                        "CLBs": 10800,
                        "BRAM": 300,
                        "DSP": 96,
                    },
                    "Part4": {
                        "CLBs": 10440,
                        "BRAM": 240,
                        "DSP": 96
                    },
                    "Part5": {
                        "CLBs": 10800,
                        "BRAM": 300,
                        "DSP": 144
                    },
                    "Part6": {
                        "CLBs": 10800,
                        "BRAM": 300,
                        "DSP": 72
                    }
                
            },
            {   "Modelo": 'M',
                "Part0": {
                        "CLBs": 20160,
                        "BRAM": 480,
                        "DSP": 192
                    },
                "Part1": {
                        "CLBs": 10440,
                        "BRAM": 288,
                        "DSP": 144
                    },
                "Part2": {
                        "CLBs": 10800,
                        "BRAM": 300,
                        "DSP": 144
                    },
                "Part3": {
                        "CLBs": 3060,
                        "BRAM": 108,
                        "DSP": 0
                    },
                "Part4": {
                        "CLBs": 3060,
                        "BRAM": 144,
                        "DSP": 72
                    },
                "Part5": {
                        "CLBs": 3060,
                        "BRAM": 72,
                        "DSP": 72
                    },
                "Part6": {
                        "CLBs": 3060,
                        "BRAM": 108,
                        "DSP": 0
                    },
                "Part7": {
                        "CLBs": 3060,
                        "BRAM": 144,
                        "DSP": 72
                    }     
            }             
            ]
    
    with open('topologia.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
        
    for index_node,node in enumerate(data.values()):
        if node['FPGA'] != []:
            new_fpga=random.choice(fpga_M)
            list_fpga = [new_fpga]
            list_aux = [list_fpga]
            data[f'Nodo{index_node}']['FPGA'] = list_aux
                
    with open('topologia.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4)
    
def main():
    
    init_time = time.time()
    
    nr_nodos = 20
    nr_links = int(nr_nodos * 1.3)
    Projeto.gerador_Req(nr_nodos, nr_nodos*6)
    
    initial_solution = gt.gerador_Topologia(nr_nodos, nr_links)
    
    # Parameters for simulated annealing
    initial_temperature = 15000
    cooling_rate = 0.9999
    stopping_temperature = 1e-10
    
    # Run simulated annealing
    best_value = simulated_annealing(initial_temperature, cooling_rate, stopping_temperature, initial_solution)
    final_solution = ilp_solver.main(True)
    print(f"Best value Greedy: {best_value}")
    print(f"Final solution ILP: {final_solution[0]}")
    
    end_time = time.time()
    total_time = end_time - init_time
    print("Execution time: ", total_time)
    
    return best_value, final_solution[0], total_time
    

if __name__ == "__main__":
    results = []
    for i in range(10):
        results.append(main())
    print(results)
        