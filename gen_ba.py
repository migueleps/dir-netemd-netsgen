import networkx as nx
import sys
import numpy as np

nnodes = [1250,2500,5000,10000]
densities = [10,20,40,80]

def check_density(net,expected_d):
    sum_deg = sum([deg for n, deg in net.degree()])
    avg_k = sum_deg/net.number_of_nodes()
    deviation = expected_d * 0.1
    return avg_k >= expected_d - deviation and avg_k <= expected_d + deviation

params = {1250:[5,10,20,41],2500:[5,10,20,41],5000:[5,10,20,40],10000:[5,10,20,40]}

for n in nnodes:
    param = params[n]
    for j,d in enumerate(densities):
        for i in range(10):
            nn = nx.barabasi_albert_graph(n,param[j])
            while not check_density(nn,d):
                nn = nx.barabasi_albert_graph(n,param[j])
            g = nx.convert_node_labels_to_integers(nn,first_label=1)
            ofile = "ba_{}_{}_{}.edges".format(n,d,i)
            nx.write_edgelist(g,ofile,data=False)
