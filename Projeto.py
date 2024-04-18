import json
import math
import random
import statistics as stats
from dataclasses import dataclass
import matplotlib.pyplot as plt
import copy
import numpy as np
import ILP_ciente
import ILP_nao_ciente
import gerador_topologia
import os


@dataclass
class Function:
    name_func:str
    name_imp:str
    clb:int
    bram:int
    dsp:int

@dataclass
class Req:
    id:int
    init_node:int
    out_node:int
    max_Lat:int
    min_T:int
    func:Function
    price:float

@dataclass
class Partition:
    clb:int
    bram:int
    dsp:int

@dataclass
class Link:
    nodo_d: str
    min_Lat: int
    max_T: int

@dataclass
class Node:
    id:str
    fpga:Partition
    link: Link

def check_Lat(nodo_S,nodo_D,lista_Paths,lista_Nodos): #checa menor lat dentre os caminhos possiveis
    
    path=list(dfs_caminhos(lista_Paths,nodo_S,nodo_D))
    path_Ord=sorted(path,key=len)
    menor_Lat=None
    
    for p in path_Ord:
        lat=None
        
        for b,c in zip(p,p[1:]):
            for nodo in lista_Nodos[b].link:
                if int(nodo.nodo_d)==c:
                    if lat==None:
                        lat=nodo.min_Lat
                    else:
                        lat=lat+nodo.min_Lat
        if menor_Lat==None:
            menor_Lat=lat
        
        if lat<menor_Lat:
            menor_Lat=lat
        
    return menor_Lat          

def gerador_Req(nro_Nodos,nro_Req):

    
    lista_Caminhos,lista_Nodos=ler_Topologia()
        
    funcao = {}
    requisicoes = {}

    implementacoes=[{
        "nome" : "FW0",
        "CLBs" : 1150,
        "BRAM" : 5,
        "DSPs" : 0,
        "Lat" : 4.2,
        "Throughput": 2.9},
        {
        "nome" : "FW1",
        "CLBs" : 8537,
        "BRAM" : 1,
        "DSPs" : 0,
        "Lat" : 23,
        "Throughput": 2},
        {
        "nome" : "FW2",
        "CLBs" : 8123,
        "BRAM" : 241,
        "DSPs" : 0,
        "Lat" : 73,
        "Throughput": 92.16},
        {
        "nome" : "DPI0",
        "CLBs" : 8377,
        "BRAM" : 37,
        "DSPs" : 0,
        "Lat" : 278,
        "Throughput": 0.8},
        {
        "nome" : "DPI1",
        "CLBs" : 8612,
        "BRAM" : 438,
        "DSPs" : 0,
        "Lat" : 2778,
        "Throughput": 0.8},
        {
        "nome" : "DPI2",
        "CLBs" : 15206,
        "BRAM" : 36,
        "DSPs" : 0,
        "Lat" : random.randint(278,2778),
        "Throughput": 14.4},
        {
        "nome" : "DPI3",
        "CLBs" : 5154,
        "BRAM" : 407,
        "DSPs" : 0,
        "Lat" : random.randint(278,2778),
        "Throughput": 40},
        {
        "nome" : "DPI4",
        "CLBs" : 713,
        "BRAM" : 96,
        "DSPs" : 0,
        "Lat" : random.randint(278,2778),
        "Throughput": 40},
        {
        "nome" : "DPI5",
        "CLBs" : 6048,
        "BRAM" : 399,
        "DSPs" : 0,
        "Lat" : random.randint(278,2778),
        "Throughput": 102.6},
         {
        "nome" : "AES0",
        "CLBs" : 2532,
        "BRAM" : random.randint(1,5),
        "DSPs" : 0,
        "Lat" : random.randint(2,21),
        "Throughput": 49.38},
        {
        "nome" : "AES1",
        "CLBs" : random.randint(2000,3000),
        "BRAM" : 2,
        "DSPs" : 0,
        "Lat" : 21,
        "Throughput": 1.054},
        {
        "nome" : "AES2",
        "CLBs" : 4095,
        "BRAM" : random.randint(1,5),
        "DSPs" : 0,
        "Lat" : 2,
        "Throughput": 59.3},
        {
        "nome" : "AES3",
        "CLBs" : 2034,
        "BRAM" : random.randint(1,5),
        "DSPs" : 0,
        "Lat" : random.randint(2,21),
        "Throughput": 45},
        {
        "nome" : "AES4",
        "CLBs" : 9561,
        "BRAM" : 450,
        "DSPs" : 0,
        "Lat" : random.randint(2,21),
        "Throughput": 119.3}
    ] #descricao de valores de diferentes implementacoes de funcoes


    nro_Func=random.randint(9,12) #Restringe numero de funcoes na simulacao
    
    for func in range (nro_Func):
        sort_Func=random.randint(0,len(implementacoes)-1)
        if implementacoes[sort_Func]["nome"][0]=='F':
            nome='Firewall'
        elif implementacoes[sort_Func]["nome"][0]=='D':
            nome='Deep Packet Inspection'
        elif implementacoes[sort_Func]["nome"][0]=='A':
            nome='Advanced Encryption Standard'
        funcao[func] = {
            "Nome": nome,
            "implementacao": implementacoes[sort_Func]
            }
        implementacoes[sort_Func]["CLBs"]=int(implementacoes[sort_Func]["CLBs"]*1.25) 
        #considera que apenas 80% das clb são de fato utilizadas
    
    for index in range (nro_Req):
        
        rand_nro_fun=random.randint(1,3) #tamanho da SFC
        func_list=[]
        while rand_nro_fun != 0:
            rand_nro_fun -= 1
            rand_fun=random.randint(0,nro_Func-1)
            if not func_list:
                func_list.append(funcao[rand_fun])
            else:
                while func_list[-1]["Nome"]==funcao[rand_fun]["Nome"]:
                    rand_fun=random.randint(0,nro_Func-1)
                func_list.append(funcao[rand_fun])
        
        rand_nodo_S=random.randint(0,(nro_Nodos-1))
        rand_nodo_D=random.randint(0,(nro_Nodos-1))
        
        while rand_nodo_S==rand_nodo_D:
            rand_nodo_D=random.randint(0,nro_Nodos-1)
        
        aux=funcao[rand_fun]["implementacao"]
        valor=set_value(func_list)
        

        lat=check_Lat(rand_nodo_S,rand_nodo_D,lista_Caminhos, lista_Nodos)            
        
        requisicoes[index] = {
            "Id": index,
            "Nodo_S": rand_nodo_S,
            "Nodo_D": rand_nodo_D,
            "max_Lat": int(lat*1.3),
            "min_T": aux["Throughput"],
            "function_chain": func_list,
            "valor": valor
            }

    with open ("requisicoes.json","w") as outfile:
        json.dump(requisicoes, outfile, indent=4)

    with open ("funcoes.json","w") as outfile:
        json.dump(funcao, outfile, indent=4)

    with open ("implementacoes.json","w") as outfile:
        json.dump(implementacoes, outfile, indent=4)
    
def dfs_caminhos(grafo, inicio, fim):
    pilha = [(inicio, [inicio])]
    while pilha:
        vertice, caminho = pilha.pop()
        for proximo in set(grafo[vertice]) - set(caminho):
            if proximo == fim:
                yield caminho + [proximo]
            else:
                pilha.append((proximo, caminho + [proximo]))

def ler_Requisicoes():
    
    with open("requisicoes.json") as file1:
        requisicoes = json.load(file1)
        
        
        
    lista_Req=[]
    
    for a,val in enumerate(requisicoes.values()):
        Id=val["Id"]
        nodo_S=val["Nodo_S"]
        nodo_D=val["Nodo_D"]
        lat=val["max_Lat"]
        thro=val["min_T"]
        valor=val["valor"]
        c_Func=[]
        for fun in val["function_chain"]:
            nome_F=fun["Nome"]
            imp=fun["implementacao"]
            nome_I=imp["nome"]
            clb=imp["CLBs"]
            bram=imp["BRAM"]
            dsp=imp["DSPs"]
            c_Func.append(Function(nome_F,nome_I,clb,bram,dsp))
        c_Req=Req(Id,nodo_S,nodo_D,lat,thro,c_Func,valor)
        lista_Req.append(c_Req)
        
    return lista_Req

def ler_Topologia():
    

    #file_path= r"C:\Users\victo\Documents\GitHub\Projeto-Mestrado\topologia.json"
    with open("topologia.json") as file:
        topologia = json.load(file)
    

    nodos=[]
    links=[]
    lista_Caminhos=[]
    caminhos=[]
    lista_Nodos=[]


    for index,values in enumerate(topologia.values()):
        
        nodos=topologia.keys()
        nodos = [str(key) for key in nodos]
        nodo_id=nodos[index]
        fpgas=(values["FPGA"])
        links=(values["Links"])
        caminhos=[]
        lista_Links=[]
        lista_Fpga=[]

        for l in links:
            nodo_d=str(*l.keys())   
            lat=l[nodo_d]["Lat"]
            thro=l[nodo_d]["Throughput"]
            const_Link=Link(nodo_d,lat,thro)
            lista_Links.append(const_Link)
            caminhos.append(int(nodo_d))
        lista_Caminhos.append(caminhos)

        
        for fpga in fpgas:
            
            for parts in fpga:
                lista_Parts=[]
                for part in parts:
                #id=str(*part.keys())
                    if part=='Modelo':
                        continue
                    clb=parts[part]["CLBs"]
                    bram=parts[part]["BRAM"]
                    dsp=parts[part]["DSP"]
                    const_Part=Partition(clb,bram,dsp)
                    lista_Parts.append(const_Part)
                lista_Fpga.append(lista_Parts)
            
        const_Nodo=Node(nodo_id,lista_Fpga,lista_Links)
        
        lista_Nodos.append(const_Nodo)
                    
    

    return lista_Caminhos,lista_Nodos

def set_value(func_list):
    total_value=0
    for func in func_list:
        if func["implementacao"]["CLBs"]>10000 or func["implementacao"]["BRAM"]>240:
            total_value+=20
        elif func["implementacao"]["CLBs"]>5000 or func["implementacao"]["BRAM"]>120:
            total_value+=10
        else:
            total_value+=6
            
    return total_value

def wrong_Run(lista_Req,lista_Paths,lista_Nodos):
    
    lista_Fpga=[]
    for nodo in lista_Nodos:
        for fpga in nodo.fpga:
            clb=0
            bram=0
            dsp=0
            nodo_id=nodo.id
            for part in fpga:
                clb+=part.clb
                bram+=part.bram
                dsp+=part.dsp
            if int(clb/110000)==1:
                modelo=3
            elif int(clb/58000)==1:
                modelo=2
            elif int(clb/22000)==1:
                modelo=1
            lista_Fpga.append([nodo_id,modelo,clb,bram,dsp])
            
            
    
    with open ("topologia_wrong.json","w") as outfile:
        json.dump(lista_Fpga, outfile, indent=4)       
            
    aloc_Req=[]
    
    for nr_req,req in enumerate(lista_Req):
        path=list(dfs_caminhos(lista_Paths,req.init_node,req.out_node))
        path_Ord=sorted(path,key=len)
        check_Node=False
        check_Link=1
        refresh_Links=[]
        device_id=None
        
        
        for caminho in path_Ord:
            
            check_Node=False
            check_Link=1
            for nodo in caminho:
                device_id=[]
                total_utilizado=[]
                total_restante=[]
                for i_func in range(len(req.func)):
                    for i_device,device in enumerate(lista_Fpga):
                        if device[0]=='Nodo'+str(nodo):

                            if not total_utilizado:
                                for i_equipament in range(len(lista_Fpga)):
                                    total_utilizado.append([0,0,0])
                                    total_restante.append([0,0,0])
                            
                            if device[2]>=total_utilizado[i_device][0]and device[3]>=total_utilizado[i_device][1]and device[4]>=total_utilizado[i_device][2]:
                                total_restante[i_device]=[device[2]-total_utilizado[i_device][0],device[3]-total_utilizado[i_device][1],device[4]-total_utilizado[i_device][2]]
                                if total_restante[i_device][0]>=req.func[i_func].clb and total_restante[i_device][1]>=req.func[i_func].bram and total_restante[i_device][2]>=req.func[i_func].dsp:
                                    device_id.append([i_device,i_func])  
                                    total_utilizado[i_device][0]+=req.func[i_func].clb
                                    total_utilizado[i_device][1]+=req.func[i_func].bram
                                    total_utilizado[i_device][2]+=req.func[i_func].dsp
                                    break            
                                #checa se fpga tem recursos para alocar requisicao
                if len(device_id)==len(req.func):
                    check_Node=True
                    break
        
            for b,c in zip(caminho,caminho[1:]):
                lista_Check=check_Path(c,lista_Nodos[b].link,req)
                check_Link+=lista_Check[0]
                aux_Lista=b,lista_Check[1],lista_Check[2]
                refresh_Links.append(aux_Lista)
            if check_Link==len(caminho):
                check_Link=True
                break
            else:
                check_Link=False
        #checa se caminho tem capacidade de throughput
        
        if check_Link and check_Node:
            
            aloc_Req.append([req,device[1],i_device])
            for func in range(len(req.func)):
                lista_Fpga[device_id[func][0]][2]=lista_Fpga[device_id[func][0]][2]-req.func[func].clb
                lista_Fpga[device_id[func][0]][3]=lista_Fpga[device_id[func][0]][3]-req.func[func].bram
                lista_Fpga[device_id[func][0]][4]=lista_Fpga[device_id[func][0]][4]-req.func[func].dsp
            
            
            
            for nodo_I,nodo_F,thro in refresh_Links:
                for l in (lista_Nodos[nodo_I].link):
                    if int(l.nodo_d)==nodo_F:
                        l.min_T=thro
        #se link e recursos satisfazem os requisitos, req eh alocada e atualiza-se recursos consumidos
    
    ratio=len(aloc_Req)/len(lista_Req)
    
    #print("Nr requisicoes alocadas W:",len(aloc_Req),"\nRatio:",round(ratio,2),"%")
    
    
    
    return(len(aloc_Req), aloc_Req)
#executa o algoritmo guloso pela visão '

def check_Path(node_D,nodos,req):
    valid_Path=0
    new_Thro=None
    
    for nodo in nodos:
        if int(nodo.nodo_d)==node_D:
            if nodo.min_Lat<=req.max_Lat:
                if nodo.max_T>=req.min_T:
                    new_Thro=nodo.max_T-req.min_T
                    valid_Path=1
                    
    return [valid_Path,node_D,new_Thro]
#checa se o caminho do nodo inicial ate o final eh valido em relacao a latencia e vazio

def check_Parts(devices, function, part_allocated,nodo):
    
    
    pesos=[]
    
    weight_clb=1
    weight_bram=50
    weight_dsp=20
    
    for fpga,partitions in enumerate(devices):
        if len(partitions)==0: 
            return False
        for index_part,part in enumerate(partitions):
            total_weight=0
            allocated = False
            for cont in range(len(part_allocated)):
                if part_allocated[cont] == False:
                    continue
                if index_part == part_allocated[cont][3] and fpga == part_allocated[cont][2]:
                    allocated =True
                
            if allocated:
                continue
            if part.clb-function.clb<0:
                continue
            if part.bram-function.bram<0:
                continue
            if part.bram-function.bram<0:
                continue
            total_weight=(part.clb-function.clb)*weight_clb
            total_weight+=(part.bram-function.bram)*weight_bram
            total_weight+=(part.dsp-function.dsp)*weight_dsp
            pesos.append([total_weight,nodo,fpga,index_part])
            
    if len(pesos)==0: 
            return False    
    
    
    min_value = min(pesos, key=lambda sublist: sublist[0])
    
    return(min_value) 
#Checa por partição que aloca melhor a req     

def check_Wrong(aloc_Req,lista_Paths):
    
    with open("topologia_wrong.json") as file:
        topologia = json.load(file)
      
    aloc_W=[]
    
    for req in aloc_Req:
        path=list(dfs_caminhos(lista_Paths,req[0].init_node,req[0].out_node))
        path_Ord=sorted(path,key=len)
        
        not_valid=True
        
        for idx_func in range(len(req[0].func)):
            func_valid=[]
            for id,device in enumerate(topologia):
                
                for path in path_Ord:
                    for nodo in path:
                        
                        if device[0]!="Nodo"+str(nodo) or device[1]==0:
                            continue
                    
                    
                        min_Tile_clb=math.ceil(req[0].func[idx_func].clb/60)
                        min_Tile_bram=math.ceil(req[0].func[idx_func].bram/12)
                    
                    
                        min_Clb=0
                        min_Bram=0
                            
                        if device[1]==1:
                            divisor=5
                            min_Tile=5
                        elif device[1]==2:
                            divisor=8
                            min_Tile=3
                        elif device[1]==3:
                            divisor=15
                            min_Tile=2
                            
                        comparador=0
                        
                        #checa por numero de CLB
                        for linha in range(divisor,0,-1):
                            if min_Tile_clb%linha == 0 and min_Tile_clb<(device[2]*(linha/divisor)):
                                for index in range(0,int(min_Tile_clb/linha),10):            
                                    min_Bram+=linha
                                melhor=0
                                break
                            else:
                                if comparador==0:
                                    comparador=(min_Tile_clb%linha) / linha
                                    
                                else:
                                    if comparador>((min_Tile_clb%linha) / linha):
                                        comparador=(min_Tile_clb%linha) / linha
                                        melhor=linha              #checa por menor ratio entre coluna/linha, priorizando colunas maiores
                        if melhor!=0:
                            for index in range(0,int(min_Tile_clb/melhor),10):            
                                min_Bram+=melhor
                            linha=melhor
                        
                        part=[linha,math.ceil(min_Tile_clb/linha)]
                        
                        comparador=0
                        #checa por numero de BRAM
                        for linha in range(divisor,0,-1):
                            
                            if min_Tile_bram%linha == 0 and min_Tile_bram<(device[3]*(linha/divisor)):
                                for index in range(0,int(min_Tile_bram/linha),min_Tile):            
                                    min_Clb+=linha
                                melhor=0
                                break
                            else:
                                if comparador==0:
                                    comparador=(min_Tile_bram%linha) / linha
                                    
                                else:
                                    if comparador>((min_Tile_bram%linha) / linha):
                                        comparador=(min_Tile_bram%linha) / linha
                                        melhor=linha              #checa por menor ratio entre coluna/linha, priorizando colunas maiores
                        if melhor!=0:
                            for index in range(0,int(min_Tile_bram/melhor),min_Tile):            
                                min_Clb+=melhor
                            linha=melhor
                        
                        
                        if device[2]-min_Tile_bram<0 or device[3]-min_Tile_bram<0:
                            continue
                        
                        else:
                            if min_Bram>=min_Tile_bram or min_Clb>=min_Tile_clb:
                                if part[0]>=linha: 
                                    min_Clb=part[0]*math.ceil(min_Tile_clb/part[0])*60
                                    min_Bram=part[0]*math.ceil(min_Tile_bram/part[0])*12
                                    topologia[id][2]=topologia[id][2]-min_Clb
                                    topologia[id][3]=topologia[id][3]-min_Bram
                                    not_valid = False
                                    func_valid.append(True)
                                    break
                                else:
                                    min_Clb=linha*math.ceil(min_Tile_clb/linha)*60
                                    min_Bram=linha*math.ceil(min_Tile_bram/linha)*12
                                    topologia[id][2]=topologia[id][2]-min_Clb
                                    topologia[id][3]=topologia[id][3]-min_Bram
                                    not_valid = False
                                    func_valid.append(True)
                                    break
                        
                        
                            
                    if not_valid == False:
                        break
                if not_valid == False:
                    break
                                               
                    
                            
        if len(func_valid) != len(req[0].func): 
            aloc_W.append(req)
            
    return aloc_W               
                                     
def greedy(lista_Req,lista_Paths,node_List):
    aloc_Req=[]
    cash=0
    for req in lista_Req:
        path=list(dfs_caminhos(lista_Paths,req.init_node,req.out_node))
        path_Ord=sorted(path,key=len)
        
        refresh_Links=[]
        check_Link=False

        
        for caminho in path_Ord:
            
            if check_Link == "True":
                break
            check_Node=False
            check_Link=1
            best_part=[]
            for nodo in caminho:
                
                if len(node_List[nodo].fpga)==0:
                    continue
                
                if len(best_part)==0:
                    
                    for func in req.func:
                        best_part.append(check_Parts(node_List[nodo].fpga,func,best_part,nodo))
                elif False in best_part:
                    indices = [i for i, x in enumerate(best_part) if x == False]
                    for i in indices:
                        valid_part = check_Parts(node_List[nodo].fpga,req.func[i],best_part,nodo)
                        if valid_part:
                            best_part[i]=valid_part
                    
                    
                if False in best_part:
                    continue
                else:
                    check_Node=True
                    index = 3
                    best_part = sorted(best_part, key=lambda sublist: sublist[index], reverse=True)
                    #organiza a lista em ordem decrescente para o pop() funcionar corretamente
                    break
          
    
            if check_Node==False:
                continue
            
            for b,c in zip(caminho,caminho[1:]):
                lista_Check=check_Path(c,node_List[b].link,req)
                check_Link+=lista_Check[0]
                aux_Lista=b,lista_Check[1],lista_Check[2]
                refresh_Links.append(aux_Lista)
            if check_Link==len(caminho):
                check_Link="True"
                break
            else:
                check_Link=False
                
    
        if check_Link and check_Node:
            
            aloc_Req.append(req)
            
            for func in range(len(req.func)):
                node_List[best_part[func][1]].fpga[best_part[func][2]].pop(best_part[func][3])
            for nodo_I,nodo_F,thro in refresh_Links:
                for l in (node_List[nodo_I].link):
                    if int(l.nodo_d)==nodo_F:
                        l.min_T=thro
        #cash+=req.price

    #ratio=len(aloc_Req)/len(lista_Req)
    

    return(len(aloc_Req), aloc_Req, cash)

def plot_Func(aloc_Desv,valor_Desv,dataset_index,dataset_req_Aloc,dataset_wrongrun):
    
    fig = plt.figure() 
    ax = fig.add_subplot(111) 
    ax.plot(dataset_index, dataset_req_Aloc,color='tab:green',label='Abordagem Ciente de Partições') 
    ax.errorbar(dataset_index, dataset_req_Aloc, yerr=aloc_Desv, fmt="go")
    ax.plot(dataset_index, dataset_wrongrun, color = 'tab:red', label='Abordagem Não Ciente de Partições') 
    ax.errorbar(dataset_index, dataset_wrongrun, yerr=valor_Desv,fmt='ro')
    #plt.title('Numero de funcoes alocadas', fontweight="bold") 
    ax.grid() 
    ax.set_xlabel("Número de Nodos") 
    ax.set_ylabel("Funções Alocadas") 
    ax.set_ylim(0)
    
    plt.legend(loc=2)
    plt.savefig('Grafico_Func.png')
    plt.show()

def plot_Invalidos_fpga(lista_Invalidos,lista_Nodos_all, nr_Simul,lista_Wrong_run):
    
    
    #quebra a lista de req inv em lista de listas com tamanho de acordo com nr de simulaçoes por tamanho de rede
    result = [lista_Invalidos[i:i+nr_Simul] for i in range(0, len(lista_Invalidos), nr_Simul)]
    lista_Nodos= [lista_Nodos_all[i:i+nr_Simul] for i in range(0, len(lista_Nodos_all), nr_Simul)]
    lista_Req = [lista_Wrong_run[i:i+nr_Simul] for i in range(0, len(lista_Wrong_run), nr_Simul)]
    
    nodo_5=[]
    nodo_10=[]
    nodo_15=[]
    nodo_20=[]
    nodo_25=[]
    nodo_30=[]
    nodo_35=[]
    nodo_40=[]
    total=[0,0,0]
    nodos=[nodo_5,nodo_10,nodo_15,nodo_20,nodo_25,nodo_30,nodo_35,nodo_40,total]
  
    

    KU040_Total=[]
    KU095_Total=[]
    VU190_Total=[]
    
    
    
    for i in range(len(lista_Req)):
        for j in range(len(lista_Req[i])):
            for req in lista_Req[i][j]:
                for requisition in result[i][j]:
               
                        
                            if result[i][j] == [0,0,0]:
                                continue
                            
                            if req==requisition[0]:
                                lista_Req[i][j].remove(req)
    
    
    
    
    
    for step in lista_Nodos:
        KU040=0
        KU095=0
        VU190=0
        for inst in step:
            for nodo in inst:
                for fpga in nodo.fpga:
                        if len(fpga)==9:
                            VU190+=1
                        elif len(fpga)==6:
                            KU095+=1
                        elif len(fpga)==3 or len(fpga)==1:
                            KU040+=1
        KU040_Total.append(KU040)
        KU095_Total.append(KU095)
        VU190_Total.append(VU190)
    
    
    
    for nodo in range(len(KU040_Total)):
        nodos[nodo].append(KU040_Total[nodo])
        nodos[nodo].append(KU095_Total[nodo])
        nodos[nodo].append(VU190_Total[nodo])
        nodos[8][0]+=KU040_Total[nodo]
        nodos[8][1]+=KU095_Total[nodo]
        nodos[8][2]+=VU190_Total[nodo]


    KU040_Total=[]
    KU095_Total=[]
    VU190_Total=[]
   
    
    for step in lista_Req:
        KU040=0
        KU095=0
        VU190=0
        
        for inst in step:
            lista_ids=[]
            for req in inst:
                if req==0:
                    continue
                if req[2] in lista_ids:
                    continue
                else:
                    lista_ids.append(req[2])
                    if req[1]==3:
                        VU190+=1
                    elif req[1]==2:
                        KU095+=1
                    elif req[1]==1:
                        KU040+=1
        KU040_Total.append(KU040)
        KU095_Total.append(KU095)
        VU190_Total.append(VU190)

    soma_KU040=0
    soma_KU095=0
    soma_VU190=0
    
    for nodo in range(len(KU040_Total)):
        nodos[nodo][0]=(KU040_Total[nodo]/ nodos[nodo][0])
        soma_KU040+=KU040_Total[nodo]
        nodos[nodo][1]=KU095_Total[nodo]/ nodos[nodo][1]
        soma_KU095+=KU095_Total[nodo]
        nodos[nodo][2]=VU190_Total[nodo]/ nodos[nodo][2]
        soma_VU190+=VU190_Total[nodo]
    
    nodos[8][0]=soma_KU040/ nodos[8][0]
    nodos[8][1]=soma_KU095/ nodos[8][1]
    nodos[8][2]=soma_VU190/ nodos[8][2]
    
    barWidth = 0.1
    br1 = np.arange(3)
    br2 = [x + barWidth for x in br1]
    br3 = [x + barWidth for x in br2]
    br4 = [x + barWidth for x in br3]
    br5 = [x + barWidth for x in br4]
    br6 = [x + barWidth for x in br5]
    br7 = [x + barWidth for x in br6]
    br8 = [x + barWidth for x in br7]
    br9 = [x + barWidth for x in br8]
    
    plt.close()
    plt.bar(br1, nodos[0], color ='tab:red', width = barWidth,
            edgecolor ='k', label ='5')
    plt.bar(br2, nodos[1], color ='tab:orange', width = barWidth,
            edgecolor ='k', label ='10')
    plt.bar(br3, nodos[2], color ='tab:olive', width = barWidth,
            edgecolor ='k', label ='15')
    plt.bar(br4, nodos[3], color ='tab:green', width = barWidth,
            edgecolor ='k', label ='20')
    plt.bar(br5, nodos[4], color ='tab:blue', width = barWidth,
            edgecolor ='k', label ='25')
    plt.bar(br6, nodos[5], color ='tab:cyan', width = barWidth,
            edgecolor ='k', label ='30')
    plt.bar(br7, nodos[6], color ='tab:pink', width = barWidth,
            edgecolor ='k', label ='35')
    plt.bar(br8, nodos[7], color ='tab:purple', width = barWidth,
            edgecolor ='k', label ='40')
    plt.bar(br9, nodos[8], color ='tab:brown', width = barWidth,
            edgecolor ='k', label ='Média')
    
    
    labels=['KU040', 'KU095', 'VU190']
    # Adding Xticks
    plt.xlabel('Modelos FPGA')
    plt.ylabel('Fração de soluções inválidas')
    plt.legend(loc='upper left',  ncol = 3)
    plt.xticks(br1+0.4,labels)
    plt.ylim(0,0.7)
    plt.savefig('Grafico_FPGA.png')
    plt.show()
    
def plot_Solutions_inv(nr_Simul,lista_Invalidos):
    
    
    
    total_Inv=[]
    result = [lista_Invalidos[i:i+nr_Simul] for i in range(0, len(lista_Invalidos), nr_Simul)]
    
    for step in result:
        cont_Inv=0
        for inst in step:
            if inst == [0,0,0]:
                cont_Inv+=1
        total_Inv.append(cont_Inv)
        
    for step in range(len(result)):  
        total_Inv[step]=nr_Simul-total_Inv[step]
        total_Inv[step]=total_Inv[step]/nr_Simul
        
        
    fig = plt.figure() 
    ax = fig.add_subplot(111) 
    ax.plot([5,10,15,20,25,30,35,40], total_Inv,color='tab:green')
    ax.grid() 
    ax.set_xlabel("Número de Nodos") 
    ax.set_ylabel("Fração de soluções inválidas") 
    plt.savefig('Grafico_Func_invalido.png')
    plt.show()

def plot_ILP_value(dataset_ILP_ciente, dataset_std_ILP_ciente, dataset_ILP_naociente, dataset_std_ILP_naociente):
    fig = plt.figure() 
    ax = fig.add_subplot(111) 
    nodes = [5,10,15,20,25,30,35,40]
    nodes = nodes[:len(dataset_ILP_ciente)]
    
    # Plot for ciente
    ax.errorbar(nodes, dataset_ILP_ciente, yerr=dataset_std_ILP_ciente, fmt='-o', color='tab:green', label='Aware')
    
    # Plot for naociente
    ax.errorbar(nodes, dataset_ILP_naociente, yerr=dataset_std_ILP_naociente, fmt='-o', color='tab:red', label='Unaware')
    ax.set_ylim(bottom=0)  # Set the starting point of y-axis to 0
    ax.grid() 
    ax.set_xlabel("Nodes") 
    ax.set_ylabel("Mean Value") 
    ax.legend()  # Add a legend
    
    plt.savefig('Grafico_ILP.png')
    plt.show()

def plot_time_ILP(dataset_ILP_time, dataset_ILP_time_nao_ciente):
    
    topology_size = [5,10,15,20,25,30,35,40]
    topology_size = topology_size[:len(dataset_ILP_time)]

    # Plot for dataset_ILP_time
    fig1 = plt.figure() 
    ax1 = fig1.add_subplot(111) 
    ax1.plot(topology_size, dataset_ILP_time, color='tab:green', label='Partition Awareness')
    ax1.grid() 
    ax1.set_xlabel("Nodes") 
    ax1.set_ylabel("Execution Time(s)") 
    plt.legend(loc=2)
    plt.savefig('Grafico_Time_Ciente.png')
    plt.show()

    # Plot for dataset_ILP_time_nao_ciente
    fig2 = plt.figure() 
    ax2 = fig2.add_subplot(111) 
    ax2.plot(topology_size, dataset_ILP_time_nao_ciente, color='tab:red', label='Partition Unawareness')
    ax2.grid() 
    ax2.set_xlabel("Nodes") 
    ax2.set_ylabel("Execution Time (s)") 
    plt.legend(loc=2)
    plt.savefig('Grafico_Time_Nao_Ciente.png')
    plt.show()

def compare_datasets(dataset_ILP, dataset_ILP_nao_ciente, dataset_total):
    # Calculate the sum and max of values in each dataset
    sum_ILP = sum(dataset_ILP)
    sum_ILP_nao_ciente = sum(dataset_ILP_nao_ciente)
    sum_total = sum(dataset_total)

    # Create a bar chart to compare the total amounts and max values
    labels = ['Awareness', 'Unawareness', 'Total']
    totals = [sum_ILP, sum_ILP_nao_ciente, sum_total]

    plt.bar(labels, totals)
    plt.title('Comparison Between Models')
    plt.xlabel('Dataset')
    plt.ylabel('Value')
    plt.savefig('Grafico_Comparacao.png')
    plt.show()

def plot_resource_comparison_ILP(used_thro, total_thro, used_clb, total_clb, used_bram, total_bram, used_dsp, total_dsp):
    # Tuple datasets [mean, std_dev] for each resource
    datasets = [used_thro, total_thro, used_clb, total_clb, used_bram, total_bram, used_dsp, total_dsp]
    dataset_labels = ['Used Throughput', 'Total Throughput', 'Used CLBs', 'Total CLBs', 'Used BRAM', 'Total BRAM', 'Used DSPs', 'Total DSPs']

    # Define topology sizes
    topology_sizes = np.array([5, 10, 15, 20, 25, 30, 35, 40])
    topology_sizes = topology_sizes[:len(datasets[0])]
    # Iterate through the datasets
    for i in range(0, len(datasets), 2):
        # Extract mean and std_dev from tuples for each dataset
        tuples1 = datasets[i]
        tuples2 = datasets[i + 1]

        # Set up the labels for the current pair of datasets
        labels = [dataset_labels[i], dataset_labels[i + 1]]

        # Plotting
        fig, ax = plt.subplots()

        # Width of the bars
        width = 1

        # Iterate over the tuples
        for j in range(len(tuples1)):
            means1, std_devs1 = tuples1[j]
            means2, std_devs2 = tuples2[j]

            # Plot bars for means and error bars for std_devs
            ax.bar(topology_sizes[j] - width/2, means1, width, label=labels[0] if j == 0 else "", yerr=std_devs1, capsize=3, color='tab:orange')
            ax.bar(topology_sizes[j] + width/2, means2, width, label=labels[1] if j == 0 else "", yerr=std_devs2, capsize=3, color='tab:blue')

        # Add some text for labels, title, and custom x-axis tick labels, etc.
        ax.set_xlabel('Topology Size')
        ax.set_ylabel('Values')
        ax.set_title(f'Comparison of {labels[0]} and {labels[1]}')
        ax.set_xticks(topology_sizes)
        ax.legend()

        fig.tight_layout()

        # Save and show the figure
        plt.savefig(f'Resources_Comparison_ILP_aware_Bars_{labels[0]}_{labels[1]}.png')
        plt.show()

def plot_resource_comparison_ILP_nao_ciente(used_thro, total_thro, used_clb, total_clb, used_bram, total_bram, used_dsp, total_dsp):
    # Tuple datasets [mean, std_dev] for each resource
    datasets = [used_thro, total_thro, used_clb, total_clb, used_bram, total_bram, used_dsp, total_dsp]
    dataset_labels = ['Used Throughput', 'Total Throughput', 'Used CLBs', 'Total CLBs', 'Used BRAM', 'Total BRAM', 'Used DSPs', 'Total DSPs']

    # Define topology sizes
    topology_sizes = np.array([5, 10, 15, 20, 25, 30, 35, 40])
    topology_sizes = topology_sizes[:len(datasets[0])]
    # Iterate through the datasets
    for i in range(0, len(datasets), 2):
        # Extract mean and std_dev from tuples for each dataset
        tuples1 = datasets[i]
        tuples2 = datasets[i + 1]

        # Set up the labels for the current pair of datasets
        labels = [dataset_labels[i], dataset_labels[i + 1]]

        # Plotting
        fig, ax = plt.subplots()

        # Width of the bars
        width = 1

        # Iterate over the tuples
        for j in range(len(tuples1)):
            means1, std_devs1 = tuples1[j]
            means2, std_devs2 = tuples2[j]

            # Plot bars for means and error bars for std_devs
            ax.bar(topology_sizes[j] - width/2, means1, width, label=labels[0] if j == 0 else "", yerr=std_devs1, capsize=3, color='tab:orange')
            ax.bar(topology_sizes[j] + width/2, means2, width, label=labels[1] if j == 0 else "", yerr=std_devs2, capsize=3, color='tab:blue')

        # Add some text for labels, title, and custom x-axis tick labels, etc.
        ax.set_xlabel('Topology Size')
        ax.set_ylabel('Values')
        ax.set_title(f'Comparison of {labels[0]} and {labels[1]}')
        ax.set_xticks(topology_sizes)
        ax.legend()

        fig.tight_layout()

        # Save and show the figure
        plt.savefig(f'Resources_Comparison_ILP_unaware_Bars_{labels[0]}_{labels[1]}.png')
        plt.show()

def save_results_file(*datasets):
    #check if json file exists:
    if os.path.isfile('results.json'):
        with open('results.json') as file:
            results = json.load(file)
    else:
        results = {'aloc_Desv': {'5': [], '10': [], '15': [], '20': [], '25': [], '30': [], '35': [], '40': []}, 
                    'valor_Desv': {'5': [], '10': [], '15': [], '20': [], '25': [], '30': [], '35': [], '40': []}, 
                    'wrong_Desv': {'5': [], '10': [], '15': [], '20': [], '25': [], '30': [], '35': [], '40': []},
                    'total_Value': {'5': [], '10': [], '15': [], '20': [], '25': [], '30': [], '35': [], '40': []},
                    'index': {'5': [], '10': [], '15': [], '20': [], '25': [], '30': [], '35': [], '40': []},
                    'req_Aloc': {'5': [], '10': [], '15': [], '20': [], '25': [], '30': [], '35': [], '40': []},
                    'wrong_run': {'5': [], '10': [], '15': [], '20': [], '25': [], '30': [], '35': [], '40': []},
                    'ILP_ciente_mean': {'5': [], '10': [], '15': [], '20': [], '25': [], '30': [], '35': [], '40': []}, 
                    'ILP_nao_ciente_mean': {'5': [], '10': [], '15': [], '20': [], '25': [], '30': [], '35': [], '40': []},
                    'ILP_ciente_std_dev': {'5': [], '10': [], '15': [], '20': [], '25': [], '30': [], '35': [], '40': []},
                    'ILP_nao_ciente_std_dev': {'5': [], '10': [], '15': [], '20': [], '25': [], '30': [], '35': [], '40': []}, 
                    'ILP_time_ciente': {'5': [], '10': [], '15': [], '20': [], '25': [], '30': [], '35': [], '40': []}, 
                    'ILP_time_nao_ciente': {'5': [], '10': [], '15': [], '20': [], '25': [], '30': [], '35': [], '40': []}, 
                    'ILP_used_throughput_ciente_mean': {'5': [], '10': [], '15': [], '20': [], '25': [], '30': [], '35': [], '40': []},
                    'ILP_used_throughput_ciente_std_dev': {'5': [], '10': [], '15': [], '20': [], '25': [], '30': [], '35': [], '40': []}, 
                    'ILP_total_throughput_ciente_mean': {'5': [], '10': [], '15': [], '20': [], '25': [], '30': [], '35': [], '40': []},
                    'ILP_total_throughput_ciente_std_dev': {'5': [], '10': [], '15': [], '20': [], '25': [], '30': [], '35': [], '40': []},
                    'ILP_used_clb_ciente_mean': {'5': [], '10': [], '15': [], '20': [], '25': [], '30': [], '35': [], '40': []},
                    'ILP_used_clb_ciente_std_dev': {'5': [], '10': [], '15': [], '20': [], '25': [], '30': [], '35': [], '40': []},
                    'ILP_total_clb_ciente_mean': {'5': [], '10': [], '15': [], '20': [], '25': [], '30': [], '35': [], '40': []},
                    'ILP_total_clb_ciente_std_dev': {'5': [], '10': [], '15': [], '20': [], '25': [], '30': [], '35': [], '40': []},
                    'ILP_used_bram_ciente_mean': {'5': [], '10': [], '15': [], '20': [], '25': [], '30': [], '35': [], '40': []},
                    'ILP_used_bram_ciente_std_dev': {'5': [], '10': [], '15': [], '20': [], '25': [], '30': [], '35': [], '40': []},
                    'ILP_total_bram_ciente_mean': {'5': [], '10': [], '15': [], '20': [], '25': [], '30': [], '35': [], '40': []},
                    'ILP_total_bram_ciente_std_dev': {'5': [], '10': [], '15': [], '20': [], '25': [], '30': [], '35': [], '40': []},
                    'ILP_used_dsp_ciente_mean': {'5': [], '10': [], '15': [], '20': [], '25': [], '30': [], '35': [], '40': []},
                    'ILP_used_dsp_ciente_std_dev': {'5': [], '10': [], '15': [], '20': [], '25': [], '30': [], '35': [], '40': []},
                    'ILP_total_dsp_ciente_mean': {'5': [], '10': [], '15': [], '20': [], '25': [], '30': [], '35': [], '40': []},
                    'ILP_total_dsp_ciente_std_dev': {'5': [], '10': [], '15': [], '20': [], '25': [], '30': [], '35': [], '40': []},
                    'ILP_used_throughput_nao_ciente_mean': {'5': [], '10': [], '15': [], '20': [], '25': [], '30': [], '35': [], '40': []},
                    'ILP_used_throughput_nao_ciente_std_dev': {'5': [], '10': [], '15': [], '20': [], '25': [], '30': [], '35': [], '40': []},
                    'ILP_total_throughput_nao_ciente_mean': {'5': [], '10': [], '15': [], '20': [], '25': [], '30': [], '35': [], '40': []},
                    'ILP_total_throughput_nao_ciente_std_dev': {'5': [], '10': [], '15': [], '20': [], '25': [], '30': [], '35': [], '40': []},
                    'ILP_used_clb_nao_ciente_mean': {'5': [], '10': [], '15': [], '20': [], '25': [], '30': [], '35': [], '40': []},
                    'ILP_used_clb_nao_ciente_std_dev': {'5': [], '10': [], '15': [], '20': [], '25': [], '30': [], '35': [], '40': []},
                    'ILP_total_clb_nao_ciente_mean': {'5': [], '10': [], '15': [], '20': [], '25': [], '30': [], '35': [], '40': []},
                    'ILP_total_clb_nao_ciente_std_dev': {'5': [], '10': [], '15': [], '20': [], '25': [], '30': [], '35': [], '40': []},
                    'ILP_used_bram_nao_ciente_mean': {'5': [], '10': [], '15': [], '20': [], '25': [], '30': [], '35': [], '40': []},
                    'ILP_used_bram_nao_ciente_std_dev': {'5': [], '10': [], '15': [], '20': [], '25': [], '30': [], '35': [], '40': []},
                    'ILP_total_bram_nao_ciente_mean': {'5': [], '10': [], '15': [], '20': [], '25': [], '30': [], '35': [], '40': []},
                    'ILP_total_bram_nao_ciente_std_dev': {'5': [], '10': [], '15': [], '20': [], '25': [], '30': [], '35': [], '40': []},
                    'ILP_used_dsp_nao_ciente_mean': {'5': [], '10': [], '15': [], '20': [], '25': [], '30': [], '35': [], '40': []},
                    'ILP_used_dsp_nao_ciente_std_dev': {'5': [], '10': [], '15': [], '20': [], '25': [], '30': [], '35': [], '40': []},
                    'ILP_total_dsp_nao_ciente_mean': {'5': [], '10': [], '15': [], '20': [], '25': [], '30': [], '35': [], '40': []},
                    'ILP_total_dsp_nao_ciente_std_dev': {'5': [], '10': [], '15': [], '20': [], '25': [], '30': [], '35': [], '40': []},
                    'ILP_compare_invalid_mean': {'5': [], '10': [], '15': [], '20': [], '25': [], '30': [], '35': [], '40': []},
                    'ILP_compare_invalid_std_dev': {'5': [], '10': [], '15': [], '20': [], '25': [], '30': [], '35': [], '40': []}}
        

    topology_size = [5, 10, 15, 20, 25, 30, 35, 40]
    topology_size = topology_size[:len(datasets[0])]
    #append values to json file
    for index, size in enumerate(topology_size):
        results['aloc_Desv'][str(size)].append(datasets[0][index])
        results['valor_Desv'][str(size)].append(datasets[1][index])
        results['wrong_Desv'][str(size)].append(datasets[2][index])
        results['total_Value'][str(size)].append(datasets[3][index])
        results['index'][str(size)].append(datasets[-1])
        results['req_Aloc'][str(size)].append(datasets[5][index])
        results['wrong_run'][str(size)].append(datasets[6][index])
        results['ILP_ciente_mean'][str(size)].append(datasets[7][index])
        results['ILP_nao_ciente_mean'][str(size)].append(datasets[8][index])
        results['ILP_ciente_std_dev'][str(size)].append(datasets[9][index])
        results['ILP_nao_ciente_std_dev'][str(size)].append(datasets[10][index])
        results['ILP_time_ciente'][str(size)].append(datasets[11][index])
        results['ILP_time_nao_ciente'][str(size)].append(datasets[12][index])
        results['ILP_used_throughput_ciente_mean'][str(size)].append(datasets[13][index][0])
        results['ILP_used_throughput_ciente_std_dev'][str(size)].append(datasets[13][index][1])
        results['ILP_total_throughput_ciente_mean'][str(size)].append(datasets[14][index][0])
        results['ILP_total_throughput_ciente_std_dev'][str(size)].append(datasets[14][index][1])
        results['ILP_used_clb_ciente_mean'][str(size)].append(datasets[15][index][0])
        results['ILP_used_clb_ciente_std_dev'][str(size)].append(datasets[15][index][1])
        results['ILP_total_clb_ciente_mean'][str(size)].append(datasets[16][index][0])
        results['ILP_total_clb_ciente_std_dev'][str(size)].append(datasets[16][index][1])
        results['ILP_used_bram_ciente_mean'][str(size)].append(datasets[17][index][0])
        results['ILP_used_bram_ciente_std_dev'][str(size)].append(datasets[17][index][1])
        results['ILP_total_bram_ciente_mean'][str(size)].append(datasets[18][index][0])
        results['ILP_total_bram_ciente_std_dev'][str(size)].append(datasets[18][index][1])
        results['ILP_used_dsp_ciente_mean'][str(size)].append(datasets[19][index][0])
        results['ILP_used_dsp_ciente_std_dev'][str(size)].append(datasets[19][index][1])
        results['ILP_total_dsp_ciente_mean'][str(size)].append(datasets[20][index][0])
        results['ILP_total_dsp_ciente_std_dev'][str(size)].append(datasets[20][index][1])
        results['ILP_used_throughput_nao_ciente_mean'][str(size)].append(datasets[21][index][0])
        results['ILP_used_throughput_nao_ciente_std_dev'][str(size)].append(datasets[21][index][1])
        results['ILP_total_throughput_nao_ciente_mean'][str(size)].append(datasets[22][index][0])
        results['ILP_total_throughput_nao_ciente_std_dev'][str(size)].append(datasets[22][index][1])
        results['ILP_used_clb_nao_ciente_mean'][str(size)].append(datasets[23][index][0])
        results['ILP_used_clb_nao_ciente_std_dev'][str(size)].append(datasets[23][index][1])
        results['ILP_total_clb_nao_ciente_mean'][str(size)].append(datasets[24][index][0])
        results['ILP_total_clb_nao_ciente_std_dev'][str(size)].append(datasets[24][index][1])
        results['ILP_used_bram_nao_ciente_mean'][str(size)].append(datasets[25][index][0])
        results['ILP_used_bram_nao_ciente_std_dev'][str(size)].append(datasets[25][index][1])
        results['ILP_total_bram_nao_ciente_mean'][str(size)].append(datasets[26][index][0])
        results['ILP_total_bram_nao_ciente_std_dev'][str(size)].append(datasets[26][index][1])
        results['ILP_used_dsp_nao_ciente_mean'][str(size)].append(datasets[27][index][0])
        results['ILP_used_dsp_nao_ciente_std_dev'][str(size)].append(datasets[27][index][1])
        results['ILP_total_dsp_nao_ciente_mean'][str(size)].append(datasets[28][index][0])
        results['ILP_total_dsp_nao_ciente_std_dev'][str(size)].append(datasets[28][index][1])
        results['ILP_compare_invalid_mean'][str(size)].append(datasets[29][index][0])
        results['ILP_compare_invalid_std_dev'][str(size)].append(datasets[29][index][1])


        with open('results.json', 'w') as file:
            json.dump(results, file, indent=4)
       
def check_Wrong2(req_allocated): #Funciona somente até 2 FPGAs por nodo
    
    with open("topologia_wrong.json") as file:
        topologia = json.load(file)
        
    invalid_list=[]
    valid=None
    for req in req_allocated:
        for idx_device,device in enumerate(topologia):
            if valid==True:
                break
            try:
                if device[0]=="Nodo"+str(req[3]) and topologia[idx_device+1][0]=="Nodo"+str(req[3]) and req[4]==1:
                    continue
            
                
                min_Tile_clb=math.ceil(req[0].func[req[1]].clb/60)
                min_Tile_bram=math.ceil(req[0].func[req[1]].bram/12)
            
            
                min_Clb=0
                min_Bram=0
                
                modelo=device[1]
                clb=device[2]
                bram=device[3]
                
                if modelo==1:
                    total_lines=5
                    column_clb=int((clb/60)/total_lines)
                    column_bram=int((bram/12)/total_lines)
                    min_Tile=5+1
                elif modelo==2:
                    total_lines=8
                    column_clb=int((clb/60)/total_lines)
                    column_bram=int((bram/12)/total_lines)
                    min_Tile=5+1
                elif modelo==3:
                    total_lines=15
                    column_clb=int((clb/60)/total_lines)
                    column_bram=int((bram/12)/total_lines)
                    min_Tile=2+1
                    
            
                for coluna in range(1,column_clb+1):
                    if valid==True:
                        break
                    for linha in range(1,total_lines+1):
                        if min_Tile_clb<linha*coluna:
                                       
                            min_Bram=linha*int(coluna/min_Tile)
                            if min_Bram>=min_Tile_bram:
                                valid=True
                                topologia[idx_device][2]=clb-(linha*coluna*60)
                                topologia[idx_device][3]=bram-(min_Bram*12)
                                break
                
                            
                for coluna in range(1,column_bram+1):
                    if valid==True:
                        break
                    for linha in range(1,total_lines+1):
                        if min_Tile_bram<linha*coluna:           
                            min_Clb=linha*int(coluna/min_Tile)   
                            if min_Clb>=min_Tile_clb:
                                valid=True
                                topologia[idx_device][3]=bram-(linha*coluna*12)
                                topologia[idx_device][2]=clb-(min_Clb*60)
                                break
            except:
                continue
                            
        if valid != True:
            invalid_list.append(req[0].id)
        valid=None
        
        
                            
    return list(set(invalid_list))

def plot_invalid_ratio(dataset_compare_ILP_ratio):
    fig = plt.figure() 
    ax = fig.add_subplot(111) 
    nodes = list(range(len(dataset_compare_ILP_ratio)))  # Use the index as the node
    mean_values = [val[0] for val in dataset_compare_ILP_ratio]
    std_dev_values = [val[1] for val in dataset_compare_ILP_ratio]

    # Plot with error bars
    ax.errorbar(nodes, mean_values, yerr=std_dev_values, fmt='o', color='tab:green', ecolor='tab:green', elinewidth=3, capsize=0, label='Invalid\nTotal')
    ax.plot(nodes, mean_values, color='tab:green', label='Invalid\nTotal')
    ax.grid() 
    ax.set_xlabel("Nodes") 
    ax.set_ylabel("Invalid Ratio") 
    ax.legend()  # Add a legend

    ax.set_ylim(bottom=0)  # Set the starting point of y-axis to 0

    plt.savefig('Grafico_Invalid_Ratio.png')
    plt.show()

def main():

    modo=None

    while  (modo != '2' and modo != '1'):
        
        modo=input("1- Testar unitario\n2- Teste em escala\n")

        if modo == '1': #serve para debug ou analises especificas
            
            nodos_G=int(input("Numero de nodos da rede:\n"))
            links_G=int(input("Numero de links da rede:\n"))
            req=int(input("Numero de requisicoes:\n"))
            gerador_topologia.gerador_Topologia(nodos_G,links_G)
            gerador_Req(nodos_G,req)
            lista_Paths,lista_Nodos=ler_Topologia()
            lista_Req=ler_Requisicoes()
            res_w=wrong_Run(lista_Req,lista_Paths,lista_Nodos)
            res_g=greedy(lista_Req,lista_Paths,lista_Nodos)
            
            result_ILP_ciente,time_ILP_ciente,values_ILP,req_allocated_ILP_aware = ILP_ciente.main()
            print("ILP ciente:",result_ILP_ciente)
            _,_,_,req_allocated_ILP_unaware = ILP_nao_ciente.main()
            
            for idx_req,req in enumerate(req_allocated_ILP_aware):
                req_allocated_ILP_aware[idx_req] = lista_Req[req]
            
            for idx_req,req in enumerate(req_allocated_ILP_unaware):
                req_allocated_ILP_unaware[idx_req][0] = lista_Req[req[0]]
            
            list_wrong_ILP_unaware=check_Wrong2(req_allocated_ILP_unaware)
            print(list_wrong_ILP_unaware)
            
            
            '''#visualização apenas
            a=[]
            b=[]
            c=[]
            for i in res_w[1]:
                a.append(i[0].id)
            print("W:",a)
            for j in res_g[1]:
                b.append(j.id)
            print("G:",b)
            wrong=check_Wrong(res_w[1],lista_Paths)
            for i in wrong:
                c.append(i[0].id)
            print("WW:",c)'''
            
        elif modo=='2':
            
            
            nr_Repeat=2

            print('Executando...')

            lista_Results_g=[]
            lista_Results_w=[]
            dataset_index=[]
            dataset_req_Aloc=[]
            dataset_wrongrun=[]
            dataset_mean_ILP_ciente=[]
            dataset_mean_ILP_nao_ciente=[]
            dataset_ILP_time_ciente=[]
            dataset_ILP_time_nao_ciente=[]
            dataset_std_ILP_ciente=[]
            dataset_std_ILP_nao_ciente=[]
            dataset_ILP_used_throughput_ciente=[]
            dataset_ILP_total_throughput_ciente=[]
            dataset_ILP_used_clb_ciente=[]
            dataset_ILP_total_clb_ciente=[]
            dataset_ILP_used_bram_ciente=[]
            dataset_ILP_total_bram_ciente=[]
            dataset_ILP_used_dsp_ciente=[]
            dataset_ILP_total_dsp_ciente=[]
            dataset_ILP_used_throughput_nao_ciente=[]
            dataset_ILP_total_throughput_nao_ciente=[]
            dataset_ILP_used_clb_nao_ciente=[]
            dataset_ILP_total_clb_nao_ciente=[]
            dataset_ILP_used_bram_nao_ciente=[]
            dataset_ILP_total_bram_nao_ciente=[]
            dataset_ILP_used_dsp_nao_ciente=[]
            dataset_ILP_total_dsp_nao_ciente=[]
            dataset_compare_ILP_ratio=[]

            aloc_Desv=[]
            valor_Desv=[]
            wrong_Desv=[]
            lista_Invalidos=[]
            lista_Nodos_all=[]
            lista_Nodos_W=[]
            total_value=[]
            
            
            for index in range (5,35,5):
                print(nr_Repeat,index)
                req_Aloc_g=[]
                req_Aloc_w=[]
                nr_req_Aloc_W=[]
                lista_result_ILP_ciente=[]
                lista_time_ILP_ciente=[]
                lista_result_ILP_nao_ciente=[]
                lista_time_ILP_nao_ciente=[]
                lista_used_throughput_ILP_ciente=[]
                lista_total_throghput_ILP_ciente=[]
                lista_used_clb_ILP_ciente=[]
                lista_total_clb_ILP_ciente=[]
                lista_used_bram_ILP_ciente=[]
                lista_total_bram_ILP_ciente=[]
                lista_used_dsp_ILP_ciente=[]
                lista_total_dsp_ILP_ciente=[]
                lista_used_throughput_ILP_nao_ciente=[]
                lista_total_throghput_ILP_nao_ciente=[]
                lista_used_clb_ILP_nao_ciente=[]
                lista_total_clb_ILP_nao_ciente=[]
                lista_used_bram_ILP_nao_ciente=[]
                lista_total_bram_ILP_nao_ciente=[]
                lista_used_dsp_ILP_nao_ciente=[]
                lista_total_dsp_ILP_nao_ciente=[]
                valor_Final = []
                total_value_inst=[]
                lista_compare_ILP_ratio=[]
                
                for cont in range(nr_Repeat):

                    total_value_req=0

                    size=index
                    nodos_G=size
                    links_G=int(size*1.3)
                    req=random.randint(int(size*5),int(size*8))
                    
                    gerador_topologia.gerador_Topologia(nodos_G, links_G)
                    gerador_Req(nodos_G,req)
                    
                    lista_Paths,lista_Nodos=ler_Topologia()
                    lista_Nodos_aux=copy.deepcopy(lista_Nodos)
                    
                    lista_Req=ler_Requisicoes()
                    results_g=greedy(lista_Req,lista_Paths,lista_Nodos)
                    lista_Nodos=copy.deepcopy(lista_Nodos_aux)
                    
                    results_w=wrong_Run(lista_Req,lista_Paths,lista_Nodos)
                    lista_Nodos=copy.deepcopy(lista_Nodos_aux)
                    
                    aux=check_Wrong(results_w[1],lista_Paths)
    
                    if len(aux)==0:
                        aux=[0,0,0]
                    lista_Invalidos.append(aux)
                    lista_Nodos_all.append(lista_Nodos)

                    lista_Results_g.append({
                        "Teste"+str(index):{
                        "Lista Requisicoes": len(lista_Req),
                        "Requiscoes alocadas": results_g[0]},
                        "Nodos": len(lista_Nodos),
                        "Valor": results_g[2]
                        })

                    req_Aloc_g.append(results_g[0])
                    valor_Final.append(results_g[2])

                    lista_Results_w.append({
                        "Teste"+str(index):{ 
                        "Lista Requisicoes": len(lista_Req),
                        "Requiscoes alocadas": results_w[0]},
                        "Nodos": len(lista_Nodos),
                        })
                    
                    nr_req_Aloc_W.append(results_w[0])
                    lista_Nodos_W.append(results_w[1])
                    
                    for req in lista_Req:
                        total_value_req+=req.price
                    total_value_inst.append(total_value_req)

                    result_ILP_ciente,time_ILP_ciente, resources_model_ILP, req_allocated_ILP_aware = ILP_ciente.main()
                    if result_ILP_ciente == 0:
                        continue
                    lista_result_ILP_ciente.append(result_ILP_ciente)
                    lista_time_ILP_ciente.append(time_ILP_ciente)
                    lista_used_throughput_ILP_ciente.append(resources_model_ILP[0])
                    lista_total_throghput_ILP_ciente.append(resources_model_ILP[1])
                    lista_used_clb_ILP_ciente.append(resources_model_ILP[2])
                    lista_total_clb_ILP_ciente.append(resources_model_ILP[3])
                    lista_used_bram_ILP_ciente.append(resources_model_ILP[4])
                    lista_total_bram_ILP_ciente.append(resources_model_ILP[5])
                    lista_used_dsp_ILP_ciente.append(resources_model_ILP[6])
                    lista_total_dsp_ILP_ciente.append(resources_model_ILP[7])

                    result_ILP_nao_ciente, time_ILP_nao_ciente, resources_model_ILP_nao_ciente,req_allocated_ILP_unaware = ILP_nao_ciente.main()
                    if result_ILP_nao_ciente == 0:
                        continue
                    lista_result_ILP_nao_ciente.append(result_ILP_nao_ciente)
                    lista_time_ILP_nao_ciente.append(time_ILP_nao_ciente)
                    lista_used_throughput_ILP_nao_ciente.append(resources_model_ILP_nao_ciente[0])
                    lista_total_throghput_ILP_nao_ciente.append(resources_model_ILP_nao_ciente[1])
                    lista_used_clb_ILP_nao_ciente.append(resources_model_ILP_nao_ciente[2])
                    lista_total_clb_ILP_nao_ciente.append(resources_model_ILP_nao_ciente[3])
                    lista_used_bram_ILP_nao_ciente.append(resources_model_ILP_nao_ciente[4])
                    lista_total_bram_ILP_nao_ciente.append(resources_model_ILP_nao_ciente[5])
                    lista_used_dsp_ILP_nao_ciente.append(resources_model_ILP_nao_ciente[6])
                    lista_total_dsp_ILP_nao_ciente.append(resources_model_ILP_nao_ciente[7])
                     
                     
                    for idx_req,req in enumerate(req_allocated_ILP_aware):
                        req_allocated_ILP_aware[idx_req] = lista_Req[req]
                    
                    for idx_req,req in enumerate(req_allocated_ILP_unaware):
                        req_allocated_ILP_unaware[idx_req][0] = lista_Req[req[0]]
                    
                    list_wrong_ILP_unaware=check_Wrong2(req_allocated_ILP_unaware)
                    if list_wrong_ILP_unaware==[]:
                        lista_compare_ILP_ratio.append(0)
                    else:
                        lista_compare_ILP_ratio.append(len(list_wrong_ILP_unaware)/len(req_allocated_ILP_unaware))
                     
                aloc_Desv.append(stats.stdev(req_Aloc_g))
                valor_Desv.append(stats.pstdev(valor_Final))
                wrong_Desv.append(stats.stdev(nr_req_Aloc_W))
                total_value.append(stats.mean(total_value_inst))
                dataset_index.append(index)
                dataset_req_Aloc.append(stats.mean(req_Aloc_g))
                dataset_wrongrun.append(stats.mean(nr_req_Aloc_W))
                dataset_mean_ILP_ciente.append(stats.mean(lista_result_ILP_ciente))
                dataset_mean_ILP_nao_ciente.append(stats.mean(lista_result_ILP_nao_ciente))
                dataset_std_ILP_ciente.append(stats.pstdev(lista_result_ILP_ciente))
                dataset_std_ILP_nao_ciente.append(stats.pstdev(lista_result_ILP_nao_ciente))
                dataset_ILP_time_ciente.append(stats.mean(lista_time_ILP_ciente))
                dataset_ILP_time_nao_ciente.append(stats.mean(lista_time_ILP_nao_ciente))
                dataset_ILP_used_throughput_ciente.append([stats.mean(lista_used_throughput_ILP_ciente),stats.pstdev(lista_used_throughput_ILP_ciente)])
                dataset_ILP_total_throughput_ciente.append([stats.mean(lista_total_throghput_ILP_ciente),stats.pstdev(lista_total_throghput_ILP_ciente)])
                dataset_ILP_used_clb_ciente.append([stats.mean(lista_used_clb_ILP_ciente),stats.pstdev(lista_used_clb_ILP_ciente)])
                dataset_ILP_total_clb_ciente.append([stats.mean(lista_total_clb_ILP_ciente),stats.pstdev(lista_total_clb_ILP_ciente)])
                dataset_ILP_used_bram_ciente.append([stats.mean(lista_used_bram_ILP_ciente),stats.pstdev(lista_used_bram_ILP_ciente)])
                dataset_ILP_total_bram_ciente.append([stats.mean(lista_total_bram_ILP_ciente),stats.pstdev(lista_total_bram_ILP_ciente)])
                dataset_ILP_used_dsp_ciente.append([stats.mean(lista_used_dsp_ILP_ciente),stats.pstdev(lista_used_dsp_ILP_ciente)])
                dataset_ILP_total_dsp_ciente.append([stats.mean(lista_total_dsp_ILP_ciente),stats.pstdev(lista_total_dsp_ILP_ciente)])
                dataset_ILP_used_throughput_nao_ciente.append([stats.mean(lista_used_throughput_ILP_nao_ciente),stats.pstdev(lista_used_throughput_ILP_nao_ciente)])
                dataset_ILP_total_throughput_nao_ciente.append([stats.mean(lista_total_throghput_ILP_nao_ciente),stats.pstdev(lista_total_throghput_ILP_nao_ciente)])
                dataset_ILP_used_clb_nao_ciente.append([stats.mean(lista_used_clb_ILP_nao_ciente),stats.pstdev(lista_used_clb_ILP_nao_ciente)])
                dataset_ILP_total_clb_nao_ciente.append([stats.mean(lista_total_clb_ILP_nao_ciente),stats.pstdev(lista_total_clb_ILP_nao_ciente)])
                dataset_ILP_used_bram_nao_ciente.append([stats.mean(lista_used_bram_ILP_nao_ciente),stats.pstdev(lista_used_bram_ILP_nao_ciente)])
                dataset_ILP_total_bram_nao_ciente.append([stats.mean(lista_total_bram_ILP_nao_ciente),stats.pstdev(lista_total_bram_ILP_nao_ciente)])
                dataset_ILP_used_dsp_nao_ciente.append([stats.mean(lista_used_dsp_ILP_nao_ciente),stats.pstdev(lista_used_dsp_ILP_nao_ciente)])
                dataset_ILP_total_dsp_nao_ciente.append([stats.mean(lista_total_dsp_ILP_nao_ciente),stats.pstdev(lista_total_dsp_ILP_nao_ciente)])
                dataset_compare_ILP_ratio.append([stats.mean(lista_compare_ILP_ratio),stats.pstdev(lista_compare_ILP_ratio)])
                
            #Salva dados dataset em arquivo
                
            save_results_file(aloc_Desv, valor_Desv, wrong_Desv, total_value, dataset_index, dataset_req_Aloc, 
                                dataset_wrongrun, dataset_mean_ILP_ciente, dataset_std_ILP_ciente, dataset_mean_ILP_nao_ciente, 
                                dataset_std_ILP_nao_ciente, dataset_ILP_time_ciente, dataset_ILP_time_nao_ciente, dataset_ILP_used_throughput_ciente, 
                                dataset_ILP_total_throughput_ciente, dataset_ILP_used_clb_ciente, dataset_ILP_total_clb_ciente, 
                                dataset_ILP_used_bram_ciente, dataset_ILP_total_bram_ciente, dataset_ILP_used_dsp_ciente, dataset_ILP_total_dsp_ciente, 
                                dataset_ILP_used_throughput_nao_ciente, dataset_ILP_total_throughput_nao_ciente, dataset_ILP_used_clb_nao_ciente, 
                                dataset_ILP_total_clb_nao_ciente, dataset_ILP_used_bram_nao_ciente, dataset_ILP_total_bram_nao_ciente, 
                                dataset_ILP_used_dsp_nao_ciente, dataset_ILP_total_dsp_nao_ciente,dataset_compare_ILP_ratio, nr_Repeat)    


                
               
            #plot_Invalidos_fpga(lista_Invalidos,lista_Nodos_all,nr_Repeat,lista_Nodos_W)  
            #plot_Solutions_inv(nr_Repeat, lista_Invalidos)
            #plot_Func(aloc_Desv,wrong_Desv,dataset_index,dataset_req_Aloc,dataset_wrongrun)
            plot_ILP_value(dataset_mean_ILP_ciente,dataset_std_ILP_ciente,dataset_mean_ILP_nao_ciente,dataset_std_ILP_nao_ciente)
            plot_time_ILP(dataset_ILP_time_ciente, dataset_ILP_time_nao_ciente)
            compare_datasets(dataset_mean_ILP_ciente, dataset_mean_ILP_nao_ciente,total_value)
            plot_resource_comparison_ILP(dataset_ILP_used_throughput_ciente, dataset_ILP_total_throughput_ciente, dataset_ILP_used_clb_ciente, dataset_ILP_total_clb_ciente, dataset_ILP_used_bram_ciente, dataset_ILP_total_bram_ciente, dataset_ILP_used_dsp_ciente, dataset_ILP_total_dsp_ciente)
            plot_resource_comparison_ILP_nao_ciente(dataset_ILP_used_throughput_nao_ciente, dataset_ILP_total_throughput_nao_ciente, dataset_ILP_used_clb_nao_ciente, dataset_ILP_total_clb_nao_ciente, dataset_ILP_used_bram_nao_ciente, dataset_ILP_total_bram_nao_ciente, dataset_ILP_used_dsp_nao_ciente, dataset_ILP_total_dsp_nao_ciente)    
            plot_invalid_ratio(dataset_compare_ILP_ratio)

            with open("Req_Alocadas.txt","w") as outfile:
                for result in results_g[1]:
                    outfile.write(str(result))
                    outfile.write('\n')
                
            with open("Req_Wrong.txt","w") as outfile:
                for result in results_w[1]:
                    outfile.write(str(result))
                    outfile.write('\n')

        
        else:
            print("Modo inválido")

if __name__ == "__main__":
    main()