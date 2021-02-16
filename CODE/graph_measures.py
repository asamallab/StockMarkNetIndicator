# Python script for computing simple graph measures
# Input 1: Measure (EdgeCount, AverageDegree, AverageWeightedDegree, EdgeDensity, Diameter, AverageClustering)
# Input 2: Edge_file
"""
=================================================================================================
If you are using this code, kindly cite the following articles:
(1) A. Samal, H.K. Pharasi, S. J. Ramaia, H. Kannan, E. Saucan, J. Jost & A. Chakraborti, Network geometry and market instability, R. Soc. Open Sci. 8: 201734 (2021).
=================================================================================================
"""

import networkx as nx
import itertools
import sys

measure = sys.argv[1]
in_file = sys.argv[2]

G = nx.read_edgelist(in_file, comments='#',data=(('metric',float),))
G.remove_edges_from(nx.selfloop_edges(G))

if measure == "EdgeCount":
  	print( str(G.number_of_edges()) )
  
elif measure == "AverageDegree":
  	dsum = 0
  	tot = 0
  	for item in list(G.degree()):
    		dsum = dsum + item[1]
    		tot = tot + 1
 	
	avg = float(dsum) / float(tot)
	print(str(avg))   

elif measure == "AverageWeightedDegree":
  	dsum = 0
  	tot = 0
  	for item in list(G.degree(weight='metric')):
    		dsum = dsum + item[1]
    		tot = tot + 1
 	
	avg = float(dsum) / float(tot)
	print(str(avg))     

elif measure == "EdgeDensity":
  	tot = 0.5*( G.number_of_nodes()*(G.number_of_nodes()-1) )
  	print( str( float(G.number_of_edges()) / tot ) )

elif measure == "Diameter":
 	print(str(float(nx.diameter(G))))

elif measure == "AverageClustering":
 	print(str(float(nx.average_clustering(G))))

elif measure == "AverageShortestPathLength":
 	print(str(float(nx.average_shortest_path_length(G,weight='metric'))))
