import ILP_Full
import ILP_FixPos
import ILP_FixPart
import time
import gerador_topologia
import Projeto

nro_nodos = 10

print("Topologia com 1.3x Links")
gerador_topologia.gerador_Topologia(nro_nodos,int(nro_nodos*1.3))
Projeto.gerador_Req(nro_nodos, nro_nodos * 10)