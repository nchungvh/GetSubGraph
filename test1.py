import networkx as nx
import numpy as np 
import pdb
import argparse

def parse_args():
	parser = argparse.ArgumentParser(description = "get subgraph")
	parser.add_argument( '--graph1', default = "flickr", help = "path for input")
	parser.add_argument( '--graph2', default = "lastfm", help = "path for input")

	return parser.parse_args()

def read_file(graph):
	filenodes = open('{}.nodes'.format(graph)).readlines()
	for i in range(len(filenodes)):
		filenodes[i] = filenodes[i].split()
	filenodes = np.asarray(filenodes)
	#pdb.set_trace()(253245,2)

	fileedges = open('{}.edges'.format(graph)).readlines()
	for i in range(len(fileedges)):
		fileedges[i] = fileedges[i].split()
	fileedges = np.asarray(fileedges)

	my_graph = nx.Graph()
	edges = nx.read_edgelist('{}.edges'.format(graph))
	my_graph.add_edges_from(edges.edges())
	my_graph.add_nodes_from([(int(node), {'username': attr}) for (node, attr) in filenodes])

	return filenodes,fileedges, my_graph

# my_graph = nx.Graph()
# edges = nx.read_edgelist('flickr/flickr.edges')
# nodes = nx.read_adjlist('flickr/flickr.nodes')
# print(nodes.nodes(data = True))
# my_graph.add_edges_from(edges.edges())
# my_graph.add_nodes_from(nodes)

def get_subgraph(graph1,graph2):
	#### read nodes

########################################## get sub_graph1 ################################################

	nodeGraph,edgesGraph , my_graph = read_file(graph1)
	#### read file groundtruth
	file = open('{}-{}.map.raw'.format(graph,graph2)).readlines()
	for i in range(len(file)):
		file[i] = file[i].split()
	file = np.asarray(file)
	a_list = np.asarray(file[:,0])
	b_list = np.asarray(file[:,1])
	#pdb.set_trace()
	sub_nodes =[]
	for i in range(len(a_list)):
		for j in range(len(nodeGraph)):
			if(str(nodeGraph[j][1])==a_list[i]):
				sub_nodes.append(int(nodeGraph[j][0]))
				break

	sub_nodes = np.sort(sub_nodes)
	print(sub_nodes)
	sub_nodes_1hop = list(sub_nodes)
	for i in range(len(sub_nodes)):
		for j in range(len(edgesGraph)):
			if(int(edgesGraph[j][0])==sub_nodes[i]):
				sub_nodes_1hop.append(int(edgesGraph[j][1]))
			elif(int(edgesGraph[j][1])==sub_nodes[i]):
				sub_nodes_1hop.append(int(edgesGraph[j][0]))
			else:
				continue
	kn = np.asarray(set(np.sort(sub_nodes_1hop)))
	j = 0
	pdb.set_trace()
	for i in range(len(nodeGraph)):
		if(int(nodeGraph[i][0])<kn[j]):
			my_graph.remove_node(nodeGraph[i][0])
		else:
			j+=1
			if(j>len(kn)):
				break
	nx.write_gpickle(my_graph, "{}_subgraph_{}-{}.gpickle".format(graph1,graph1,graph2))

######################################## get sub_graph2 #########################################################
	
	nodeGraph,edgesGraph , my_graph = read_file(graph2)
	#### read file groundtruth
	file = open('{}-{}.map.raw'.format(graph,graph2)).readlines()
	for i in range(len(file)):
		file[i] = file[i].split()
	file = np.asarray(file)
	a_list = np.asarray(file[:,0])
	b_list = np.asarray(file[:,1])
	#pdb.set_trace()
	sub_nodes =[]
	for i in range(len(a_list)):
		for j in range(len(nodeGraph)):
			if(str(nodeGraph[j][1])==a_list[i]):
				sub_nodes.append(int(nodeGraph[j][0]))
				break

	sub_nodes = np.sort(sub_nodes)
	print(sub_nodes)
	sub_nodes_1hop = list(sub_nodes)
	for i in range(len(sub_nodes)):
		for j in range(len(edgesGraph)):
			if(int(edgesGraph[j][0])==sub_nodes[i]):
				sub_nodes_1hop.append(int(edgesGraph[j][1]))
			elif(int(edgesGraph[j][1])==sub_nodes[i]):
				sub_nodes_1hop.append(int(edgesGraph[j][0]))
			else:
				continue
	kn = np.asarray(set(np.sort(sub_nodes_1hop)))
	j = 0
	pdb.set_trace()
	for i in range(len(nodeGraph)):
		if(int(nodeGraph[i][0])<kn[j]):
			my_graph.remove_node(nodeGraph[i][0])
		else:
			j+=1
			if(j>len(kn)):
				break
	nx.write_gpickle(my_graph, "{}_subgraph_{}-{}.gpickle".format(graph2,graph1,graph2))

if __name__ == "__main__":
    args = parse_args()
    print(args)
    get_subgraph(args[0],args[1])


#### extract nodes from groundtruth