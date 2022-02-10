import networkx as nx
import sys
import numpy as np
import random as rd
import math

nnodes = [1250,2500,5000,10000]
densities = [10,20,40,80]
p=0.05

def DD2(N,pr,pn):
    g=nx.Graph()
    g.add_edge(0,1)
    g.add_edge(0,2)
    while g.number_of_nodes() < N:
        node = rd.choice(range(g.number_of_nodes()))
        dup2(node,g,pr,pn)
    print("DD2: ",N,pr,pn,g.number_of_edges(),sum([deg for no,deg in g.degree()])/float(N))
    return g

def dup2(node,G,pr,pn):
    new=G.number_of_nodes()
    G.add_node(new)
    neighs = list(G.neighbors(node))
    for i in neighs:
        G.add_edge(new,i)
        t = rd.random()
        if t<pr:
            G.remove_edge(new,i)
        elif t>1-pr:
            G.remove_edge(node,i)
    if rd.random() < pn:
        G.add_edge(node,new)
    G.remove_nodes_from(list(nx.isolates(G)))
    

def check_density(net,expected_d):
    sum_deg = sum([deg for n, deg in net.degree()])
    avg_k = sum_deg/float(net.number_of_nodes())
    deviation = min(3,expected_d * 0.1)
    return avg_k >= expected_d - deviation and avg_k <= expected_d + deviation

params = {1250:[0.182,0.16,0.13,0.08],2500:[0.21,0.175,0.14,0.1],5000:[0.21,0.175,0.14,0.13],10000:[0.22,0.18,0.17,0.128]}

for n in nnodes:
    print n
    param = params[n]
    for j,d in enumerate(densities):
        print d
        for i in range(10):
            print i
            nn = DD2(n,param[j],p)
            error_counter = 1
            sum_k = 0
            while not check_density(nn,d):
                sum_k += sum([deg for no,deg in nn.degree()])/float(n)
                if error_counter > 25:
                    raise ValueError("choose different param for {},{} with average k {}".format(n,d,sum_k/float(error_counter)))
                nn = DD2(n,param[j],p)
                error_counter += 1
            g = nx.convert_node_labels_to_integers(nn,first_label=1)
            ofile = "ddvazq_{}_{}_{}.edges".format(n,d,i)
            nx.write_edgelist(g,ofile,data=False)
