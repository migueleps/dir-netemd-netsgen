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

params = {1250:[0.505,0.693,0.8,0.83],2500:[0.508,0.63,0.7,0.782],5000:[0.515,0.615,0.685,0.75],10000:[0.485,0.565,0.653,0.71]}

for n in nnodes:
    print n
    param = params[n]
    for j,d in enumerate(densities):
        print d
        for i in range(10):
            print i
            nn = nx.duplication_divergence_graph(n,param[j])
            error_counter = 1
            sum_k = 0
            while not check_density(nn,d):
                if error_counter > 20:
                    raise ValueError("choose different param for {},{} with average k {}".format(n,d,sum_k/error_counter))
                nn = nx.duplication_divergence_graph(n,param[j])
                error_counter += 1
                sum_k += sum([deg for no,deg in nn.degree()])/n 
            g = nx.convert_node_labels_to_integers(nn,first_label=1)
            ofile = "ddispo_{}_{}_{}.edges".format(n,d,i)
            nx.write_edgelist(g,ofile,data=False)
