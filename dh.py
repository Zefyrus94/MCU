###LIBRARIES
import subprocess
import sys
import importlib
modnames = ['networkx', 'pathlib','flask']

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

pkgs = ['networkx', 'pathlib','flask']
for lib in pkgs:
    try:
        globals()[lib] = importlib.import_module(lib)
    except ImportError:
        install(lib)

#import networkx as nx
from networkx.readwrite import json_graph
from random import uniform,randint,shuffle
#import numpy
#from numpy import linalg as LA
import math as Math
import json
import os
from pathlib import Path
import time
import shutil
import datetime
from flask import Flask, render_template, request, jsonify,send_file
#from flask_cors import CORS

#app = Flask(__name__)
#CORS(app)
app = Flask(__name__)


###CLEAN
def cleanFiles(folder):
	for filename in os.listdir(folder):
	    file_path = os.path.join(folder, filename)
	    try:
	        if os.path.isfile(file_path) or os.path.islink(file_path):
	            os.unlink(file_path)
	        elif os.path.isdir(file_path):
	            shutil.rmtree(file_path)
	    except Exception as e:
	        print('Failed to delete %s. Reason: %s' % (file_path, e))
"""folder = './html/'
cleanFiles(folder)
folder = './tmp/'
cleanFiles(folder)"""
##
clear = lambda: os.system('cls') #on Windows System
clear()
###GRAPH
"""G=nx.read_graphml('graph.graphml')
data = json_graph.node_link_data(G)"""
###

def transform(links,id2num):
	for l in links:
		l['source']=id2num[l['source']]
		l['target']=id2num[l['target']]
	return links
def transformNodes(nodes,id2num):
	for n in nodes:
		n['id']=id2num[n['id']]
	return nodes
def neighbors(links,node):
	neighs=[]
	for l in links:
		if(l['source']==node):
			neighs.append(l['target'])
		elif(l['target']==node):
			neighs.append(l['source'])
	return neighs
def inizializza(num):
	fPosult=[]
	i=0
	while(i<num):
		fPosult.append(i)
		i=i+1
	return fPosult
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
def point_segment_dist(p0x, p0y, p1x, p1y, p2x, p2y):
    x_diff = p2x - p1x
    y_diff = p2y - p1y
    num = abs(y_diff*p0x - x_diff*p0y + p2x*p1y - p2y*p1x)
    den = Math.sqrt(y_diff**2 + x_diff**2)
    if(den==0):
    	return float('inf')
    return num / den
def takeTheOther(links,link,node):
	for l in links:
		if(l==link):
			if(l['source']==node):
				other=l['target']
				return other
			elif(l['target']==node):
				other=l['source']
				return other
def incidents(links,node):
	incs=[]
	for l in links:
		if(l['source']==node or l['target']==node):
			incs.append(l)
	return incs
def saveConfiguration(filename,data):
	fileContent = Path('parentServer.html').read_text()
	fileContent=fileContent.replace("@@@@@@", filename+".json")
	html= open('./html/'+filename+'.html',"w+")
	html.write(fileContent)
	html.close()
	##json
	content= open('./tmp/'+filename+'.json',"w+")
	content.write(json.dumps(data))
	content.close()
def energy(v,old_x,old_y,new_x,new_y,lambda1,lambda2,lambda3,lambda4,numNodes,numEdges,fineTuning,fPos,links,nodes):
	de=0.0
	##distanza tra nodi
	u=0
	while(u<numNodes):
		#print("distanza tra nodi, u: "+str(u)+" v: "+str(v))
		if (u == v):
			u=u+1
			continue
		#print("a")
		odx = old_x - fPos[u][0]
		ody = old_y - fPos[u][1]
		dx = new_x - fPos[u][0]
		dy = new_y - fPos[u][1]
		odist2 = odx * odx + ody * ody;
		dist2 = dx * dx + dy * dy;
		#print("odist2: "+str(odist2)+"\ndist2: "+str(dist2))
		if(dist2==0):
			firstDist=float("inf")
		else:
			firstDist=lambda1 / dist2
		de += firstDist - lambda1 / odist2
		#print("de: "+str(de))
		u=u+1
	#print("Ok")
	##edge length
	neis=neighbors(links, v)
	numneis=len(neis)
	j=0
	while(j<numneis):
		#print("edge length")
		u=neis[j];
		odx = old_x - fPos[u][0]
		ody = old_y - fPos[u][1]
		odist2 = odx * odx + ody * ody
		dx = new_x - fPos[u][0]
		dy = new_y - fPos[u][1]
		dist2 = dx * dx + dy * dy
		de += lambda2 * (dist2 - odist2)
		j=j+1

	##edge crossing metric  
	no=0
	j=0
	while(j<numneis):
		u = neis[j];
		u_x = fPos[u][0]
		u_y = fPos[u][1]
		e=0
		while(e<numEdges):
			edge=links[e]
			u1 = edge['source']
			u2 = edge['target']
			if (u1 == v or u2 == v or u1 == u or u2 == u):
				e=e+1
				continue
			"""i=0
			fine=len(fPos)-1
			while(i<fine):
				print(str(i)+": "+str(fPos[i][0])+", "+str(fPos[i][1]))
				i=i+1"""
			u1_x = fPos[u1][0]
			u1_y = fPos[u1][1]
			u2_x = fPos[u2][0]
			u2_y = fPos[u2][1]
			no -= intersects(old_x, old_y, u_x, u_y, 
						u1_x, u1_y, u2_x, u2_y);
			no += intersects(new_x, new_y, u_x, u_y,
						u1_x, u1_y, u2_x, u2_y);
			e=e+1
		j=j+1
	de = de+lambda3 * no

	##edge distance metric, solo per fine tuning    
	if (fineTuning):
		#All non-incident edges from the moved 'v'
		e=0
		while(e<numEdges):
			edge=links[e]
			u1 = edge['source']
			u2 = edge['target']
			if (u1 == v or u2 == v):
				e=e+1
				continue
			u1_x = fPos[u1][0]
			u1_y = fPos[u1][1]
			u2_x = fPos[u2][0]
			u2_y = fPos[u2][1]
			d_ev = point_segment_dist(old_x, old_y, u1_x, u1_y,
							u2_x, u2_y)
			if(d_ev==0):
				toSubtract=float('inf')
			else:
				toSubtract=lambda4 / d_ev
			de -= toSubtract
			d_ev = point_segment_dist(new_x, new_y, u1_x, u1_y,
							u2_x, u2_y)
			if(d_ev==0):
				toAdd=float('inf')
			else:
				toAdd=lambda4 / d_ev
			de = de+toAdd
			e=e+1

		#All other nodes from all of v's incident edges
		incs=incidents(links, v)#incident(graph, v)#gli archi con v come source o target
		no=len(incs)
		e=0
		while(e<no):
			mye=incs[e];
			u=takeTheOther(incs, mye,v)
			u_x=fPos[u][0]
			u_y=fPos[u][1]
			w=0
			while(w<numNodes):
				if (w == v or w == u):
					w=w+1
					continue
				w_x=fPos[w][0]
				w_y=fPos[w][1]
				d_ev = point_segment_dist(w_x, w_y, old_x,
								old_y, u_x, u_y)
				if(d_ev==0):
					toSubtract=float('inf')
				else:
					toSubtract=lambda4 / d_ev
				de -= toSubtract
				d_ev = point_segment_dist(w_x, w_y, new_x, new_y,
							  u_x, u_y)
				if(d_ev==0):
					toAdd=float('inf')
				else:
					toAdd=lambda4 / d_ev
				de = de+toAdd;
				w=w+1
			e=e+1
	return de
def DH(graph,cooling,lambda1,lambda2,lambda3,lambda4):
	#VARIABILI
	links=graph['links']
	nodes=graph['nodes']
	numNodes = len(nodes)
	numEdges = len(links)
	#cooling=0.75#pre: 0.75; 0.9^x*100=10=> x=log_0.9(10/100); con 0.99, circa 298*2 fasi totali (30 min di esec)
	saPhases=Math.log(5/100,cooling)#10#10
	ftPhases=max(saPhases, Math.log(numNodes,2))#10
	#width = 2000#Math.sqrt(numNodes) * 10
	height = width = 2000
	fineTuning=0
	radius=width / 2
	fineTuning_factor=0.01
	min_x=width/2
	max_x=-width/2
	min_y=height/2
	max_y=-height/2
	numProve = 30#3
	density=numEdges/(numNodes*(numNodes-1))
	"""lambda1 = 10000#pre: 10000
	lambda2 = density/1000#0.0001#den/10
	lambda3 = 10-Math.sqrt(density)#1.0#1-sqrt(den)
	lambda4 = (40-density)/5#0.2#(1-den)/5"""
	nodesNum=inizializza(numNodes)# nodesNum è un vettore di numeri da 0 a numNodes-1
	proveNum=inizializza(numProve)#proveNum è un vettore di numeri da 0 a 29
	proveX=[]
	proveY=[]
	#inizializzo le posizioni in fPos, è una matrice di dimensione n*2 (nodi,posizioni)
	fPos=[]
	i=0
	while(i<numNodes):
		fPos.append(i)
		fPos[i]=[]
		fPos[i].append(0)
		fPos[i].append(1)
		i=i+1
	i=0
	while(i<numNodes):
		x = fPos[i][0] = uniform(-width/2, width/2);
		y = fPos[i][1] = uniform(-height/2, height/2);
		if (x < min_x):
			min_x = x
		elif (x > max_x):
			max_x = x
		if (y < min_y):
			min_y = y
		elif (y > max_y):
			max_y = y
		i=i+1
	#le x e le y lungo cui mi sposterò
	i=0
	while(i<numProve):
		angle=2 * Math.pi / numProve * i
		proveX.append(Math.cos(angle))#tryx e y sono vettori di 30 elementi
		proveY.append(Math.sin(angle))
		i=i+1
	#phase è la fase, il phase in cui mi trovo
	phase=0
	while(phase<saPhases+ftPhases):
		shuffle(nodesNum)#mischio il vettore con i nodi 0...51
		fineTuning = phase >= saPhases
		#in fine tuning il raggio è inizializzato come il minimo tra gli intervalli x e y
		if (fineTuning): 
		  fx=max_x - min_x
		  fy=max_y - min_y
		  radius = fineTuning_factor*min(fx,fy)
		#questa azione è compiuta su tutti i nodi
		p=0
		while(p<numNodes):
			v=nodesNum[p]#prendo il p-esimo nodo, v
			shuffle(proveNum)#mischio il vettore di numeri da 0 a 29
			t=0
			#faccio delle prove
			while(t<numProve):
				ti=proveNum[t]
				#provo a muovere il nodo v
				old_x = fPos[v][0]
				old_y = fPos[v][1]
				new_x = old_x + radius * proveX[ti];
				new_y = old_y + radius * proveY[ti];

				if (new_x < -width /2):
					new_x = -width/2 - 1e-6
				if (new_x >  width /2):
					new_x =  width/2 - 1e-6
				if (new_y < -height/2):
					new_y = -height/2 - 1e-6
				if (new_y >  height/2):
					new_y =  height/2 - 1e-6

				##METRICHE
				de=energy(v,old_x,old_y,new_x,new_y,lambda1,lambda2,lambda3,lambda4,numNodes,numEdges,fineTuning,fPos,links,nodes)
				#FINE METRICHE
				#accettazione; con probabilità se non in fine tuning
				if (de < 0 or
				(not fineTuning and uniform(0,1) < Math.exp(-de/radius))):
					fPos[v][0] = new_x
					fPos[v][1] = new_y
					if (new_x < min_x):
						min_x = new_x
					elif (new_x > max_x):
						max_x = new_x
					if (new_y < min_y):
						min_y = new_y
					elif (new_y > max_y):
						max_y = new_y
				t=t+1
			p=p+1
		#raffreddamento, restringo il raggio
		radius *= cooling
		phase=phase+1
	return fPos
###fine funzioni
@app.route('/', methods = ['GET', 'POST'])
@app.route('/index.html')
def index():
	if request.method == 'POST':
		storage=request.json['file']
		data=json.loads(storage)
		cooling=request.json['cooling']
		lambda1=request.json['l1']
		lambda2=request.json['l2']
		lambda3=request.json['l3']
		lambda4=request.json['l4']

		cooling=float(cooling.strip('"'))
		lambda1=int(lambda1.strip('"'))
		lambda2=float(lambda2.strip('"'))
		lambda3=float(lambda3.strip('"'))
		lambda4=float(lambda4.strip('"'))

		links=data['links']
		nodes=data['nodes']
		id2num={}
		i=0
		for n in nodes:
			nid=n['id']
			if(nid not in(id2num)):
				id2num[nid]=i
				i=i+1
		links=transform(links,id2num)
		nodes=transformNodes(nodes,id2num)
		start_time = time.time()
		print(str(start_time))
		newData={"nodes":nodes,"links":links}
		#print(newData)
		print("newData: "+str(newData)+"\ncooling: "+str(cooling)+"\nlambda1: "+str(lambda1)+"\nlambda2: "+str(lambda2)+"\nlambda3: "+str(lambda3)+"\nlambda4: "+str(lambda4))
		fPos=DH(newData,cooling,10000,lambda2,lambda3,lambda4)
		distanceFromBorder=100
		minx=distanceFromBorder
		miny=distanceFromBorder
		maxX=0
		for f in fPos:
			if(f[0]<minx):
				minx=f[0]
			if(f[1]<miny):
				miny=f[1]
			if(f[0]>maxX):
				maxX=f[0]
		i=0
		newNodes=[]
		for n in nodes:
			n['x']=fPos[i][0]+abs(distanceFromBorder-minx)
			n['y']=fPos[i][1]+abs(distanceFromBorder-miny)
			i=i+1
			newNodes.append(n)
		print("--- %s seconds ---" % (time.time() - start_time))
		count=0
		for l in links:
			for m in links:
				for n in nodes:
					if(n['id']==l['source']):
						slx=n['x']
						sly=n['y']
					if(n['id']==l['target']):
						tlx=n['x']
						tly=n['y']
					if(n['id']==m['source']):
						smx=n['x']
						smy=n['y']
					if(n['id']==m['target']):
						tmx=n['x']
						tmy=n['y']
				if(intersects(slx,sly,tlx,tly,smx,smy,tmx,tmy)):
					count+=1
		newData={"nodes":newNodes,"links":links}
		print("incroci totali: "+str(count))
		print("fine")
		now=datetime.datetime.now()
		ora=str(now.hour)+"-"+str(now.minute)
		filename="dh"+str(count)+"_"+ora
		#print(data['nodes'])
		saveConfiguration(filename,newData)
		fileContent = Path('parentServer.html').read_text()
		fileContent=fileContent.replace("@@@@@@", filename+".json")
		imgPos=maxX+abs(distanceFromBorder-minx)+250
		fileContent=fileContent.replace("####", str(imgPos))
		html= open('./templates/'+filename+'.html',"w+")
		html.write(fileContent)
		html.close()
		content= open('./templates/'+filename+'.json',"w+")
		content.write(json.dumps(newData))
		content.close()
		return jsonify(filename)
	else:
		if(len(request.args)==1):
			filename=request.args['f']
			return render_template(filename)
		elif(len(request.args)==2):
			filename=request.args['f']
			print(filename)
			with open('tmp/'+filename) as json_file:
				newData=json.load(json_file)
			return jsonify(newData)
		else:	
			return render_template('index.html')


@app.route('/img')
def image():
	idim=request.args['id']
	response = send_file('img/'+idim, mimetype='image/gif')
	return response
@app.route('/graphml', methods = ['POST'])
def graphml():
  storage=request.json['file']
  print(storage)
  print("\n======================\n")
  ml= open('./tmp/graph.graphml',"w+")
  ml.write(storage)
  ml.close()
  G=networkx.read_graphml('./tmp/graph.graphml')
  data = json_graph.node_link_data(G)
  print(data)
  return data
if __name__ == "__main__":
    app.run()


    


