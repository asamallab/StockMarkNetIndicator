"""
==================================
Program to compute Menger and Haantjes curvature for edges in unweighted and 
undirected network.
Written by: Areejit Samal
Reference:
(1) A. Samal, H.K. Pharasi, S. J. Ramaia, H. Kannan, E. Saucan, J. Jost & A. Chakraborti, Network geometry and market instability, R. Soc. Open Sci. 8: 201734 (2021).
(2) E. Saucan, A. Samal & J. Jost. A simple differential geometry for complex networks. Network Science, 1-28 (2020). doi:10.1017/nws.2020.42.
(3) E. Saucan, A. Samal & J. Jost, A Simple Differential Geometry for Networks and Its Generalizations In: H. Cherifi, S. Gaito, J. Mendes, E. Moro, L. Rocha (Eds) Complex Networks and Their Applications VIII. COMPLEX NETWORKS 2019. Studies in Computational Intelligence, Vol. 881. Springer. 

Input 1: Edge_file 
Input 2: Out_file     
==================================
"""

import networkx as nx
import math
import sys

# Creating the undirected and unweighted graph from edge file
print ("-"*25)
G = nx.Graph()
count=0
for i in open(sys.argv[1], 'r'):
	e = i.strip().split('\t')
	if e[0]!=e[1]:
		G.add_edge(e[0], e[1], weight = 1)
	if e[0]==e[1]:
		count += 1 	

nnodes=G.number_of_nodes()
nedges=G.number_of_edges()
print ("Graph has \"%d\" nodes and \"%d\" edges"%(nnodes,nedges))
print ("Number of self edges is %d"%(count))
print ("-"*25)

# Compute Menger and Haantjes curvature of each edge
print("Started computing Menger and Haantjes curvature of each edge ...")

mt=(1.0/math.sqrt(3))

RE=open(sys.argv[2],'w')

for u,v in G.edges():
	mce=0
	hce=0
	nE=0
	for pl in range(1,4):
		paths=nx.all_simple_paths(G, source=u, target=v,cutoff=pl)
		nP = len(list(paths))		
		hce += (nP-nE)*math.sqrt(pl - 1)
		if pl == 2:
			mce += (nP-nE)*mt 
		nE = nP
			
	RE.write("%s\t%s\t%f\t%f\n"%(u,v,mce,hce))
	 
print ("-"*25)
