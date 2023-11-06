#imports
import gurobipy as gp
from gurobipy import GRB
import json

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

    file_path= r"C:\Users\victo\Documents\GitHub\Projeto-Mestrado\topologia.json"
    with open(file_path) as file:
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
                    clb=0
                    bram=0
                    dsp=0
                    for idx_p,part in enumerate(parts):
                        if part=='Modelo':
                            continue
                        clb+=parts[part]["CLBs"]
                        bram+=parts[part]["BRAM"]
                        dsp+=parts[part]["DSP"]
                    const_Part=clb,bram,dsp
                    resources.append(const_Part)
            graph[f"Nodo_{index}"]={
                "Resources": resources,
                "Latency": list_Lat,
                "Throughput": list_Throughput}
            
    return graph,paths

def monta_req():
    #Requisições
    
    file_path= r"C:\Users\victo\Documents\GitHub\Projeto-Mestrado\requisicoes.json"
    with open(file_path) as file:
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
        c_Req=f"Nodo_{nodo_S}",f"Nodo_{nodo_D}",lat,thro,c_Func
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
    for node in graph:
        for set_idx, resources in enumerate(graph[node]["Resources"]):
            for req_idx, req in enumerate(requisitions):
                path=list(dfs_caminhos(paths,req[0],req[1]))
                path_Ord=sorted(path,key=len)
                for path in path_Ord:
                    for func in range(len(req[4])):
                        x[(node, set_idx, req_idx, func, tuple(path))] = model.addVar(vtype=GRB.BINARY, name=f"x_{node}_{set_idx}_{req_idx}_{func}_{path}")

    # Decision variables to indicate whether a path is chosen for each requisition
    path_chosen = {}
    for req_idx, req in enumerate(requisitions):
        for path in sorted((list(dfs_caminhos(paths, req[0], req[1]))), key=len):
            path_chosen[(req_idx, tuple(path))] = model.addVar(vtype=GRB.BINARY, name=f"PathChosen_{req_idx}_{tuple(path)}")
                    
            

    # Objective function: Maximize the number of allocated requisitions with chosen paths
    model.setObjective(gp.quicksum(x[(node, set_idx, req_idx, func, tuple(path))] for node in graph 
                                for set_idx, resources in enumerate(graph[node]["Resources"]) 
                                for req_idx, req in enumerate(requisitions) 
                                for path in sorted((list(dfs_caminhos(paths, req[0], req[1]))), key=len) 
                                for func in range(len(req[4])) ), GRB.MAXIMIZE)
    
    return model,path_chosen,x
    
def set_constraints(graph, requisitions, paths, model, x, path_chosen):
    
    '''    # Constraint: Each requisition must be allocated to exactly one path
    for req_idx, req in enumerate(requisitions):
        model.addConstr(gp.quicksum(path_chosen[(req_idx, tuple(path))] for path in sorted((list(dfs_caminhos(paths, req[0], req[1]))), key=len)) == 1, f"ReqAllocation_{req_idx}")
        
    # Constraint: Each requisition must be allocated to exactly one set of resources
    for req_idx, req in enumerate(requisitions):
        model.addConstr(gp.quicksum(x[(node, set_idx, req_idx, func, tuple(path))] for node in graph 
                                for set_idx, resources in enumerate(graph[node]["Resources"]) 
                                for path in sorted((list(dfs_caminhos(paths, req[0], req[1]))), key=len) 
                                for func in range(len(req[4])) ) == 1, f"ReqAllocation_{req_idx}")
    
    # Constraint: Each requisition must be allocated to a set of resources that can support its function chain
    for req_idx, req in enumerate(requisitions):
        for path in sorted((list(dfs_caminhos(paths, req[0], req[1]))), key=len):
            for func in range(len(req[4])):
                model.addConstr(gp.quicksum(x[(node, set_idx, req_idx, func, tuple(path))] for node in graph 
                                for set_idx, resources in enumerate(graph[node]["Resources"])) <= 1, f"ReqAllocation_{req_idx}")'''
                
    
    #ANALIZAR ESTAS RESTRIÇÕES
    
    # Constraint: Resources
    for req_idx, req in enumerate(requisitions):
        path=list(dfs_caminhos(paths,req[0],req[1]))
        path_Ord=sorted(path,key=len)
        for path in path_Ord:   
            for node in path:
                node = f"Nodo_{node}"
                for set_idx, resources in enumerate(graph[node]['Resources']):
                    for func in range(len(req[4])):
                        for resource_idx in range(3):  
                            model.addConstr(gp.quicksum(x[(node,set_idx, req_idx, func,tuple(path))]*req[4][func][resource_idx] 
                                                        for node in graph for set_idx,resources in enumerate(graph[node]["Resources"]) 
                                                        for func in range(len(req[4])) for path in sorted((list(dfs_caminhos(paths, req[0], req[1]))), key=len)) <= resources[resource_idx],f"ResourceCapacity_{node}_{resource_idx}_{req_idx}_{set_idx}")
                        
                            '''a=model.addConstr(
                                gp.quicksum(req[4][func][resource_idx] * x[(node,set_idx, req_idx, func,tuple(path))]
                                            for func in range(len(req[4])))
                                <= resources[resource_idx],
                                f"ResourceCapacity_{node}_{resource_idx}_{req_idx}_{set_idx}"
                            )'''
                            
                            


    # Constraint: Maximum Latency and Minimum Throughput Constraints
            
                for func in range(len(req[4])):
                    total_latency = 0
                    total_throughput = float('inf') 
                    
                    for i in range(len(path) - 1):
                        total_latency += graph[f"Nodo_{path[i]}"]['Latency'][f"Nodo_{path[i+1]}"]
                        link_throughput = graph[f"Nodo_{path[i]}"]['Throughput'][f"Nodo_{path[i+1]}"]
                        if link_throughput < total_throughput:
                            total_throughput = link_throughput

                    if total_latency > req[2] or total_throughput < req[3]:
                        model.addConstr(gp.quicksum(x[(node,set_idx, req_idx, func,tuple(path))] for node in graph for set_idx,resources in enumerate(graph[node]["Resources"])) == 0, f"LatencyThroughputViolation_{req_idx}_{func}")

    # Constraint: Throughput > 0
                
                    [model.addConstr(gp.quicksum( req[3] * x[(f"Nodo_{path[i]}", set_idx, req_idx, func, tuple(path))] for i in range(len(path) - 1) 
                                                    for set_idx,_ in enumerate(graph[f"Nodo_{path[i]}"]["Resources"]))
                        <= graph[f"Nodo_{path[i]}"]["Throughput"][f"Nodo_{path[i + 1]}"]) for i in range(len(path) - 1)]  
                    
    # Constraint: Only one path is chosen for each requisition
    for req_idx, req in enumerate(requisitions):
        model.addConstr(gp.quicksum(path_chosen[(req_idx, tuple(path))] for path in sorted((list(dfs_caminhos(paths, req[0], req[1]))), key=len)) == 1,
                        f"PathSelection_{req_idx}")
        
    
    #Constraint: Req is allocated at most once

    for req_idx, req in enumerate(requisitions):
        model.addConstr(gp.quicksum(x[(node, set_idx, req_idx, func, tuple(path))] for node in graph
                                    for set_idx,_ in enumerate(graph[node]["Resources"])
                                    for func in range(len(req[4]))
                                    for path in sorted((list(dfs_caminhos(paths, req[0], req[1]))), key=len)) <= 1,
                        f"AllocationLimit_{req_idx}")
        
def main():
        
        graph,paths=monta_grafo()
        requisitions=monta_req()
        link_throughput=throughput_capacity(graph)
        model, path_chosen, x =monta_modelo(graph, requisitions, paths)
        set_constraints(graph, requisitions, paths, model, x, path_chosen)
        
        # Optimize model
        model.optimize()
        
        
        # Print solution
        if model.status == GRB.OPTIMAL:
            print('\nOptimal allocation:')
            for v in model.getVars():
                if v.x > 0:
                    print(f"{v.varName} = {v.x}")
            print(f"\nOptimal objective value: {model.objVal}")
        else:
            print('No solution found.')          
       
       
        return model.objVal

if __name__ == '__main__':
    main()