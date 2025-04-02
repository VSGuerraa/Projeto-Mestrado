import gerador_topologia
import gerador_req  
import ILP_Full
import ILP_FixPos
import ILP_ciente
import csv
import json
import gurobipy 

def adjust_topology(model):

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
                {   "Modelo": 'P',
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
            },
            {"Modelo": "M",
                "Part0": {
                        "CLBs": 16800,
                        "BRAM": 432,
                        "DSP": 192
                    },
                "Part1": {
                        "CLBs": 13440,
                        "BRAM": 336,
                        "DSP": 192
                    },
                "Part2": {
                        "CLBs": 12960,
                        "BRAM": 336,
                        "DSP": 96
                    },
                "Part3": {
                        "CLBs": 16800,
                        "BRAM": 432,
                        "DSP": 192
                    }
            },
            {"Modelo": 'M',
                "Part0": {
                        "CLBs": 3360,
                        "BRAM": 84,
                        "DSP": 48
                    },
                "Part1": {
                        "CLBs": 3360,
                        "BRAM": 84,
                        "DSP": 48
                    },
                "Part2": {
                        "CLBs": 3360,
                        "BRAM": 84,
                        "DSP": 48
                    },
                "Part3": {
                        "CLBs": 3360,
                        "BRAM": 84,
                        "DSP": 48
                    },
                "Part4": {
                        "CLBs": 3360,
                        "BRAM": 84,
                        "DSP": 48
                    },
                "Part5": {
                        "CLBs": 3360,
                        "BRAM": 84,
                        "DSP": 48
                    },
                "Part6": {
                        "CLBs": 3360,
                        "BRAM": 84,
                        "DSP": 48
                    },
                "Part7": {
                        "CLBs": 3360,
                        "BRAM": 84,
                        "DSP": 48
                    },
                "Part8": {
                        "CLBs": 3240,
                        "BRAM": 84,
                        "DSP": 24
                    },
                "Part9": {
                        "CLBs": 3240,
                        "BRAM": 84,
                        "DSP": 24
                    },
                "Part10": {
                        "CLBs": 3240,
                        "BRAM": 84,
                        "DSP": 24
                    },
                "Part11": {
                        "CLBs": 3240,
                        "BRAM": 84,
                        "DSP": 24
                    },
                "Part12": {
                        "CLBs": 3240,
                        "BRAM": 84,
                        "DSP": 24
                    },
                "Part13": {
                        "CLBs": 3240,
                        "BRAM": 84,
                        "DSP": 24
                    },
                "Part14": {
                        "CLBs": 3240,
                        "BRAM": 84,
                        "DSP": 24
                    },
                "Part15": {
                        "CLBs": 3240,
                        "BRAM": 84,
                        "DSP": 24
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

    partitions = [0,6,13,21,25] #hard-coded index of the partitions in the fpga_M list

    nodes_wFPGA = []
    visited = []

    for v in model.getVars():
        if v.X >0.5:
            var_name = v.VarName.split('_')
            if var_name[0]  == 'w':
                node = int(var_name[2])
                partition = int(var_name[3])
                if node not in visited:
                    nodes_wFPGA.append([node, partition])
                    visited.append(node)

    #Open the topology file and change the position of the nodes with FPGA and respective partitions
    with open("topologia.json") as file:
        topologia = json.load(file)

    for node in topologia:
        topologia[node]['FPGA'] = {}

    for node, partition in nodes_wFPGA:
        for index,value in enumerate(partitions):
            if value == partition:
                topologia[f'Nodo{node}']['FPGA'] = [[fpga_M[index]]]
    
    with open("topologia.json", "w") as file:
        json.dump(topologia, file, indent=4)

def main():

    for nro_nodos in range(10, 25, 5):
        

        nro_req = nro_nodos*10
        result = 0
        stop = False
        batches = 5
        

        for top in range(10):
            
            gerador_topologia.gerador_Topologia(nro_nodos,int(nro_nodos*1.3))

            gerador_req.main(nro_nodos, nro_req)
    
            result, total_time, mount_time = ILP_Full.main()
            
            print(result.ObjVal)
            
            aloc = []
            
            for v in result.getVars():
                if v.X > 0.5:
                    aloc.append(v.VarName)
                    
            with open('Dynamic_alocation_compare.csv', 'a+', newline='') as csv_file:
                writer = csv.writer(csv_file)        
                writer.writerow(['Full', result.ObjVal, result.ObjBound, total_time, mount_time, aloc])

            with open('requisicoes.json', 'r') as json_file:
                req = json.load(json_file)  
                csv_row = []
                for req, req_data in req.items():
                    csv_row.append(req_data)
            
            with open('Dynamic_alocation_compare.csv', 'a+', newline='') as csv_file:
                writer = csv.writer(csv_file)
                writer.writerow(csv_row)

            adjust_topology(result)

            for batch in range(batches):

                for size in range(0, 3):    
                    
                    gerador_req.main(nro_nodos, nro_req, size, batch)
        
                    result, total_time, mount_time = ILP_FixPos.main()
                    aloc = []
                    for v in result.getVars():
                        if v.X > 0.5:
                            aloc.append(v.VarName)

                    with open('Dynamic_alocation_compare.csv', 'a+', newline='') as csv_file:
                        writer = csv.writer(csv_file)
                        writer.writerow([f'Change partition_{batch} + new batch', result.ObjVal, result.ObjBound, total_time, mount_time, f"Size_function_target{size}",aloc])
                    
                    result, total_time, mount_time = ILP_ciente.main()
                    aloc = []
                    for v in result.getVars():
                        if v.X >0.5:
                            aloc.append(v.VarName)
                    
                    with open('Dynamic_alocation_compare.csv', 'a+', newline='') as csv_file:
                        writer = csv.writer(csv_file)
                        writer.writerow([f'New batch_{batch}', result.ObjVal, result.ObjBound, total_time, mount_time,  f"Size_function_target{size}", aloc])
                    
                    with open('requisicoes.json', 'r') as json_file:
                        req = json.load(json_file)  
                        csv_row = []
                        for req, req_data in req.items():
                            csv_row.append(req_data)
                
                    with open('Dynamic_alocation_compare.csv', 'a+', newline='') as csv_file:
                        writer = csv.writer(csv_file)
                        writer.writerow(csv_row)

            with open('topologia.json', 'r') as json_file:
                    topologia = json.load(json_file)
                    csv_row = []
                    for _, node_data in topologia.items():
                        resource = node_data['FPGA']
                        csv_row.append(resource) 
                        link = node_data['Links']
                        csv_row.append(link)
                
            with open('ILP_Compare.csv', 'a+', newline='') as csv_file:
                writer = csv.writer(csv_file)
                writer.writerow(csv_row)


if __name__ == "__main__":
    main()