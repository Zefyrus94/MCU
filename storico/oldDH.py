###LIBRARIES
import networkx as nx
from networkx.readwrite import json_graph
from random import uniform,randint
import numpy
from numpy import linalg as LA
import math as Math
import json
import os
from pathlib import Path
import time
import shutil
##
start_time = time.time()
###CLEAN
folder = './html/'
for filename in os.listdir(folder):
    file_path = os.path.join(folder, filename)
    try:
        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.unlink(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)
    except Exception as e:
        print('Failed to delete %s. Reason: %s' % (file_path, e))
folder = './tmp/'
for filename in os.listdir(folder):
    file_path = os.path.join(folder, filename)
    try:
        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.unlink(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)
    except Exception as e:
        print('Failed to delete %s. Reason: %s' % (file_path, e))
clear = lambda: os.system('cls') #on Windows System
clear()
###GRAPH
test=False
valorizzato=False
if(test and not valorizzato):
  with open('test.json') as json_file:
    data=json.load(json_file)
elif(valorizzato):
  with open('originale.json') as json_file:
      data=json.load(json_file)
else:
  G=nx.read_graphml('graph.graphml')
  data = json_graph.node_link_data(G)

##IABLES
width=1000
height=800
nodes=data['nodes']
links=data['links']

###FUNCTIONS
def getStartingPositions(nodes,links):
  for n in nodes:
      n['x']=uniform(200,width)
      n['y']=uniform(200,height)
      for l in links:
        if(l['source']==n['id']):
          l['s']={'x':n['x'],'y':n['y']}
        if(l['target']==n['id']):
          l['t']={'x':n['x'],'y':n['y']}
  return nodes
def chooseANode(max):
  rand=randint(0,max-1)
  it=0
  for n in nodes:
    if(it==rand):
      return n
    it=it+1
# returns true iff the line from (a,b)->(c,d) intersects with (p,q)->(r,s)
def intersects(a,b,c,d,p,q,r,s):
  det = (c - a) * (s - q) - (r - p) * (d - b)
  if (det == 0):
    #print("det 0")
    return False
  else:
    lambdA = ((s - q) * (r - a) + (p - r) * (s - b)) / det
    gamma = ((b - d) * (r - a) + (c - a) * (s - b)) / det
    #print("lambdA: "+str(lambdA)+"\ngamma: "+str(gamma))
    return (0 < lambdA and lambdA < 1) and (0 < gamma and gamma < 1)
def numberOfIntersections(nodes,links):
    res=0
    for k in links:
        #print("ciclo esterno")
        for l in links:
            #print("ciclo interno")
            """for m in nodes:
                if(m['id']==k['source']):
                    sourceK=m
                if(m['id']==k['target']):
                    targetK=m
                if(m['id']==l['source']):
                    sourceL=m
                if(m['id']==l['target']):
                    targetL=m"""
            #print(k['s'])
            try:
              skx=k['s']['x']
              sky=k['s']['y']
              #print(k['t'])
              tkx=k['t']['x']
              tky=k['t']['y']
              #print(l['s'])
              slx=l['s']['x']
              sly=l['s']['y']
              tlx=l['t']['x']
              tly=l['t']['y']
            except:
              print(k)
              print("-----")
              print(l)
              exit()
            if(intersects(skx,sky,tkx,tky,slx,sly,tlx,tly)):
                res=res+1
            """else:
              #print("l'arco "+sourceK['name']+", "+targetK['name']+" non interseca "+sourceL['name']+", "+targetL['name'])
              if(sourceK['name']=="Ant-Man" and targetK['name']=='Avengers: Endgame' and sourceL['name']=="Black Panther" and targetL['name']=='Ant-Man and the Wasp'):
                print("skx: "+str(skx)+"; sky: "+str(sky)+"\ntkx: "+str(tkx)+"; tky: "+str(tky)+"\nslx: "+str(slx)+"; sly: "+str(sly)+"\ntlx: "+str(tlx)+"; tly: "+str(tly))
                exit("l'arco "+sourceK['name']+", "+targetK['name']+" non interseca "+sourceL['name']+", "+targetL['name'])
    exit("res: "+str(res))"""
    return res
def distance_to_line(p0, p1, p2):
    x_diff = p2['x'] - p1['x']
    y_diff = p2['y'] - p1['y']
    num = abs(y_diff*p0['x'] - x_diff*p0['y'] + p2['x']*p1['y'] - p2['y']*p1['x'])
    den = Math.sqrt(y_diff**2 + x_diff**2)
    return num / den
#questa fase costa tanto 0.32 s circa con il grafo di prova di 52 nodi
# l'ideale è somma len archi ^2 bassa (ma non troppo); somma distanze tra coppie di nodi alta (ma non troppo);
# num incroci bassa
#distanza dai bordi non rispettata, quindi posta come condizione nello spostamento lungo la circonferenza di raggio T
# nel fine tuning considero anche la distanza punto linea tra nodo e archi vicini
def computeEnergy(nodes,links,logInfo):
  sac_time=time.time()
  width=1000
  height=800
  lambda1=8
  #lambda2=100
  lambda3=5
  lambda4=1000
  repulsiveTot=0
  #fromBordersTot=0
  edgeLenTot=0
  numCrossTot=0
  distanze=[]
  for u in nodes:
    ux=u['x']
    uy=u['y']
    posi=numpy.array([ux,uy])
    """dr=numpy.linalg.norm(posi-numpy.array([width,uy]))
    dl=numpy.linalg.norm(posi-numpy.array([0,uy]))
    dt=numpy.linalg.norm(posi-numpy.array([ux,0]))
    db=numpy.linalg.norm(posi-numpy.array([ux,height]))
    """
    """rt={'x':width,'y':0}
    rb={'x':width,'y':height}
    tl={'x':0,'y':0}
    tr={'x':width,'y':0}
    bl={'x':0,'y':height}
    br={'x':width,'y':height}
    lt={'x':0,'y':0}
    lb={'x':0,'y':height}
    dr=distance_to_line(u, rt, rb)
    dl=distance_to_line(u, lt, lb)
    dt=distance_to_line(u, tl, tr)
    db=distance_to_line(u, bl, br)
    """
    """
    if(dr==0):
      dr=1
    if(dl==0):
      dl=1
    if(dt==0):
      dt=1
    if(db==0):
      db=1
    fromBordersTot=fromBordersTot+lambda2*(1/pow(dr,2)+1/pow(dl,2)+1/pow(dt,2)+1/pow(db,2))"""
    for v in nodes:
      #se sono elementi diversi
      if(u['id']!=v['id']):
        vx=v['x']
        vy=v['y']
        posj=numpy.array([vx,vy])
        duv=numpy.linalg.norm(posi-posj)
        #se sono nello stesso punto, l'inverso della distanza è infinito, quindi ipotizzo un valore molto alto
        if(duv==0):
          iduv=1000
        else:
          iduv=1/pow(duv,2)
        repulsiveTot=repulsiveTot+lambda1*duv
        for l in links:
          if(l['source']==u['id'] and l['target']==v['id']):
            source=u
            target=v
            edgeLenTot=edgeLenTot+lambda3*pow(numpy.linalg.norm(posi-posj),2)
            break
 
  #questo costa circa 0.28 s
  numCrossTot=lambda4*numberOfIntersections(nodes,links)
  #print("--- %s Compute energy seconds ---" % (time.time() - sac_time))
  #exit("numCrossTot: "+str(numCrossTot))
  #exit("repulsiveTot: "+str(repulsiveTot)+"\nfromBordersTot: "+str(fromBordersTot)+"\nedgeLenTot: "+str(edgeLenTot)+"\nnumCrossTot: "+str(numCrossTot))
  #print(str(fromBordersTot))
  msg="r: "+str(repulsiveTot)+", e: "+str(edgeLenTot)+", c: "+str(numCrossTot)+"\n"+logInfo+"\n"
  log= open('./tmp/info.log',"a+")
  log.write(msg)
  log.close()
  tot=repulsiveTot+edgeLenTot+numCrossTot
  totMax=1.7976931348623157e+8#va normalizzata in [0,1]
  tot=tot/totMax
  return tot,numCrossTot
def computeFTEnergy(nodes,links,logInfo):
  tot,numCrossTot= computeEnergy(nodes,links,logInfo)
  nodeLinkDist=0
  gmin=60
  lambda5=1
  for v in nodes:
    for l in links:
      for n in nodes:
        if(n['id']==l['source']):
          source=n
        if(n['id']==l['target']):
          target=n
      dl=lambda5*distance_to_line(v, source, target)
      if(dl<gmin):
        nodeLinkDist=nodeLinkDist+dl
  totMax=1.7976931348623157e+8#va normalizzata in [0,1]
  tot=(tot+nodeLinkDist)/totMax
  return tot,numCrossTot
def move(node,rad,nodes,links):
  #print("sposto "+node['name'])
  #print("x: "+str(node['x'])+"y: "+str(node['y']))
  startx=node['x']
  starty=node['y']
  if(node['x']+rad>1400):
    startx=1400-rad-20#tolgo un margine
  elif(node['x']-rad<30):
    startx=30+rad+20#aggiungo un margine
  if(node['y']+rad>1000):
    starty=1000-rad-20#tolgo un margine
  elif(node['y']-rad<30):
    starty=30+rad+20#aggiungo un margine
  #radial base approach, mi muovo su una circonferenza: fa pochi spostamenti buoni
  """angle=2*Math.pi*uniform(0,1)#senza uniform mi muovo sempre a dx, cos 1 sin 0
  nx=startx+Math.cos(angle)*rad
  ny=starty+Math.sin(angle)*rad"""
  #approccio quadrato, mi muovo nell'area di un quadrato
  nx=uniform(startx-rad,startx+rad)
  ny=uniform(starty-rad,starty+rad)
  width=1000
  height=800
  maxNodeX=width
  minNodeX=0
  maxNodeY=height
  minNodeY=0
  log= open('./tmp/info.log',"a+")
  log.write("("+str(node['x'])+", "+str(node['y'])+") =>("+str(nx)+", "+str(ny)+")\n")
  log.close()
  for n in nodes:
      if(n['id']==node['id']):
        n['x']=nx
        n['y']=ny
        break
  for l in links:
      if(l['source']==node['id']):
        l['s']['x']=nx
        l['s']['y']=ny
      if(l['target']==node['id']):
        l['t']['x']=nx
        l['t']['y']=ny  
def moveBack(vc,vx,vy,nodes,links):
  for n in nodes:
    if(n['id']==vc['id']):
      n['x']=vx
      n['y']=vy
      break
  for l in links:
      if(l['source']==vc['id']):
        l['s']['x']=vx
        l['s']['y']=vx
      if(l['target']==vc['id']):
        l['t']['x']=vx
        l['t']['y']=vx
def fixNodePos(nodes):
    maxX=0
    maxY=0
    for v in nodes:
        if(v['x']<30):
            if(abs(v['x']-30)>maxX):
                maxX=abs(v['x']-30)
        if(v['y']<30):
            if(abs(v['y']-30)>maxY):
                maxY=abs(v['y']-30)
    for v in nodes:
        v['x']=v['x']+100+maxX
        v['y']=v['y']+100+maxY
def saveConfiguration(filename,data):
  fileContent = Path('parent.html').read_text()
  fileContent=fileContent.replace("@@@@@@", filename+".json")
  html= open('./html/'+filename+'.html',"w+")
  html.write(fileContent)
  html.close()
  ##json
  content= open('./tmp/'+filename+'.json',"w+")
  content.write(json.dumps(data))
  content.close()
def polyn(input):
  return 25*input#meglio 30, ma troppo lento per grossi input
def simulatedAnnealing(data):
    #exit(str(len(data['nodes'])))
    #inizio con posizioni casuali dei nodes
    nodes=data['nodes']
    links=data['links']
    valorizzato=False
    if(not valorizzato):
        nodes=getStartingPositions(nodes,links)
        f= open('originale.json',"w+")
        f.write(json.dumps(data))
        f.close()
    else:
      for n in nodes:
        for l in links:
          if(l['source']==n['id']):
            l['s']={'x':n['x'],'y':n['y']}
          if(l['target']==n['id']):
            l['t']={'x':n['x'],'y':n['y']}
    T=100
    stages=11
    fineTuningStages=4
    numNodes=len(nodes)
    currentStage=0
    fineTuningStage=0
    numMoves=polyn(numNodes)
    currentMove=0
    gamma=0.8
    fuoriArea=False
    ###
    vc=chooseANode(numNodes)
    prevEnergy,ncp=computeEnergy(nodes,links,'')
    if(ncp<=2000000):
      saveConfiguration('outer',data)
    while(currentStage<=stages and not fuoriArea):
        sao_time=time.time()
        currentMove=0
        #print("currentStage: "+str(currentStage)+"\nT: "+str(T))
        while(currentMove<=numMoves and not fuoriArea):
            sai_time=time.time()
            print("currentStage: "+str(currentStage)+"\nT: "+str(T))
            print("currentMove: "+str(currentMove))
            #print(vc)
            vx=vc['x']
            vy=vc['y']
            """for n in nodes:
              if(n['x']>1400 or n['x']<0 or n['y']>1200 or n['y']<0):
                  print("fuori area, vado in fine tuning")
                  fuoriArea=True
                  fineTuningStages=fineTuningStages+(stages-currentStage)
                  print("fineTuningStages: "+str(fineTuningStages))
                  print("T: "+str(T))
                  T=100
                  break"""
            move(vc,T,nodes,links)
            newEnergy,ncn=computeEnergy(nodes,links,"s"+str(currentStage)+"i"+str(currentMove)+".json")
            de=newEnergy-prevEnergy
            #accetta la configurazione attuale
            #print("de: "+str(de))
            if(ncn<=ncp):
              ncp=ncn
              saveConfiguration('K_s'+str(currentStage)+'i'+str(currentMove),data)
            if(de<0):
                """if(fuoriArea):
                  moveBack(vc,vx,vy,nodes,links)
                  fineTuningStages=fineTuningStages+(stages-currentStage)
                  print("fineTuningStages: "+str(fineTuningStages))
                  print("T: "+str(T))
                  T=100
                  break"""
                prevEnergy=newEnergy
                vc=chooseANode(numNodes)
                #if(currentMove<10):
                saveConfiguration('s'+str(currentStage)+'i'+str(currentMove),data)
            elif(uniform(0,1)<Math.exp(-de/T)):
                #    print("accetto la configurazione, anche se è peggio")
                """if(fuoriArea):
                  moveBack(vc,vx,vy,nodes,links)
                  fineTuningStages=fineTuningStages+(stages-currentStage)
                  print("fineTuningStages: "+str(fineTuningStages))
                  print("T: "+str(T))
                  T=100
                  break"""
                vc=chooseANode(numNodes)
            else:
                #print("move back")
                moveBack(vc,vx,vy,nodes,links)
            print("--- %s seconds ---" % (time.time() - sai_time))#0.6s a iterazione=>0.14s
            currentMove=currentMove+1
        currentStage=currentStage+1
        print("--- %s seconds ---" % (time.time() - sao_time))
        T=gamma*T
    #fine-tuning phase
    #exit("temperatura: "+str(T))
    currentStage=0
    #vc=chooseANode(numNodes)
    #prevEnergy=computeFTEnergy(nodes,links)
    T=100
    prevEnergy,ncp=computeFTEnergy(nodes,links,str(currentStage)+str(currentMove))
    while(currentStage<=fineTuningStages):
        currentMove=0
        while(currentMove<=numMoves):
            print("currentStage FT: "+str(currentStage))
            print("currentMove 2: "+str(currentMove))
            vx=vc['x']
            vy=vc['y']
            move(vc,T,nodes,links)
            newEnergy,ncn=computeFTEnergy(nodes,links,str(currentStage)+str(currentMove))
            if(ncn<=ncp):
              ncp=ncn
              saveConfiguration('K_FT_s'+str(currentStage)+'i'+str(currentMove),data)
            de=newEnergy-prevEnergy
            #accetta la configurazione attuale
            if(de<0):
                prevEnergy=newEnergy
                saveConfiguration('FT_s'+str(currentStage)+'i'+str(currentMove),data)
                vc=chooseANode(numNodes)
            else:
                moveBack(vc,vx,vy,nodes,links)
            currentMove=currentMove+1
        currentStage=currentStage+1
simulatedAnnealing(data)
#fixNodePos(nodes)
minimo=50
massimo=0
for n in nodes:
  if(n['x']<minimo):
    minimo=n['x']
  if(n['x']>massimo):
    massimo=n['x']
diff=massimo-minimo
exit("diff: "+str(diff))
f= open('res.json',"w+")
f.write(json.dumps(data))
f.close()
print("--- %s seconds ---" % (time.time() - start_time))
print("fine")