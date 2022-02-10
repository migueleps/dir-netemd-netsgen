import networkx as nx
import sys
import numpy as np

nnodes = [1250,2500,5000,10000]
densities = [10,20,40,80]
dim = 3

def check_density(net,expected_d):
    sum_deg = sum([deg for n, deg in net.degree()])
    avg_k = sum_deg/net.number_of_nodes()
    deviation = expected_d * 0.1
    return avg_k >= expected_d - deviation and avg_k <= expected_d + deviation

params = {1250:[0.131,0.172,0.213,0.28],2500:[0.101,0.134,0.169,0.215],5000:[0.085,0.105,0.135,0.17],10000:[0.066,0.08,0.103,0.13]}

for n in nnodes:
    print n
    param = params[n]
    for j,d in enumerate(densities):
        print d
        for i in range(10):
            print i
            nn = nx.random_geometric_graph(n,param[j],dim)
            error_counter = 1
            sum_k = 0
            while not check_density(nn,d):
                if error_counter > 20:
                    raise ValueError("choose different param for {},{} with average k {}".format(n,d,sum_k/error_counter))
                nn = nx.random_geometric_graph(n,param[j],dim)
                error_counter += 1
                sum_k += sum([deg for no,deg in nn.degree()])/n
            g = nx.convert_node_labels_to_integers(nn,first_label=1)
            ofile = "geom_{}_{}_{}.edges".format(n,d,i)
            nx.write_edgelist(g,ofile,data=False)
