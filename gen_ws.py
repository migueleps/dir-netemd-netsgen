import networkx as nx
import sys
import numpy as np

nnodes = [1250,2500,5000,10000]
densities = [10,20,40,80]
p = 0.05

def check_density(net,expected_d):
    sum_deg = sum([deg for n, deg in net.degree()])
    avg_k = sum_deg/net.number_of_nodes()
    deviation = expected_d * 0.1
    return avg_k >= expected_d - deviation and avg_k <= expected_d + deviation

for n in nnodes:
    print n
    for j,d in enumerate(densities):
        print d
        for i in range(10):
            print i
            nn = nx.watts_strogatz_graph(n,d,p)
            error_counter = 1
            while not check_density(nn,d):
                if error_counter >= 10:
                    raise ValueError("wrong param for {},{}".format(n,d))
                nn = nx.watts_strogatz_graph(n,d,p)
                error_counter += 1
            g = nx.convert_node_labels_to_integers(nn,first_label=1)
            ofile = "ws_{}_{}_{}.edges".format(n,d,i)
            nx.write_edgelist(g,ofile,data=False)
