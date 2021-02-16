# Python code for calculating communication efficiency of a network.
# The reference articles for the computed measure:
# Latora, V., and Marchiori, M. (2001). Efficient behavior of small-world networks. Physical Review Letters 87.
# Latora, V., and Marchiori, M. (2003). Economic small-world behavior in weighted networks. Eur Phys J B 32, 249-263.
# Input 1: Node_file
# Input 2: Edge_file with weights
"""
=================================================================================================
If you are using this code, kindly cite the following articles:
(1) S. Venkatesan, R.P. Vivek-Ananth, R.P. Sreejith, P. Mangalapandi, A.A. Hassanali & A. Samal, Network approach towards understanding the crazing in glassy amorphous polymers, Journal of Statistical Mechanics: Theory and Experiment 043305 (2018).
(2) A. Samal, H.K. Pharasi, S. J. Ramaia, H. Kannan, E. Saucan, J. Jost & A. Chakraborti, Network geometry and market instability, R. Soc. Open Sci. 8: 201734 (2021).
=================================================================================================
"""

import igraph as ig
import sys

#edge files folder path
nodefile=sys.argv[1]
infile=sys.argv[2]

G=ig.Graph.Read_Ncol(infile,weights=True,directed=False,names=True)

N=G.vcount()
nodes=[i.strip().split()[0] for i in open(nodefile) if isinstance(int(i.strip().split()[0]),int)]
n_nodes=len(nodes)
n_isolated_nodes=n_nodes-N

if n_isolated_nodes != 0:
	G.add_vertices(n_isolated_nodes)
N=G.vcount()

length=G.shortest_paths_dijkstra(weights='weight')

temp=0
for i in length:
	temp+=sum([1.0/x for x in i if x!=0])
ce=float(temp)/float(N*(N-1))

print(ce)


