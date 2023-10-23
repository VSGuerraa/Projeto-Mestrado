import json
import networkx as nx
import matplotlib.pyplot as plt
import random
import sys

def gerador_Topologia(nro_Nodos, nro_Links):
    
    G = nx.gnm_random_graph(nro_Nodos, nro_Links)
    
    while not(nx.is_connected(G)):
        G = nx.gnm_random_graph(nro_Nodos, nro_Links)
    
    #visualiza grafico em tela
    
    subax1 = plt.subplot(121)
    nx.draw_circular(G, with_labels=True, font_weight='bold')
    
    plt.savefig('Grafo.png')
    #plt.show() 
    subax1.clear()
    
    lista=list(G.edges)

    topologia_rede=[]
    fpga=[]
    


    fpga=[[30300,600,1920],[67200,1680,768],[134280,3780,1800]]
    list_thro=[40,100,200,400]
    
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
                } 
            ]  
    fpga_M=[
            {       "Modelo": 'M',
             
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
            }             
            ]
    fpga_G=[
        {           "Modelo": 'G',
         
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
            }
        ]
                
    size_Fgpa=[fpga_P,fpga_M,fpga_G]

    for a in range(nro_Nodos):
        lista_Fpga=[]
        lista_Links=[]
        
        for b in lista:
            nodoS = b[0]
            nodoD = b[1]
            if nodoD == a:
                lista_Links.append(nodoS)
            if nodoS == a:
                lista_Links.append(nodoD)

        for c in range(len(lista_Links)):
            thro=random.choice(list_thro)
            lat= random.randint(20,200)
            lista_Links[c]={lista_Links[c]: {"Lat": lat, "Throughput": thro}}
       

        nro_fpga=random.randint(0,3)
        
        if nro_fpga!=0:
            lista_Part=[]
            for device in range(nro_fpga):
                
                
                sort_Fpga=random.choice(range(len(fpga)))
                
                lista_Part.append(random.choice(size_Fgpa[sort_Fpga]))
                
            lista_Fpga.append(lista_Part)
           
        topologia_rede.append({"Nodo"+str(a): {"FPGA": lista_Fpga, "Links": lista_Links}})
        
    with open ("topologia.json","w") as outfile:
        json.dump(topologia_rede, outfile, indent=4)
        
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
        