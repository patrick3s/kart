"""Rótulos por ilha das partes do Dimi (Fase 3). Usa somente o NPZ original.
0 Corpo_Kart, 1 Cabeca, 2..5 Wheel_Front_Left, Wheel_Front_Right, Wheel_Rear_Left, Wheel_Rear_Right."""
import numpy as np
NOMES=["Corpo_Kart","Cabeca","Wheel_Front_Left","Wheel_Front_Right","Wheel_Rear_Left","Wheel_Rear_Right"]
# centros (Y, Z) do eixo de cada roda, por ajuste de círculo às faces externas (|X|>0.33); frente = -Y, esquerda = +X
CENTROS={2:(1,-0.2515,0.1288),3:(-1,-0.2511,0.1292),4:(1,0.2246,0.1311),5:(-1,0.2286,0.1282)}
CAB_FORA=[273,346,462,503,700]    # gola/capuz (textura azul) — ficam no corpo
CAB_DENTRO=[482,531,548,556]      # pele do pescoço abaixo de Z 0,44
def rotulos(co,comp):
    nc=int(comp.max())+1; ids=np.arange(nc)
    mins=np.full((nc,3),np.inf); maxs=np.full((nc,3),-np.inf)
    for k in range(3): np.minimum.at(mins[:,k],comp,co[:,k]); np.maximum.at(maxs[:,k],comp,co[:,k])
    cen=(mins+maxs)/2; lab=np.zeros(nc,np.int8)
    cab=((mins[:,2]>=0.44)&(maxs[:,2]<=0.76)&(np.abs(cen[:,0])<=0.16)&(mins[:,1]>=-0.17)&(maxs[:,1]<=0.23)
         &(mins[:,1]<0.165)&~np.isin(ids,CAB_FORA))|np.isin(ids,CAB_DENTRO)
    lab[cab]=1
    for w,(sx,cy,cz) in CENTROS.items():
        r=np.hypot(co[:,1]-cy,co[:,2]-cz); ax=co[:,0]*sx
        rmax=np.full(nc,-1.); np.maximum.at(rmax,comp,r)
        axmin=np.full(nc,9.); np.minimum.at(axmin,comp,ax)
        axmax=np.full(nc,-9.); np.maximum.at(axmax,comp,ax)
        roda=((rmax<=0.15)&(axmin>=0.268))|((rmax<=0.10)&(axmax>=0.30)&(axmin>=0.20))
        assert not (lab[roda]!=0).any(), "ilha em duas partes"
        lab[roda]=w
    return lab
