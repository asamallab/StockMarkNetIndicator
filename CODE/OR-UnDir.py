"""
============================================================================================
A program to compute the Ollivier-Ricci curvature of a given undirected graph.
Reference:
(1) A. Samal, R.P. Sreejith, J. Gu, S. Liu, E. Saucan & J. Jost, Comparative analysis of two discretizations of Ricci curvature for complex networks, Scientific Reports 8: 8650 (2018).
(2) C.C. Ni, Y.Y. Lin, F. Luo & J. Gao. Community detection on networks with ricci flow. Scientific reports 9:9984 (2019).
The following is a modified version of the code that can be found in Chien-Chun Ni's github repository : https://github.com/saibalmars/GraphRicciCurvature.   
============================================================================================
"""

print ("-"*75)
import time, datetime
import cvxpy as cvx
import networkx as nx
import numpy as np
import sys

now = datetime.datetime.now()
start_time = time.time()
print ("Current date and time : ")
print (now.strftime("%Y-%m-%d %H:%M:%S"))
print ("="*25)


#If edge has Weight EW = 1 else EW = 0
EW=int(sys.argv[1])

EF=open(sys.argv[3], 'w')

#Creating the graph from the edge file
Graph=nx.Graph()
for i in open(sys.argv[2], 'r'):
	e = i.strip().split('\t')
	if EW == 0 and e[0]!=e[1]:
		Graph.add_edge(e[0], e[1], weight = 1)
	elif EW == 1 and e[0]!=e[1]:
		Graph.add_edge(e[0], e[1], weight = float(e[2]))

edgesize=Graph.number_of_edges()
nodesize=Graph.number_of_nodes()
print ("Graph has \"%d\" edges and \"%d\" nodes"%(edgesize, nodesize))

# Function for displaying the updates by a progress bar in console
#===============================================================================

def Progress(progress):
	
    barLength = 50
    status = ""
    if isinstance(progress, int):
        progress = float(progress)
    if not isinstance(progress, float):
        progress = 0
        status = "error: progress var must be float\r\n"
    if progress < 0:
        progress = 0
        status = "Halt...\r\n"
    if progress >= 1:
        progress = 1
        status = "Done...\r\n"
    block = int(round(barLength*progress))
    text = "\rPercent: [{0}] {1}% {2}".format( "="*block + " "*(barLength-block), round((progress*100),3), status)
    sys.stdout.write(text)
    sys.stdout.flush()


# Function to compute the Olliver ricci curvature for a given edge
#===============================================================================

def RicciCurvature_Edge(G, vertex_1, vertex_2, alpha, length):

	EPSILON = 1e-7	# to prevent division by zero

	assert vertex_1 != vertex_2, "Self loop is not allowed."	

	if length[vertex_1][vertex_2] < EPSILON:
		assert "ricciCurvature" in G[vertex_1][vertex_2], "Divided by Zero and no ricci curvature exist in Graph!"
		print("Zero Weight edge detected, return previous ricci Curvature instead.")
		return G[vertex_1][vertex_2]["ricciCurvature"]

	vertex_1_nbr = list(G.neighbors(vertex_1))
	vertex_2_nbr = list(G.neighbors(vertex_2))

	assert len(vertex_1_nbr) > 0, "vertex_1 Nbr=0?"
	assert len(vertex_2_nbr) > 0, "vertex_2 Nbr=0?" + str(vertex_1) + " " + str(vertex_2)
	x = [(1.0 - alpha) / len(vertex_1_nbr)] * len(vertex_1_nbr)
	y = [(1.0 - alpha) / len(vertex_2_nbr)] * len(vertex_2_nbr)

	vertex_1_nbr.append(vertex_1)
	vertex_2_nbr.append(vertex_2)
	x.append(alpha)
	y.append(alpha)

	# construct the cost dictionary from x to y
	d = np.zeros((len(x), len(y)))

	for i, s in enumerate(vertex_1_nbr):
		for j, t in enumerate(vertex_2_nbr):
			assert t in length[s], "vertex_2 node not in list, should not happened, pair (%d, %d)" % (s, t)
			d[i][j] = length[s][t]

	x = np.array([x]).T	# the mass that vertex_1 neighborhood initially owned
	y = np.array([y]).T	# the mass that vertex_2 neighborhood needs to received

	t0 = time.time()
	rho = cvx.Variable(shape=(len(vertex_2_nbr), len(vertex_1_nbr)))

	# objective function d(x,y) * rho * x, need to do element-wise multiply here
	obj = cvx.Minimize(cvx.sum(cvx.multiply(np.multiply(d.T, x.T), rho)))

	# \sigma_i rho_{ij}=[1,1,...,1]
	vertex_1_sum = cvx.sum(rho, axis=0)
	constrains = [rho * x == y, vertex_1_sum == np.ones(len(vertex_1_nbr)), 0 <= rho, rho <= 1]
	prob = cvx.Problem(obj, constrains)

	m = prob.solve(solver='ECOS')	
	#print(time.time() - t0, " secs for cvxpy.",)

	result = 1 - (m / length[vertex_1][vertex_2])	# divided by the length of d(i, j)
	#print("#vertex_1_nbr: %d, #vertex_2_nbr: %d, Ricci curvature = %f	"%(len(vertex_1_nbr), len(vertex_2_nbr), result))
	#print("%s\t%s\t%f"%(vertex_1, vertex_2, result))
	EF.write("%s\t%s\t%f\n"%(vertex_1, vertex_2, result*2))
	return result



# Function Compute ricci curvature for all nodes and all edges in G.
#================================================================================

def RicciCurvature(G, alpha=0.5, weight=None):
	# Construct the all pair shortest path lookup
	t0 = time.time()
	print ("> Calculate Dijkstra path length") 
	print ("Time :")
	now = datetime.datetime.now()
	print (now.strftime("%H:%M:%S"))
	length = dict(nx.all_pairs_dijkstra_path_length(G, weight=weight))
	print ("Finished :")
	now = datetime.datetime.now()
	print ("Time taken = ", round((time.time() - t0)/60.0), "min")
	# compute ricci curvature
	no=1.0
	print ("> Calculate Olliver-Ricci for each edge")
	for s, t in G.edges():
		G[s][t]['ricciCurvature'] = RicciCurvature_Edge(G, vertex_1=s, vertex_2=t, alpha=alpha, length=length)
		Progress(no/edgesize) # Progress bar on terminal
		no+=1
	# compute node ricci curvature to graph G
	print("> Node ricci curvature started")
	NF=open(sys.argv[4],'w')
	no=1.0
	for n in G.nodes():
		rcsum = 0	# sum of the neighbor Ricci curvature
		if G.degree(n) != 0:
			for nbr in G.neighbors(n):
				if 'ricciCurvature' in G[n][nbr]:
					rcsum += G[n][nbr]['ricciCurvature']
			# assign the node Ricci curvature to be the average of node's adjacency edges
			G.node[n]['ricciCurvature'] = rcsum / G.degree(n)
			NF.write("%s\t%f\t%f\n"%(n, G.node[n]['ricciCurvature'], rcsum))
		#else:
		 #       NF.write("%s\t%f\n"%(n, 3))

		Progress(no/nodesize)
		no+=1
	#print("> Node ricci curvature computation done.")'''
	return G

#================================================================================

# Calling the main function to compute Olliver-Ricci curvature of the graph
print ("Olliver-Ricci curvature for edge")
OlliverRicci=RicciCurvature(Graph, alpha=0.5, weight='weight')
print ("Current date and time : ")
now = datetime.datetime.now()
print (now.strftime("%Y-%m-%d %H:%M:%S"))
end_time = time.time()
sec=(-start_time+end_time)
print ("="*25)
print ("Time taken = %f min (%f sec)"%(sec/60, sec))
print ("-"*75)



