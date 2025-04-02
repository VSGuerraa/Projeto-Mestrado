import ILP_Full
import ILP_FixPos
import ILP_FixPart
import gerador_topologia
import gerador_req
import csv
import json
import gurobipy as gp

nro_topologias = 10
nro_replicas = 15
    
for nro_nodos in range(10, 31, 5):
    
    for top in range(nro_topologias):
        
        topologia_inicial = gerador_topologia.gerador_Topologia(nro_nodos,int(nro_nodos*1.3))

        gerador_req.main()
        
        result, total_time, mount_time = ILP_Full.main()
        
        print(result.ObjVal)
        
        aloc = []
        
        for v in result.getVars():
            if v.X > 0.5:
                aloc.append(v.VarName)
                
        with open('ILP_Compare.csv', 'a+', newline='') as csv_file:
            writer = csv.writer(csv_file)        
            writer.writerow(['Full', result.ObjVal, result.ObjBound, total_time, mount_time, aloc])
            
        
        for rep in range(nro_replicas):
            
            gerador_topologia.gerador_Topologia(nro_nodos,int(nro_nodos*1.3), topologia_inicial)
            
            result, total_time, mount_time = ILP_FixPos.main()
            aloc = []
            for v in result.getVars():
                if v.X > 0.5:
                    aloc.append(v.VarName)
            with open('ILP_Compare.csv', 'a+', newline='') as csv_file:
                writer = csv.writer(csv_file)
                writer.writerow(['FixPos', result.ObjVal, result.ObjBound, total_time, mount_time, aloc])
            
            result, total_time, mount_time = ILP_FixPart.main()
            aloc = []
            for v in result.getVars():
                if v.X >0.5:
                    aloc.append(v.VarName)
            with open('ILP_Compare.csv', 'a+', newline='') as csv_file:
                writer = csv.writer(csv_file)
                writer.writerow(['FixPart', result.ObjVal, result.ObjBound, total_time, mount_time, aloc])
        
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
        
            
        with open('requisicoes.json', 'r') as json_file:
            req = json.load(json_file)  
            csv_row = []
            for req, req_data in req.items():
                csv_row.append(req_data)
        
        with open('ILP_Compare.csv', 'a+', newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(csv_row)
        
            
    

