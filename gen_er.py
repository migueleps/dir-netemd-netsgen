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

params = {1250:[6250,12500,25000,50000],
2500:[12500,25000,50000,100000],
5000:[25000,50000,100000,200000],
10000:[50000,100000,200000,400000]}

for n in nnodes:
    param = params[n]
    for j,d in enumerate(densities):
        for i in range(10):
            nn = nx.gnm_random_graph(n,param[j])
            error_counter = 1
            while not check_density(nn,d):
                if error_counter >= 10:
                    raise ValueError("wrong e for {},{}".format(n,d))
                nn = nx.gnm_random_graph(n,param[j])
                error_counter += 1
            g = nx.convert_node_labels_to_integers(nn,first_label=1)
            ofile = "er_{}_{}_{}.edges".format(n,d,i)
            nx.write_edgelist(g,ofile,data=False)
