#imports
import gurobipy as gp
from gurobipy import GRB
import json
import time
import ast

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
    total_link_throughput = {}
    total_graph_throughput = 0
    for source_node in graph:
        for dest_node in graph[source_node]['Throughput']:
            total_link_throughput[(source_node, dest_node)] = graph[source_node]['Throughput'][dest_node]
            total_graph_throughput += graph[source_node]['Throughput'][dest_node]
    return total_link_throughput, total_graph_throughput
        
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
                    
    y = {}
    for req_idx, req in enumerate(requisitions):
        y[req_idx] = model.addVar(vtype=gp.GRB.BINARY, name=f"y_{req_idx}")        

    # Objective function: Maximize the number of allocated requisitions with chosen paths
    
    model.setObjective(gp.quicksum(y[req_idx] * req[5] for req_idx, req in enumerate(requisitions)), GRB.MAXIMIZE)

    
    return model,x,y
    
def set_constraints(graph, requisitions, paths, model, x, y, total_link_throughput):
    
    # Constraint: Resources
    for req_idx, req in enumerate(requisitions):
        for path in sorted((list(dfs_caminhos(paths, req[0], req[1]))), key=len):    
            for node in path:
                for set_idx, resources in enumerate(graph[f"Nodo_{node}"]['Resources']):
                    for func in range(len(req[4])):
                        for resource_idx in range(3):  
                            #if (req[4][func][resource_idx]>resources[resource_idx]):
                            model.addConstr(x[(node,set_idx, req_idx, func,tuple(path))]*resources[resource_idx] <= 
                                            graph[f"Nodo_{node}"]['Resources'][set_idx][resource_idx], 
                                            f"ResourceConstraint_{req_idx}_{func}_{resource_idx}_{node}_{set_idx}_{tuple(path)}")
                                

    # Constraint: Maximum Latency and Minimum Throughput Constraints
                        total_latency = 0
                        total_throughput = float('inf') 
                        
                        for i in range(len(path) - 1):
                            total_latency += graph[f"Nodo_{path[i]}"]['Latency'][f"Nodo_{path[i+1]}"]
                            link_throughput = graph[f"Nodo_{path[i]}"]['Throughput'][f"Nodo_{path[i+1]}"]
                            if link_throughput < total_throughput:
                                total_throughput = link_throughput

                        if total_latency > req[2] or total_throughput < req[3]:
                            model.addConstr(x[(node,set_idx, req_idx, func,tuple(path))]== 0, 
                            f"LatencyThroughputViolation_{req_idx}_{func}")
                        
    #Constraint: All functions must be allocated to allocated requisitions
    for req_idx, req in enumerate(requisitions):
        num_functions = len(req[4])
        model.addConstr(
            y[req_idx] * num_functions <= gp.quicksum(x[(node, set_idx, req_idx, func, tuple(path))]
                                                    for func in range(num_functions)
                                                    for path in sorted(list(dfs_caminhos(paths, req[0], req[1])), key=len)
                                                    for node in path
                                                    for set_idx, _ in enumerate(graph[f"Nodo_{node}"]["Resources"])),
            name=f"req_allocation_only_if_{req_idx}"
        )
        
    #Constraint: Allocation Limit
    for req_idx, req in enumerate(requisitions):
        for func in range(len(req[4])):
            
                model.addConstr(
                    gp.quicksum(x[(node, set_idx, req_idx, func, tuple(path))]
                                for path in sorted(list(dfs_caminhos(paths, req[0], req[1])), key=len)
                                for node in path
                                for set_idx, _ in enumerate(graph[f"Nodo_{node}"]["Resources"])
                    ) <= 1, f"AllocationLimit_{req_idx}"
                )    
                
    # Constraint: Unique Allocation of node-set_idx pair
    for node in range(len(graph)):
        for set_idx, _ in enumerate(graph[f"Nodo_{node}"]["Resources"]) :  
            try:
                model.addConstr(
                    gp.quicksum(x[node, set_idx, req_idx, func, tuple(path)]
                                for req_idx, req in enumerate(requisitions)
                                for path in sorted(list(dfs_caminhos(paths, req[0], req[1])), key=len)
                                for func in range(len(req[4])) 
                                #for node in path
                                if (node, set_idx, req_idx, func, tuple(path)) in x) <= 1,
                    f"UniqueAllocationConstraint_node_{node}_set_idx_{set_idx}")
            except KeyError:
                continue
            
            
    for source_node in graph:
        for dest_node in graph[source_node]['Throughput']:
            model.addConstr(gp.quicksum(x[(path[i], set_idx, req_idx, func, tuple(path))] * req[3] 
                                        for req_idx, req in enumerate(requisitions)
                                        for path in sorted((list(dfs_caminhos(paths, req[0], req[1]))), key=len)
                                        for func in range(len(req[4]))
                                        for i in range(len(path)-1)
                                        for set_idx, _ in enumerate(graph[f"Nodo_{path[i]}"]["Resources"])
                                        if f"Nodo_{path[i]}" == source_node and f"Nodo_{path[i+1]}" == dest_node)
                            <= total_link_throughput[(source_node, dest_node)],
                            f"LinkThroughput_{source_node}_{dest_node}")
     
def show_resources_used(graph, requisitions, paths, x, y, model):
        
    clb_used = 0
    bram_used = 0
    dsp_used = 0
    throghput_used = 0
    clb_total=0
    bram_total=0
    dsp_total=0

    #get what requisition is allocated
    reqs_allocated = []
    for req_idx, req in enumerate(requisitions):
        if y[req_idx].x > 0.5:
            reqs_allocated.append(req_idx)


    for i in range(len(graph)):
        for link in graph[f"Nodo_{i}"]["Throughput"]:
            
            link=int(link.replace("Nodo_", ""))
            for v in model.getVars():
                if v.VarName.startswith(f"x_"):
                    if v.x>0.5:
                        path_str = "_".join(v.VarName.split("_")[5:])
                        path = ast.literal_eval(path_str)
                        
                        for idx_node, node in enumerate(path):
                            if node==i:
                                try:
                                    if path[idx_node+1]==link:
                                        throghput_used+=requisitions[int(v.VarName.split("_")[3])][3]
                                except:
                                    continue
        
                                
    for req_idx, req in enumerate(requisitions):
        for path in sorted((list(dfs_caminhos(paths, req[0], req[1]))), key=len):
            for node in path:
                for set_idx, resources in enumerate(graph[f"Nodo_{node}"]['Resources']):
                    clb_total += resources[0]
                    bram_total += resources[1]
                    dsp_total += resources[2]
                    for func in range(len(req[4])):
                        if x[(node,set_idx, req_idx, func,tuple(path))].x > 0.5:
                            clb_used += resources[0]
                            bram_used += resources[1]
                            dsp_used += resources[2]
                            
    return [throghput_used, clb_used, clb_total, bram_used, bram_total, dsp_used, dsp_total]   

def main():
        
        init_time = time.time()
        graph,paths = monta_grafo()
        requisitions = monta_req()
        total_link_throughput, total_graph_throughput = throughput_capacity(graph)
        model, x, y = monta_modelo(graph, requisitions, paths)
        set_constraints(graph, requisitions, paths, model, x,y, total_link_throughput)
        
        model.setParam('TimeLimit', 5)
        model.optimize()
        #get allocation details
        req_allocated =[]
        for req_idx, req in enumerate(requisitions):
            if y[req_idx].x > 0.5:
                req_allocated.append(req_idx)
        
        values_model = show_resources_used(graph, requisitions, paths, x, y, model)
        values_model.insert(1, total_graph_throughput)
        end_time=time.time()
        time_elapsed=end_time-init_time
    
       
        return model.objVal,time_elapsed,values_model,req_allocated

if __name__ == '__main__':
    main()
    