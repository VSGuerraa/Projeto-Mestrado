import json
import random
from dataclasses import dataclass

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

def ler_Topologia():
    
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

def dfs_caminhos(grafo, inicio, fim):
    pilha = [(inicio, [inicio])]
    while pilha:
        vertice, caminho = pilha.pop()
        for proximo in set(grafo[vertice]) - set(caminho):
            if proximo == fim:
                yield caminho + [proximo]
            else:
                pilha.append((proximo, caminho + [proximo]))

def main(nro_Nodos=None, nro_Req=None):

    
    lista_Caminhos,lista_Nodos=ler_Topologia()

    if nro_Nodos==None:
        nro_Nodos= len(lista_Nodos)

    if nro_Req==None:
        nro_Req= nro_Nodos*10
        
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


    nro_Func=random.randint(12,12) #Restringe numero de funcoes na simulacao
    
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
        
        min_Throughput=[]
        max_lat=[]
        for function in func_list:
            min_Throughput.append(function["implementacao"]["Throughput"])
            max_lat.append(function["implementacao"]["Lat"])
        
        #lat=random.randint(800,3500)           
        
        requisicoes[index] = {
            "Id": index,
            "Nodo_S": rand_nodo_S,
            "Nodo_D": rand_nodo_D,
            "max_Lat": int(sum(max_lat) + check_Lat(rand_nodo_S,rand_nodo_D,lista_Caminhos,lista_Nodos) * random.uniform(1.1,2)),
            "min_T": max(min_Throughput),
            "function_chain": func_list,
            "valor": valor
            }

    with open ("requisicoes.json","w") as outfile:
        json.dump(requisicoes, outfile, indent=4)

    with open ("funcoes.json","w") as outfile:
        json.dump(funcao, outfile, indent=4)

    with open ("implementacoes.json","w") as outfile:
        json.dump(implementacoes, outfile, indent=4)