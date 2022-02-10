import networkx as nx
import sys
import numpy as np
import random as rand

nnodes = [1250,2500,5000,10000]
densities = [10,20,40,80]

rand.seed()

def check_density(net,expected_d):
    sum_deg = sum([deg for n, deg in net.degree()])
    avg_k = sum_deg/net.number_of_nodes()
    deviation = expected_d * 0.1
    return avg_k >= expected_d - deviation and avg_k <= expected_d + deviation

def find_4(g):
    s1 = 0
    s2 = 0
    t1 = 0
    t2 = 0
    numNodes = g.number_of_nodes();

    s1 = rand.randint(1,numNodes)
    s1_out_edges=[d for o,d in g.edges(s1)]
    while len(s1_out_edges) == 0 or len(s1_out_edges) >= numNodes-1:
        s1 = rand.randint(1,numNodes)
        s1_out_edges=[d for o,d in g.edges(s1)]

    t1= s1_out_edges[rand.randint(0,len(s1_out_edges)-1)]
    while_breaker = 0
    t1_out_edges=[d for o,d in g.edges(t1)]
    while len(t1_out_edges) >= numNodes - 1 and while_breaker < 2*len(s1_out_edges):
        t1= s1_out_edges[rand.randint(0,len(s1_out_edges)-1)]
        t1_out_edges=[d for o,d in g.edges(t1)]
        while_breaker+=1

    if while_breaker == 2*len(s1_out_edges):
        return False,[];

    s2 = rand.randint(1,numNodes)
    s2_out_edges=[d for o,d in g.edges(s2)]
    while_breaker=0
    while s2 == s1 or s2 == t1 or g.has_edge(s2,t1) or len(s2_out_edges) == 0 or (len(s2_out_edges) == 1 and g.has_edge(s2,s1)) and while_breaker < 4*numNodes:
        s2 = rand.randint(1,numNodes)
        s2_out_edges=[d for o,d in g.edges(s2)]
        while_breaker+=1

    if while_breaker == 4*numNodes:
        return False,[];

    while_breaker = 0;
    t2= s2_out_edges[rand.randint(0,len(s2_out_edges)-1)]
    while (t2 == s1 or g.has_edge(s1,t2)) and while_breaker < 2*len(s2_out_edges):
        t2= s2_out_edges[rand.randint(0,len(s2_out_edges)-1)]
        while_breaker+=1

    if while_breaker == 2*len(s2_out_edges):
        return False,[]

    nodes = [s1,t1,s2,t2]

    return True,nodes

S1 = 0
S2 = 2
T1 = 1
T2 = 3

def randomize_graph_deg_seq(g, number_of_switches):
    k=0
    new_g = g.copy()
    while k<number_of_switches:
        found,nodes = find_4(new_g)
        if found:
            new_g.remove_edge(nodes[S1],nodes[T1])
            new_g.remove_edge(nodes[S2],nodes[T2])
            new_g.add_edge(nodes[S1],nodes[T2])
            new_g.add_edge(nodes[S2],nodes[T1])
            k+=1
    return new_g

for n in nnodes:
    print n
    for j,d in enumerate(densities):
        print d
        for i in range(10):
            print i
            g = nx.read_edgelist("../dd_ispo/ddispo_{}_{}_{}.edges".format(n,d,i),data=False,nodetype=int)
            number_of_switches = 10 * g.number_of_edges()
            nn = randomize_graph_deg_seq(g,number_of_switches)
            g = nx.convert_node_labels_to_integers(nn,first_label=1)
            ofile = "config_{}_{}_{}.edges".format(n,d,i)
            nx.write_edgelist(g,ofile,data=False)
