import numpy as np, json, sys
z=np.load(sys.argv[1]); co=z["co"]; comp=z["components"]; ed=z["edges"]
nc=comp.max()+1; cnt=np.bincount(comp)
mins=np.full((nc,3),np.inf); maxs=np.full((nc,3),-np.inf)
for k in range(3): np.minimum.at(mins[:,k],comp,co[:,k]); np.maximum.at(maxs[:,k],comp,co[:,k])
cen=(mins+maxs)/2
# rodas: ilhas inteiramente fora da carroceria lateral, baixas
wheel=(np.abs(mins[:,0])>0.0)&((mins[:,0]>0.255)|(maxs[:,0]<-0.255))&(maxs[:,2]<0.30)
res={}
for sx,nx in((1,"Left"),(-1,"Right")):
  for sy,ny in((-1,"Front"),(1,"Rear")):
    sel=wheel&(np.sign(cen[:,0])==sx)&(np.sign(cen[:,1])==sy)
    ids=np.where(sel)[0]
    if len(ids)==0: res[f"Wheel_{ny}_{nx}"]=None; continue
    mn=mins[ids].min(0); mx=maxs[ids].max(0)
    res[f"Wheel_{ny}_{nx}"]={"ilhas":len(ids),"v":int(cnt[ids].sum()),"min":mn.round(4).tolist(),"max":mx.round(4).tolist(),"centro_bbox":((mn+mx)/2).round(4).tolist(),"diam_yz":[round(float(mx[1]-mn[1]),4),round(float(mx[2]-mn[2]),4)]}
# ilhas próximas das rodas que não entraram (possível ligação com suspensão/carroceria)
near=(~wheel)&(maxs[:,2]<0.30)&(np.abs(cen[:,0])>0.22)
res["ilhas_vizinhas_fora_do_criterio"]=[{"id":int(i),"v":int(cnt[i]),"min":mins[i].round(3).tolist(),"max":maxs[i].round(3).tolist()} for i in np.where(near)[0][:30]]
# distribuição em altura para localizar cabeça
hz=[(round(t,2),int(cnt[(mins[:,2]>=t)].sum()),int((mins[:,2]>=t).sum())) for t in (0.40,0.42,0.44,0.46,0.48,0.50)]
res["ilhas_acima_de_z"]=hz
up=np.where(mins[:,2]>0.42)[0]
res["ilhas_acima_042"]=[{"id":int(i),"v":int(cnt[i]),"min":mins[i].round(3).tolist(),"max":maxs[i].round(3).tolist()} for i in up[np.argsort(-cnt[up])][:45]]
print(json.dumps(res,ensure_ascii=False))
