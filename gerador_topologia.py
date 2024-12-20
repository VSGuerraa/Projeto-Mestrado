import json
import networkx as nx
import matplotlib.pyplot as plt
import random
import sys

def gerador_Topologia(nro_Nodos, nro_Links, G=None, initial=False):
    
    if G is None:
        G = nx.gnm_random_graph(nro_Nodos, nro_Links)

        while not(nx.is_connected(G)):
            G = nx.gnm_random_graph(nro_Nodos, nro_Links)
    
    
    degrees = dict(G.degree())
    max_degree = max(degrees.values())
    max_FGPA = nro_Nodos//4
    nroMax_FPGA_P = 0
    nroMax_FPGA_M = max_FGPA
    nroMax_FPGA_G = 0
    
    subax1 = plt.subplot(121)
    nx.draw_circular(G, with_labels=True, font_weight='bold')

    plt.savefig('Grafo.png')
    #plt.show() 
    subax1.clear()
    list_edges=list(G.edges)
    topologia_rede={}
    fpga=[]
    fpga=[[30300,600,1920],[67200,1680,768],[134280,3780,1800]]
    list_thro=[100,200,400]
    
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
                
    size_Fgpa=[fpga_P,fpga_M,fpga_G]


    for node in range(nro_Nodos):
        lista_Fpga=[]
        lista_Links=[]
        
        for edge in list_edges:
            nodoS = edge[0]
            nodoD = edge[1]
            if nodoD == node:
                lista_Links.append(nodoS)
            if nodoS == node:
                lista_Links.append(nodoD)

        for index in range(len(lista_Links)):
            thro=random.choice(list_thro)
            lat= random.randint(20,200)
            if lista_Links[index] < node:
                for links in topologia_rede[f"Nodo{lista_Links[index]}"]["Links"]:
                    nodo_D=next(iter(links))
                    if nodo_D == node:
                        lat = links[nodo_D]["Lat"]    
                        thro = links[nodo_D]["Throughput"]
                        break
            lista_Links[index] = {lista_Links[index]: {"Lat": lat, "Throughput": thro}}
        
        '''if max_degree >= 2:   
            ratio=len(lista_Links)/max_degree
            
            value1 = -82.5*ratio + 87.5
            value1 = value1/100
            value3 = 82.5*ratio - 2.5
            value3 = value3/100
            if ratio > 0.5:
                value2 = (-1*ratio)+1
            elif ratio < 0.5:
                value2 = (0.8*ratio)+0.1
            else:
                value2 = 0.5
            probabilities = [value1, value2, value3]
            nro_fpga = random.choices([0, 1, 2], probabilities)[0]
        else:
            nro_fpga = random.choice([0, 1, 2])  '''
        
        if max_FGPA != 0:
            nro_fpga = random.choice([0, 1])
        else:
            nro_fpga = 0
        
        max_FGPA = max_FGPA - nro_fpga         
        
        if nro_fpga!=0:
            lista_Part=[]
            for device in range(nro_fpga):
                sort_Fpga = random.choice([1])  
                if sort_Fpga == 0 and nroMax_FPGA_P != 0:
                    lista_Part.append(random.choice(size_Fgpa[sort_Fpga]))
                    nroMax_FPGA_P = nroMax_FPGA_P - 1
                elif sort_Fpga == 1 and nroMax_FPGA_M != 0:
                    lista_Part.append(random.choice(size_Fgpa[sort_Fpga]))
                    nroMax_FPGA_M = nroMax_FPGA_M - 1
                elif sort_Fpga == 2 and nroMax_FPGA_G != 0:
                    lista_Part.append(random.choice(size_Fgpa[sort_Fpga]))
                    nroMax_FPGA_G = nroMax_FPGA_G - 1
            lista_Fpga.append(lista_Part)
        topologia_rede.update({"Nodo"+str(node): {"FPGA": lista_Fpga, "Links": lista_Links}})
        
    with open ("topologia.json","w") as outfile:
        json.dump(topologia_rede, outfile, indent=4)
        
    if initial:
        with open ("topologia_initial.json","w") as outfile:
            json.dump(topologia_rede, outfile, indent=4)
    
    return G
              
def obter_entrada_inteira(mensagem):
    while True:
        try:
            valor = int(input(mensagem))
            return valor
        except ValueError:
            print("Entrada inválida. Insira um valor inteiro.")

def obter_entrada_dentro_intervalo(mensagem, minimo, maximo):
    while True:
        valor = obter_entrada_inteira(mensagem)
        if minimo <= valor <= maximo:
            return valor
        else:
            print(f"O valor deve estar entre {minimo} e {maximo}.")  
                
def shift_topology(graph):
    nodes = len(graph.nodes)
    


if __name__ == "__main__":
    if len(sys.argv) == 3:
        dados = json.loads(sys.argv[2])  # Converte o argumento de string JSON para um objeto Python
        nro_Nodos = dados['nodos']
        nro_Links = dados['links']
        gerador_Topologia(nro_Nodos,nro_Links)
    else:
        nro_Nodos = obter_entrada_dentro_intervalo("Número de nodos: ", 5, 40)
        nro_Links = obter_entrada_dentro_intervalo(f"Número de links: ", int(nro_Nodos*1.2), int(nro_Nodos*1.3))
        gerador_Topologia(nro_Nodos,nro_Links)
        