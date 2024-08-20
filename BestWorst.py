import csv
import random
import statistics as st
import pickle
import gerador_topologia as gt
import ILP_ciente as ILP
import json
import ast


def scrumble_positioning(graph):
    sortingNodes = []
    
    for index in range(0,len(graph),2):
        sortingNodes.append(graph[index])
            
    random.shuffle(sortingNodes)
    for index in range(0,len(graph),2):
        graph[index] = sortingNodes[index//2]

    return graph

def scrumble_partitioning(graph):
    
    fpga_P=[
                {   "Modelo": 'P',
                    
                    "Part0": {
                        "CLBs": 22200,
                        "BRAM": 480,
                        "DSP": 1560
                    }
                },
                {   "Modelo": 'P',   
                
                    "Part0": {
                        "CLBs": 10800,
                        "BRAM": 300,
                        "DSP": 600
                    },
                    "Part1": {
                        "CLBs": 10800,
                        "BRAM": 180,
                        "DSP": 600
                    },
                    "Part2": {
                        "CLBs": 2958,
                        "BRAM": 40,
                        "DSP": 240
                    }
                },
                {
                    "Modelo": 'P',
                    
                    "Part0": {
                        "CLBs": 3360,
                        "BRAM": 96,
                        "DSP": 192
                    },
                    "Part1": {
                        "CLBs": 5040,
                        "BRAM": 144,
                        "DSP": 288
                    },
                    "Part2": {
                        "CLBs": 5400,
                        "BRAM": 72,
                        "DSP": 432
                    },
                    "Part3": {
                        "CLBs": 5040,
                        "BRAM": 108,
                        "DSP": 216
                    },
                    "Part4": {
                        "CLBs": 3360,
                        "BRAM": 72,
                        "DSP": 144
                    },
                    "Part5": {
                        "CLBs": 2700,
                        "BRAM": 36,
                        "DSP": 216
                    }
                } 
            ]  
    fpga_M=[
            {"Modelo": 'M',
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
            {"Modelo": 'M',
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
            {"Modelo": 'M',
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
    fpga_G=[
            {"Modelo": 'G',
                "Part0": {
                    "CLBs": 19800,
                    "BRAM": 504,
                    "DSP": 288
                },
                "Part1": {
                    "CLBs": 19080,
                    "BRAM": 576,
                    "DSP": 288
                },
                "Part2": {
                    "CLBs": 22140,
                    "BRAM": 540,
                    "DSP": 216
                },
                
                "Part3": {
                    "CLBs": 19440,
                    "BRAM": 540,
                    "DSP": 216
                },
                "Part4": {
                    "CLBs": 10980,
                    "BRAM": 288,
                    "DSP": 144
                },
                "Part5": {
                    "CLBs": 10800,
                    "BRAM": 360,
                    "DSP": 144
                },
                "Part6": {
                    "CLBs": 2940,
                    "BRAM": 72,
                    "DSP": 0
                },
                "Part7": {
                    "CLBs": 2940,
                    "BRAM": 72,
                    "DSP": 0
                },
                "Part8": {
                    "CLBs": 2940,
                    "BRAM": 84,
                    "DSP": 24
                }
            },
            {"Modelo": 'G',
                "Part0": {
                    "CLBs": 19800,
                    "BRAM": 504,
                    "DSP": 288
                },
                "Part1": {
                    "CLBs": 19080,
                    "BRAM": 576,
                    "DSP": 288
                },
                "Part2": {
                    "CLBs": 22140,
                    "BRAM": 540,
                    "DSP": 216
                },
                "Part3": {
                    "CLBs": 19440,
                    "BRAM": 540,
                    "DSP": 216
                },
                "Part4": {
                    "CLBs": 19080,
                    "BRAM": 576,
                    "DSP": 288
                },
                "Part5": {
                    "CLBs": 19800,
                    "BRAM": 504,
                    "DSP": 288
                },
                "Part6": {
                    "CLBs": 2940,
                    "BRAM": 72,
                    "DSP": 0
                }
            },
            {"Modelo": 'G',
                "Part0": {
                    "CLBs": 19800,
                    "BRAM": 504,
                    "DSP": 288
                },
                "Part1": {
                    "CLBs": 10800,
                    "BRAM": 300,
                    "DSP": 144
                },
                "Part2": {
                    "CLBs": 10080,
                    "BRAM": 144,
                    "DSP": 72
                },
                "Part3": {
                    "CLBs": 11280,
                    "BRAM": 216,
                    "DSP": 72
                },
                "Part4": {
                    "CLBs": 10980,
                    "BRAM": 288,
                    "DSP": 144
                },
                "Part5": {
                    "CLBs": 10800,
                    "BRAM": 360,
                    "DSP": 144
                },
                "Part6": {
                    "CLBs": 10440,
                    "BRAM": 240,
                    "DSP": 96
                },
                "Part7": {
                    "CLBs": 10800,
                    "BRAM": 300,
                    "DSP": 72
                },
                "Part8": {
                    "CLBs": 10800,
                    "BRAM": 360,
                    "DSP": 144
                },
                "Part9": {
                    "CLBs": 3060,
                    "BRAM": 108,
                    "DSP": 0
                }
            }
            ]
    
    fpga=[[30300,600,1920],[67200,1680,768],[134280,3780,1800]]
    size_Fgpa=[fpga_P,fpga_M,fpga_G]
    
    for index in range(0,len(graph),2):
        if graph[index] != "[]":
            sort_Fpga=random.choice(range(len(fpga)))
            new_fpga=(random.choice(size_Fgpa[sort_Fpga]))
            graph[index]=f"{[[new_fpga]]}"
    
    return graph
        
                    

def saveGraph_to_JSON(graph):
    # Initialize an empty dictionary to hold the final structured data
    structured_data = {}

    # Iterate over the input data with index to create nodes
    for index in range(0, len(graph), 2):
        node = 0
        if index > 0:
            node = index // 2
        
        node_key = f"Nodo{node}"
        
        # Initialize the node structure
        structured_data[node_key] = {
            "FPGA": [],
            "Links": []
        }
        
        parsed_item = ast.literal_eval(graph[index])
        structured_data[node_key]["FPGA"] = parsed_item
        parsed_item = ast.literal_eval(graph[index+1])
        structured_data[node_key]["Links"] = parsed_item
    
    with open('topologia.json', 'w') as file:
        json.dump(structured_data, file, indent=4)
    
    
def saveReq_to_JSON(req):
    
    structured_data = {}
    
    for index, data in enumerate(req):
        node_key = f"{index}"
        structured_data[node_key] = {}
               
        parsed_item = ast.literal_eval(data)
        structured_data[node_key] = parsed_item
        
    
    with open('requisicoes.json', 'w') as file:
        json.dump(structured_data, file, indent=4)

def run_Best_Worst():

    with open('data_raw.csv', 'r') as file:
        reader = csv.reader(file)
        dataset = list(reader)
        
    with open('graphs.pkl', 'rb') as file:
        graphs = pickle.load(file)


    for graph in range(int(len(dataset)/101)):
        best = []
        worst = []
        graph *= 101    
        for i in range(graph, graph + 100):
            if len(best) < 3:
                dataset[i].append(i)
                best.append(dataset[i])
                best.sort(key=lambda x: x[-14])
                worst = best.copy()
                continue
            else:
                if dataset[i][-14] > best[0][-14]:
                    best[0] = dataset[i]
                    best[0].append(i)
                    best.sort(key=lambda x: x[-14])
                elif dataset[i][-14] < worst[0][-14]:
                    worst[0] = dataset[i]
                    worst[0].append(i)
                    worst.sort(key=lambda x: x[-14])
        
        saveReq_to_JSON(dataset[graph + 100])
        graphs=[]
        for i in range(3):
            #Flex positioning, fix partitioning
            baseGraph = worst[i][:-14]
            graphs.append(baseGraph)
            scrumble_partitioning(baseGraph)
            for index in range(20):
                derivateGraph = scrumble_positioning(baseGraph)    
                saveGraph_to_JSON(derivateGraph)        
                print(index)
                csv_row = []
                
                result_ILP_ciente,time_ILP_ciente, resources_model_ILP, req_allocated_ILP_aware = ILP.main()
                if result_ILP_ciente == 0:
                    continue              

                with open('topologia.json', 'r') as json_file:
                    topologia = json.load(json_file)

                for node, node_data in topologia.items():
                    resource = node_data['FPGA']
                    csv_row.append(resource) 
                    link = node_data['Links']
                    csv_row.append(link)
                
                with open('data_BestWorst.csv', 'a+', newline='') as csv_file:
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
                    
            with open('requisicoes.json', 'r') as json_file:
                req = json.load(json_file)  
                csv_row = []
                for req, req_data in req.items():
                    csv_row.append(req_data)
                    
            with open('data_BestWorst.csv', 'a+', newline='') as csv_file:
                writer = csv.writer(csv_file)
                writer.writerow(csv_row)
                
        for i in range(3):
            #Fix positioning, flex partitioning
            baseGraph = best[i][:-14]
            graphs.append(baseGraph)
            for index in range(20):
                derivateGraph = scrumble_partitioning(baseGraph)    
                saveGraph_to_JSON(derivateGraph)         
                print(index)
                csv_row = []
                
                result_ILP_ciente,time_ILP_ciente, resources_model_ILP, req_allocated_ILP_aware = ILP.main()
                if result_ILP_ciente == 0:
                    continue              

                with open('topologia.json', 'r') as json_file:
                    topologia = json.load(json_file)

                for node, node_data in topologia.items():
                    resource = node_data['FPGA']
                    csv_row.append(resource) 
                    link = node_data['Links']
                    csv_row.append(link)
                
                with open('data_BestWorst.csv', 'a+', newline='') as csv_file:
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
                    
            with open('requisicoes.json', 'r') as json_file:
                req = json.load(json_file)  
                csv_row = []
                for req, req_data in req.items():
                    csv_row.append(req_data)
                    
            with open('data_BestWorst.csv', 'a+', newline='') as csv_file:
                writer = csv.writer(csv_file)
                writer.writerow(csv_row) 
                       
        with open("graphs_BW.pkl", "wb") as f:
            pickle.dump(graphs, f)
            
            
def main():
    run_Best_Worst()           
            
if __name__ == "__main__":
    main()