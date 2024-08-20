import time
import gerador_topologia
import Heuristic
import json
import csv
import ILP_ciente as ILP
import Projeto

def main():
    
    nr_topologies = 5 #50
    
    for _ in range(nr_topologies):
        
        init_time = time.time()

        nr_nodos = 20
        nr_links = int(nr_nodos * 1.3)
        gerador_topologia.gerador_Topologia(nr_nodos, nr_links,initial=True)
        Projeto.gerador_Req(nr_nodos, nr_nodos*6)
        
        SA_run_fix_part=1
        SA_run_fix_pos=2
        
        # Parameters for simulated annealing
        initial_temperature = 10000
        cooling_rate = 0.9
        stopping_temperature = 1e-7
        
        shakes = 10 #50
                
        for shake in range(shakes):
            
            # Run simulated annealing varying the the position of the FPGAs and fixing the partition
            best_value_position = Heuristic.simulated_annealing(initial_temperature, cooling_rate, stopping_temperature,SA_run_fix_part)

            result_ILP_ciente,time_ILP_ciente, resources_model_ILP, req_allocated_ILP_aware = ILP.main(True)
            csv_row = []
            
            with open('topologia.json', 'r') as json_file:
                topologia = json.load(json_file)

            for _, node_data in topologia.items():
                resource = node_data['FPGA']
                csv_row.append(resource) 
                link = node_data['Links']
                csv_row.append(link)
            
            with open('data_compare_heuristic.csv', 'a+', newline='') as csv_file:
                writer = csv.writer(csv_file)
                
                csv_row.append(result_ILP_ciente)
                csv_row.append(time_ILP_ciente)
                csv_row.append(resources_model_ILP[0])
                csv_row.append(resources_model_ILP[1])
                csv_row.append(resources_model_ILP[2])
                csv_row.append(resources_model_ILP[3])
                csv_row.append(resources_model_ILP[4])
                csv_row.append(resources_model_ILP[5])
                csv_row.append(resources_model_ILP[6])
                csv_row.append(resources_model_ILP[7])
                csv_row.append(resources_model_ILP[8])
                csv_row.append(resources_model_ILP[9])
                csv_row.append(req_allocated_ILP_aware)
                                    
                writer.writerow(csv_row)
            
            Heuristic.scrumble_partitioning()
        
        with open('requisicoes.json', 'r') as json_file:
            req = json.load(json_file)  
            csv_row = []
            for req, req_data in req.items():
                csv_row.append(req_data)
            
        with open('data_compare_heuristic.csv', 'a+', newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(csv_row)
                
        with open('topologia_initial.json', 'r') as json_file:
            initial_solution = json.load(json_file)
        
        with open('topologia.json', 'w') as json_file:
            json.dump(initial_solution, json_file)
        
        for shake in range(shakes):
            
            # Run simulated annealing varying the the partition of the FPGAs and fixing the position
            best_value_partition = Heuristic.simulated_annealing(initial_temperature, cooling_rate, stopping_temperature,SA_run_fix_pos)
            
            result_ILP_ciente,time_ILP_ciente, resources_model_ILP, req_allocated_ILP_aware = ILP.main(True)
            csv_row = []
            
            with open('topologia.json', 'r') as json_file:
                topologia = json.load(json_file)

            for _, node_data in topologia.items():
                resource = node_data['FPGA']
                csv_row.append(resource) 
                link = node_data['Links']
                csv_row.append(link)
            
            with open('data_compare_heuristic.csv', 'a+', newline='') as csv_file:
                writer = csv.writer(csv_file)
                
                csv_row.append(result_ILP_ciente)
                csv_row.append(time_ILP_ciente)
                csv_row.append(resources_model_ILP[0])
                csv_row.append(resources_model_ILP[1])
                csv_row.append(resources_model_ILP[2])
                csv_row.append(resources_model_ILP[3])
                csv_row.append(resources_model_ILP[4])
                csv_row.append(resources_model_ILP[5])
                csv_row.append(resources_model_ILP[6])
                csv_row.append(resources_model_ILP[7])
                csv_row.append(resources_model_ILP[8])
                csv_row.append(resources_model_ILP[9])
                csv_row.append(req_allocated_ILP_aware)
                                    
                writer.writerow(csv_row)
            
            Heuristic.scrumble_positioning()
        
        with open('requisicoes.json', 'r') as json_file:
            req = json.load(json_file)  
            csv_row = []
            for req, req_data in req.items():
                csv_row.append(req_data)
            
        with open('data_compare_heuristic.csv', 'a+', newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(csv_row)
        
            
        with open('topologia_initial.json', 'r') as json_file:
            initial_solution = json.load(json_file)
        
        with open('topologia.json', 'w') as json_file:
            json.dump(initial_solution, json_file)
        
        for shake in range(shakes):
            
            # Run simulated annealing varying the the partition of the FPGAs and fixing the position
            best_value_partition = Heuristic.simulated_annealing(initial_temperature, cooling_rate, stopping_temperature)
            
            result_ILP_ciente,time_ILP_ciente, resources_model_ILP, req_allocated_ILP_aware = ILP.main(True)
            csv_row = []
            
            with open('topologia.json', 'r') as json_file:
                topologia = json.load(json_file)

            for _, node_data in topologia.items():
                resource = node_data['FPGA']
                csv_row.append(resource) 
                link = node_data['Links']
                csv_row.append(link)
            
            with open('data_compare_heuristic.csv', 'a+', newline='') as csv_file:
                writer = csv.writer(csv_file)
                
                csv_row.append(result_ILP_ciente)
                csv_row.append(time_ILP_ciente)
                csv_row.append(resources_model_ILP[0])
                csv_row.append(resources_model_ILP[1])
                csv_row.append(resources_model_ILP[2])
                csv_row.append(resources_model_ILP[3])
                csv_row.append(resources_model_ILP[4])
                csv_row.append(resources_model_ILP[5])
                csv_row.append(resources_model_ILP[6])
                csv_row.append(resources_model_ILP[7])
                csv_row.append(resources_model_ILP[8])
                csv_row.append(resources_model_ILP[9])
                csv_row.append(req_allocated_ILP_aware)
                                    
                writer.writerow(csv_row)
            
            Heuristic.neighbor_function()
        
        with open('requisicoes.json', 'r') as json_file:
            req = json.load(json_file)  
            csv_row = []
            for req, req_data in req.items():
                csv_row.append(req_data)
            
        with open('data_compare_heuristic.csv', 'a+', newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(csv_row)
            
        end_time = time.time()
        print('Execution time:', end_time - init_time)
                

if __name__ == '__main__':
    main()
        