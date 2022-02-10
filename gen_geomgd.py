import networkx as nx
import numpy as np
import random as rd
import math
import sys

def d3d(p1,p2):#euclidean distance
    return math.sqrt((p1[0]-p2[0])**2+(p1[1]-p2[1])**2+(p1[2]-p2[2])**2)

def normalize(x):
    return x / np.linalg.norm(x)

def geo3dDD(N,E):#creates a 3D geometric duplication divergence graph with N nodes and E edges 
    p={}#dict of node positions
    for i in range(5):#initialize 5 points at random positions
        p[i]=np.array([rd.random(),rd.random(),rd.random()])
    for i in range(5,N):#create new nodes by duplication divergence
        k=rd.choice(range(i))
        p[i]=p[k]+2*rd.random()*normalize(np.array([rd.random()-0.5,rd.random()-0.5,rd.random()-0.5]))#positio of new node is the position of the parrent 
        #plus a vector with random direction and random length between O and 2
    D=[]
    for i in range(N):
        for j in range(i+1,N):
            D.append(d3d(p[i],p[j])) # get array of pairwise distances 
    r=np.sort(np.array(D), axis=None)[E-1] # find radius at which the geometric graph has E edges 
    print(r)
    g=nx.random_geometric_graph(N,r,dim=3,pos=p)
    print('GEODD:',g.number_of_edges())
    return(g)


def check_density(net,expected_d):
    sum_deg = sum([deg for n,deg in net.degree()])
    avg_k = sum_deg/net.number_of_nodes()
    deviation = expected_d * 0.1
    return avg_k >= expected_d - deviation and avg_k <= expected_d + deviation

for s in [1250,2500,5000,10000]:
    for d in [10,20,40,80]:
        for i in range(0,10):
            e = s*d/2
            g = geo3dDD(s,e)
            error_counter = 1
            while not check_density(g,d):
                if error_counter >= 10:
                    raise ValueError("check e for {},{}".format(s,d))
                g = geo3dDD(s,e)
                error_counter += 1
            g = nx.convert_node_labels_to_integers(g,first_label=1)
            ofile = "geomgd_{}_{}_{}.edges".format(s,d,i)
            nx.write_edgelist(g,ofile,data=False)
