#imports
import gurobipy as gp
from gurobipy import GRB
import json
import time

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
                
def monta_grafo():
    
    #Nodos

    #file_path= r"C:\Users\victo\Documents\GitHub\Projeto-Mestrado\topologia.json"
    with open("topologia.json") as file:
        topologia = json.load(file)


    nodos=[]
    graph={}
    paths=[]

    for index,value in enumerate(topologia.values()):
        
        nodos=topologia.keys()
        nodos = [str(key) for key in nodos]
        fpgas=(value["FPGA"])
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
        
        if not fpgas:
            graph[f"Nodo_{index}"]={
                            "Resources": [(0,0,0)],
                            "Latency": list_Lat,
                            "Throughput": list_Throughput}
        else:
            for fpga in fpgas:
                for idx_f,parts in enumerate(fpga):
                    for idx_p,part in enumerate(parts):
                        if part=='Modelo':
                            continue
                        clb=parts[part]["CLBs"]
                        bram=parts[part]["BRAM"]
                        dsp=parts[part]["DSP"]
                        const_Part=clb,bram,dsp
                        resources.append(const_Part)
            graph[f"Nodo_{index}"]={
                "Resources": resources,
                "Latency": list_Lat,
                "Throughput": list_Throughput}
            
    return graph,paths

def monta_req():
    #Requisições
    
    #file_path= r"C:\Users\victo\Documents\GitHub\Projeto-Mestrado\requisicoes.json"
    with open("requisicoes.json") as file:
        requisicoes = json.load(file)
        
        
    requisitions=[]
    label_req=[]

    for a,val in enumerate(requisicoes.values()):
        label_req.append("Req_{}".format(a))
        nodo_S=val["Nodo_S"]
        nodo_D=val["Nodo_D"]
        lat=val["max_Lat"]
        thro=val["min_T"]
        valor=val["valor"]
        c_Func=[]
        for fun in val["function_chain"]:
            imp=fun["implementacao"]
            clb=imp["CLBs"]
            bram=imp["BRAM"]
            dsp=imp["DSPs"]
            c_Func.append([clb,bram,dsp])
        c_Req=f"Nodo_{nodo_S}",f"Nodo_{nodo_D}",lat,thro,c_Func,valor
        requisitions.append(c_Req)
        
    return requisitions

def throughput_capacity(graph):
    
    #Throughput Capacity
    
    link_throughput = {}
    for source_node in graph:
        for dest_node in graph[source_node]['Throughput']:
            link_throughput[(source_node, dest_node)] = graph[source_node]['Throughput'][dest_node]
            
    return link_throughput

def monta_modelo(graph, requisitions, paths):
    
    # Create a Gurobi model
    model = gp.Model("RequisitionAllocation")

    # Decision variables
    x = {}

    for req_idx, req in enumerate(requisitions):
        path=list(dfs_caminhos(paths,req[0],req[1]))
        path_Ord=sorted(path,key=len)
        for path in path_Ord:
            for func in range(len(req[4])):
                for node in path:
                    for set_idx, resources in enumerate(graph[f"Nodo_{node}"]["Resources"]):
                        x[(node, set_idx, req_idx, func, tuple(path))] = model.addVar(vtype=GRB.BINARY, name=f"x_{node}_{set_idx}_{req_idx}_{func}_{path}")

    # Decision variables to indicate whether a path is chosen for each requisition
    path_chosen = {}
    for req_idx, req in enumerate(requisitions):
        for path in sorted((list(dfs_caminhos(paths, req[0], req[1]))), key=len):
            path_chosen[(req_idx, tuple(path))] = model.addVar(vtype=GRB.BINARY, name=f"PathChosen_{req_idx}_{tuple(path)}")
                    
    y = {}
    for req_idx, req in enumerate(requisitions):
        y[req_idx] = model.addVar(vtype=gp.GRB.BINARY, name=f"y_{req_idx}")        

    # Objective function: Maximize the number of allocated requisitions with chosen paths
    
    model.setObjective(gp.quicksum(y[req_idx] * req[5] for req_idx, req in enumerate(requisitions)), GRB.MAXIMIZE)

    
    return model,path_chosen,x,y
    
def set_constraints(graph, requisitions, paths, model, x, y,path_chosen):
    
    # Constraint: Resources
    for req_idx, req in enumerate(requisitions):
        for path in sorted((list(dfs_caminhos(paths, req[0], req[1]))), key=len):    
            for node in path:
                for set_idx, resources in enumerate(graph[f"Nodo_{node}"]['Resources']):
                    for func in range(len(req[4])):
                        for resource_idx in range(3):  
                            if (req[4][func][resource_idx]>resources[resource_idx]):
                                model.addConstr(x[(node,set_idx, req_idx, func,tuple(path))]==0)

    # Constraint: Maximum Latency and Minimum Throughput Constraints
            
                        total_latency = 0
                        total_throughput = float('inf') 
                        
                        for i in range(len(path) - 1):
                            total_latency += graph[f"Nodo_{path[i]}"]['Latency'][f"Nodo_{path[i+1]}"]
                            link_throughput = graph[f"Nodo_{path[i]}"]['Throughput'][f"Nodo_{path[i+1]}"]
                            if link_throughput < total_throughput:
                                total_throughput = link_throughput

                        if total_latency > req[2] or total_throughput < req[3]:
                            model.addConstr(x[(node,set_idx, req_idx, func,tuple(path))]== 0, f"LatencyThroughputViolation_{req_idx}_{func}")
                            
    # Constraint: Only one path is chosen for each requisition
    for req_idx, req in enumerate(requisitions):
        model.addConstr(gp.quicksum(path_chosen[(req_idx, tuple(path))] for path in sorted((list(dfs_caminhos(paths, req[0], req[1]))), key=len)) == 1,
                        f"PathSelection_{req_idx}")
        

    for req_idx, req in enumerate(requisitions):
        model.addConstr(
            gp.quicksum(x[(node, set_idx, req_idx, func, tuple(path))]
                        for func in range(len(req[4]))
                        for path in sorted(list(dfs_caminhos(paths, req[0], req[1])), key=len)
                        for node in path
                        for set_idx, _ in enumerate(graph[f"Nodo_{node}"]["Resources"])) <= 1, f"AllocationLimit_{req_idx}")
    
    
    for req_idx, req in enumerate(requisitions):
        num_functions = len(req[4])
        # Constraint: If a path is chosen, then all functions must be allocated
        for func in range(num_functions):
            model.addConstr(
                y[req_idx] <= gp.quicksum(x[(node, set_idx, req_idx, func, tuple(path))]
                                        for path in sorted(list(dfs_caminhos(paths, req[0], req[1])), key=len)
                                        for node in path
                                        for set_idx, _ in enumerate(graph[f"Nodo_{node}"]["Resources"])),
                name=f"req_allocation_if_{req_idx}_{func}"
            )

        # Constraint: If a path is not chosen, then none of the functions can be allocated
        model.addConstr(
            y[req_idx] * num_functions <= gp.quicksum(x[(node, set_idx, req_idx, func, tuple(path))]
                                                    for func in range(num_functions)
                                                    for path in sorted(list(dfs_caminhos(paths, req[0], req[1])), key=len)
                                                    for node in path
                                                    for set_idx, _ in enumerate(graph[f"Nodo_{node}"]["Resources"])),
            name=f"req_allocation_only_if_{req_idx}")
       
def main():
        
        init_time=time.time()
        graph,paths=monta_grafo()
        requisitions=monta_req()
        
        #link_throughput=throughput_capacity(graph)
        model, path_chosen, x, y = monta_modelo(graph, requisitions, paths)
        set_constraints(graph, requisitions, paths, model, x,y, path_chosen)
        
        # Optimize model
        model.optimize()
        end_time=time.time()
        time_elapsed=end_time-init_time
              
       
        return model.objVal,time_elapsed

if __name__ == '__main__':
    main()
    