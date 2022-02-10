import sys
import random as ran
import networkx as nx

g = nx.read_edgelist(sys.argv[1],data=False,nodetype=int)
l = [ed for ed in g.edges()]
g = g.to_directed()

recips = [1.,0.75,0.5,0.25,0.]
target_edges = [round(len(l)/(1-(float(r)/2))) for r in recips]
edges_to_rm = [int(round((1-r) * target_edges[i])) for i,r in enumerate(recips)]

for i in range(1,len(edges_to_rm)):
    edges_to_rm[i] -= sum(edges_to_rm[:i])

for i in range(len(recips)):
    dir = "new_nets_recip{}".format(int(100*recips[i]))
    list_removing = []
    #target_edges = round(len(l)/(1-(float(r)/2)))
    #edges_to_rm = int(round((1-r) * target_edges))
    for j in range(edges_to_rm[i]):
        to_remove = ran.randint(0,len(l)-1)
        ed = l[to_remove]
        l.pop(to_remove)
        if ran.random() > 0.5:
            list_removing.append(ed)
        else:
            list_removing.append((ed[1],ed[0]))
    g.remove_edges_from(list_removing)
    print(recips[i],nx.reciprocity(g))
    nx.write_edgelist(g,"{}/{}".format(dir,sys.argv[1]),data=False)
