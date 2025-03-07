import gerador_topologia
import gerador_req  
import ILP_Full
import ILP_FixPos
import ILP_FixPart

count = 0

for nro_nodos in range(10, 21, 5):
    


    result = 0
    stop = False
    

    for i in range(1):
        
        gerador_topologia.gerador_Topologia(nro_nodos,int(nro_nodos*1.3))
        gerador_req.main()
        result_full, total_time, mount_time = ILP_Full.main()
        result = result_full.ObjVal
        print("Full: ", result)
        result_pos, total_time, mount_time = ILP_FixPos.main()
        result = result_pos.ObjVal
        print("FixPos: ", result)
        result_part, total_time, mount_time = ILP_FixPart.main()
        result = result_part.ObjVal
        print("FixPart: ", result)
        if result_full.ObjVal < result_pos.ObjVal or result_full.ObjVal < result_part.ObjVal:
            count += 1
        print("Count: ", count)
        if int(result) == 0:
            break
        
    if int(result) == 0:
        break

