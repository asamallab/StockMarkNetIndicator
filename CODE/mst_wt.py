# Python script to compute the minimum spanning tree of a network and subsequent addition of edges based on threshold on correlation values.
# Input 1: Edge_file
# Input 2: Whether the network is weighted (1) or unweighted (0)
# Input 2: Out_file
# Input 3: Node_file
"""
=================================================================================================
If you are using this code, kindly cite the following articles:
1) A. Samal, H.K. Pharasi, S. J. Ramaia, H. Kannan, E. Saucan, J. Jost & A. Chakraborti, Network geometry and market instability, (Submitted).
=================================================================================================
"""

import networkx as nx
import itertools
import sys

in_file = sys.argv[1]
out_file = sys.argv[3]
node_file = sys.argv[4]

f = open(out_file, 'w')
g = open(node_file, 'w')

G = nx.read_edgelist(in_file, comments='#', data=(('corr',float),('metric',float)))
G.remove_edges_from(G.selfloop_edges())

nodes=[]
nodes = list(G.nodes)

mst = list(nx.algorithms.tree.mst.minimum_spanning_edges(G, algorithm='prim', weight='metric', data=True))

for x in mst:
	f.write(x[0] + '\t' + x[1] + '\t')
	for edge in G.edges(data=True):
		if x[0] == edge[0] and x[1]==edge[1]:
			wt = edge[2]['metric']
			f.write("%f\n" % (wt))
			break
		elif x[0] == edge[1] and x[1]==edge[0]:
			wt = edge[2]['metric']	
			f.write("%f\n" % (wt))
			break					

for edge in G.edges(data=True):
	flag = 0

 	for x in mst:
  		if x[0] == edge[0] and x[1]==edge[1]:
   			flag = 1
  		elif x[0] == edge[1] and x[1]==edge[0]:
   			flag = 1

 	if flag == 0 and edge[2]['corr'] >= float(sys.argv[2]):
  		f.write(edge[0] + '\t' + edge[1] + '\t')
		wt = edge[2]['metric']	
		f.write("%f\n" % (wt))
  
for node in nodes:
 	g.write(node + '\n')
