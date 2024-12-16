import ILP_Full
import ILP_FixPos
import ILP_FixPart
import time
import gerador_topologia

print("Topologia com 1.3x Links")
gerador_topologia.gerador_Topologia(20,26)
ILP_Full.main()
ILP_FixPos.main()
ILP_FixPart.main()
