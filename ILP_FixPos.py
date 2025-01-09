#imports
import gurobipy as gp
from gurobipy import GRB
import json
import time


def main():
    
    init_time = time.time()

    #Paths
    def dfs_caminhos(grafo, inicio, fim):
        inicio = int(inicio.replace("Nodo_", ""))
        fim = int(fim.replace("Nodo_", ""))
        
        pilha = [(inicio, [inicio])]
        while pilha:
            vertice, caminho = pilha.pop()
            for proximo in set(grafo[vertice]) - set(caminho):
                if proximo == fim:
                    yield caminho + [proximo]
                else:
                    pilha.append((proximo, caminho + [proximo]))
                    
    #Nodos

    with open("topologia.json") as file:
        topologia = json.load(file)


    nodos=[]
    graph={}
    paths=[]
    nodes_fpga=[]

    for index,value in enumerate(topologia.values()):
            
        nodos=topologia.keys()
        nodos = [str(key) for key in nodos]
        links=(value["Links"])

        list_Lat={}
        list_Throughput={}
        resources=[]
        links_const=[]
        
        for l in links:
            nodo_d=str(*l.keys())     
            links_const.append(int(nodo_d))
            lat=l[nodo_d]["Lat"]
            thro=l[nodo_d]["Throughput"]
            list_Lat[f"Nodo_{nodo_d}"]=lat
            list_Throughput[f"Nodo_{nodo_d}"]=thro
        paths.append(links_const)
        
        if value["FPGA"] != []:
            for i in range(len(value["FPGA"])):
                nodes_fpga.append(f'Nodo_{index}')
        
        graph[f"Nodo_{index}"]={
                        "Resources": [(0,0,0)],
                        "Latency": list_Lat,
                        "Throughput": list_Throughput}
        
        
        #Requisições
        
    with open("requisicoes.json") as file:
        requisicoes = json.load(file)
        
        
    requisitions=[]



    for a,val in enumerate(requisicoes.values()):
        nodo_S=val["Nodo_S"]
        nodo_D=val["Nodo_D"]
        lat=val["max_Lat"]
        thro=val["min_T"]
        valor=val["valor"]
        c_Func=[]
        latencia_run=[]
        for fun in val["function_chain"]:
            imp=fun["implementacao"]
            clb=imp["CLBs"]
            bram=imp["BRAM"]
            dsp=imp["DSPs"]
            c_Func.append([clb,bram,dsp])
            latencia_run.append(imp['Lat'])
        c_Req=f"Nodo_{nodo_S}",f"Nodo_{nodo_D}",lat,thro,c_Func,valor,latencia_run
        requisitions.append(c_Req)
        
        
    #Throughput-Latency Capacity
    total_link_throughput = {}
    total_link_latency = {}
    for source_node in graph:
        for dest_node in graph[source_node]['Throughput']:
            total_link_throughput[(source_node, dest_node)] = graph[source_node]['Throughput'][dest_node]
        for dest_node in graph[source_node]['Latency']:
            total_link_latency[source_node, dest_node] = graph[source_node]['Latency'][dest_node]
            
            #Lista FPGAs

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
    lista_fpgas=[]

    for fpga in fpga_M:
        lista_fpgas.append(fpga)
    

    # Criar o modelo
    model = gp.Model("network_allocation")

    # Parâmetros de exemplo (para cada requisição, função, nodo, partição, e link)
    functions = [...]  # Lista de funções de rede para cada requisição
    nodes = graph.keys()  # Lista de nodos
    caminhos = []  # Lista de caminhos possíveis
    particoes = []  # Lista de partições
    links = []  # Lista de links

    for fpga_idx, fpga in enumerate(lista_fpgas):
            for part in fpga.values():
                if type(part)==str:
                    continue
                particoes.append(tuple(part.values()))

    for source_node in graph:
        for dest_node in graph[source_node]['Throughput']:
            links.append((source_node, dest_node))

    for req in requisitions:
        for path in sorted((list(dfs_caminhos(paths, req[0], req[1]))), key=len):
            caminhos.append(tuple(path))
            
    x = {}  
    y = {}     
    for req_idx, req in enumerate(requisitions):
        y[req_idx] = model.addVar(vtype=GRB.BINARY, name=f"y_{req_idx}")
        for path in sorted((list(dfs_caminhos(paths, req[0], req[1]))), key=len):
            for node in path:
                for part_idx in range(len(particoes)):
                    for func in req[4]:
                        x[(req_idx, tuple(func), f'Nodo_{node}', part_idx, tuple(path))] = model.addVar(vtype=GRB.BINARY, name=f"x_R{req_idx}_F{tuple(func)}_N{node}_P{part_idx}_K{tuple(path)}")

    # Parâmetros do modelo
    latencia_link = total_link_latency       # latência de cada link (i,j)
    throughput_link = total_link_throughput     # vazão de cada link (i,j)
    fpga_max_por_nodo = 1       # número máximo de FPGAs por nodo
    fpga_max_total = len(nodes_fpga)  # número total máximo de FPGAs permitidos na rede

    # Variáveis de decisão

    w = {}
    for node in graph:
        for p_idx in range(len(particoes)):
            w[(node, p_idx)] = model.addVar(vtype=GRB.BINARY, name=f"w_{node}_{p_idx}")


    node_fpga = {}
    for node in graph:
        node_fpga[node] = model.addVar(vtype=GRB.INTEGER, name=f"node_fpga_{node}")

    # Função Objetivo: Maximizar o valor das requisições alocadas
    model.setObjective(gp.quicksum(y[req_idx] * r[5] for req_idx, r in enumerate(requisitions)), GRB.MAXIMIZE)


    # Restrição 1: Alocação completa da requisição
    for req_idx, r in enumerate(requisitions):
        for f in r[4]:
            func_aloc = gp.quicksum(x.get((req_idx, tuple(f), f'Nodo_{n}', p_idx, tuple(k)),0)
                                    for k in (list(dfs_caminhos(paths, r[0], r[1]))) 
                                    for n in k 
                                    for p_idx in range(len(particoes)))
            model.addConstr(y[req_idx] <= func_aloc, name=f"alocacao_completa_{r}")
            
    # Restrição 2: Função alocada somente uma vez
    for req_idx, r in enumerate(requisitions):
        for f_idx, f in enumerate(r[4]):
            qtd_func_aloc = gp.quicksum(x.get((req_idx, tuple(f), f'Nodo_{n}', p_idx, tuple(k)),0) 
                                        for k in list(dfs_caminhos(paths, r[0], r[1]))
                                        for n in k
                                        for p_idx in range(len(particoes)))
            model.addConstr(qtd_func_aloc <= 1, name=f"funcao_alocada_{req_idx}_{f_idx}")
            
    # Restrição 3: Apenas um caminho é escolhido para alocar a requisição
    for req_idx, r in enumerate(requisitions):
        for k in dfs_caminhos(paths, r[0], r[1]):  # Iterate through paths
            model.addConstr(gp.quicksum( x.get((req_idx, tuple(f), f'Nodo_{n}', p_idx, tuple(k)),0)
                                        for f in r[4]
                                        for n in k
                                        for p_idx in range(len(particoes))) == y[req_idx]*len(r[4]),
                name=f"single_path_req_{req_idx}_path_{k}")


    # Restrição 4: Uso de partição única por função
    for n in nodes:
        for p_idx in range(len(particoes)):
                function_count =  gp.quicksum(x.get((req_idx, tuple(f), n, p_idx, tuple(k)),0)
                                            for req_idx, r in enumerate(requisitions)
                                            for f in r[4] 
                                            for k in list(dfs_caminhos(paths, r[0], r[1])))      
                model.addConstr(function_count <= 1, name=f"uso_particao_{n}_{p_idx}")
                
    # Restrição 5: Capacidade de throughoput do link
    for a,b in links:
        sum_thro = gp.quicksum(r[3] * x.get((req_idx, tuple(f), f'Nodo_{n}', p_idx, tuple(k)),0)
                                    for req_idx, r in enumerate(requisitions)
                                    for f in r[4] 
                                    for k in dfs_caminhos(paths, r[0], r[1])
                                    for n in k 
                                    for p_idx in range(len(particoes)))
        model.addConstr(sum_thro <= throughput_link[(a,b)], 
                        name=f"throughput_link_{a}_{b}")
        
    # Restrição 6: Latência no caminho
    for req_idx, r in enumerate(requisitions):
        for k in list(dfs_caminhos(paths, r[0], r[1])):   
            lat_path = gp.quicksum(latencia_link[f'Nodo_{i}', f'Nodo_{j}'] * x.get((req_idx, tuple(f), f'Nodo_{n}', p_idx, tuple(k)),0) 
                                        for f in r[4]
                                        for n in k
                                        for p_idx in range(len(particoes))
                                        for i, j in zip(k, k[1:]))
            lat_run = gp.quicksum(r[6][f_idx] * x.get((req_idx, tuple(f), f'Nodo_{n}', p_idx, tuple(k)),0) 
                                    for f_idx, f in enumerate(r[4])
                                    for n in k
                                    for p_idx in range(len(particoes)))
            model.addConstr((lat_path + lat_run) <= r[2], 
                            name=f"latencia_caminho_{k}")
            
    # Restrição 7: Limitação de recursos computacionais
    for n in nodes:
        for p_idx, part in enumerate(particoes):
                for req_idx, r in enumerate(requisitions):
                    sum_clb = gp.quicksum(f[0] * x.get((req_idx, tuple(f), n, p_idx-1, tuple(k)),0)
                                                for f in r[4] 
                                                for k in dfs_caminhos(paths, r[0], r[1])
                                                ) <= part[0]
                    sum_bram = gp.quicksum(f[1] * x.get((req_idx, tuple(f), n, p_idx-1, tuple(k)),0)
                                                for f in r[4] 
                                                for k in dfs_caminhos(paths, r[0], r[1])
                                                ) <= part[1]
                    sum_dsp = gp.quicksum(f[2] * x.get((req_idx, tuple(f), n, p_idx-1, tuple(k)),0)
                                                for f in r[4] 
                                                for k in dfs_caminhos(paths, r[0], r[1])
                                                ) <= part[2]
                    model.addConstr(sum_clb, name=f"capacidade_clb_{n}_{p_idx-1}_{req_idx}")
                    model.addConstr(sum_bram, name=f"capacidade_bram_{n}_{p_idx-1}_{req_idx}")
                    model.addConstr(sum_dsp, name=f"capacidade_dsp_{n}_{p_idx-1}_{req_idx}")
                    
    # Restrição 8: Se X é alocado, nodo_fpga é 1
    for n in nodes:
        for req_idx, r in enumerate(requisitions):
            for p_idx in range(len(particoes)):
                for k in dfs_caminhos(paths, r[0], r[1]):
                    for f in r[4]:
                        model.addConstr(x.get((req_idx, tuple(f), n, p_idx, tuple(k)),0) <= node_fpga[n],
                                        name=f"nodo_fpga_{n}_{req_idx}_{p_idx}_{k}_{f}")
                        
    # Restrição 9: Número máximo de FPGAs na rede
    model.addConstr(gp.quicksum(node_fpga[n] for n in nodes) <= fpga_max_total, name="max_fpgas_total")

    # Restrição 10: Ativar w se x for alocado
    for n in nodes:
        for p_idx in range(len(particoes)):
            model.addConstr(gp.quicksum(x.get((req_idx, tuple(f), n, p_idx, tuple(k)),0)
                                        for req_idx, r in enumerate(requisitions)
                                        for f in r[4]
                                        for k in dfs_caminhos(paths, r[0], r[1])) <= w.get((n, p_idx),0),
                            name=f"ativar_w_{n}_{p_idx}")
            
    # Restrição 11: Fixar w para cada particionamento
    outter_list = []
    for fpga_idx, fpga in enumerate(lista_fpgas):
        inner_list = []
        for p_idx in range(len(fpga.values())-1):
            inner_list.append(p_idx)
        outter_list.append(inner_list)
    lenght = len(particoes)

    last = []
    for n in nodes:  
        idx_out = 0
        acc = 0
        for idx in range(lenght):
            acc += 1
            size_outter = len(outter_list[idx_out])
            if acc == size_outter:
                idx_out += 1
                acc = 0
                if idx in last:
                    continue
                last.append(idx)
                continue
            model.addConstr(w.get((n, idx),0) == (w.get((n,idx+1),0)), name=f"fixar_w_{n}_{idx}")

    #Restrição 12: Apenas um particionamento por nodo

    for n in nodes:
        model.addConstr(gp.quicksum(w.get((n, p_idx),0) for p_idx in last ) <= 1, name=f"particao_nodo_{n}")
        
    #Restrição 13: Somente W com node_fpga

    for n in nodes:
        for p_idx in range(len(particoes)):
            model.addConstr(w.get((n, p_idx),0) <= node_fpga[n], name=f"w_node_fpga_{n}_{p_idx}")
        
    #Restrição 14: Força FPGA em determinados nodos
    for n in nodes_fpga:
        model.addConstr(node_fpga[n] <= 1, name=f"nodo_fpga_{n}")
                
    model.setParam("OutputFlag", 0)  # Suppress all output

    # Otimizar o modelo
    model.optimize()

    end_time = time.time()
    execution_time = end_time - init_time

    return model, execution_time
    
if __name__ == "__main__":
    main()