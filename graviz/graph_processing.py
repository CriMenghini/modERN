#!/usr/bin/python3.5
# -*- coding: utf-8 -*-

import networkx as nx
import json
from networkx.readwrite import json_graph
from multiprocessing import Pool
import itertools

def save_graph(graph, filename, representation='edges'):
	"""
		Exports a `graph` into file `filename` using given `representation`.
		Representation types
			'edges': plain list of edges
			'JSON': graph stored in JSON format including attributes in nodes
	"""

	if representation == 'edges':
		nx.write_edgelist(graph, filename)
	elif representation == 'JSON':
		node_link = json_graph.node_link_data(graph)
		json.dump(node_link, open(filename, 'w'))
	else:
		raise Exception()

def load_graph(filename, representation='edges'):
	"""
		Imports a graph from file `filename` using given `representation`.
		Representation types
			'edges': plain list of edges
			'JSON': graph stored in JSON format including attributes in nodes

		Returns imported graph in Graph() NetworkX object (undirected graph).
	"""

	if representation == 'edges':
		return nx.read_edgelist(filename, create_using=nx.Graph())
	elif representation == 'JSON':
		with open(filename) as f:
			js_graph = json.load(f)
		return json_graph.node_link_graph(js_graph)
	else:
		raise Exception()

def add_degree_centrality(graph):
	"""
		Adds degree centrality measure to each node in the `graph`.

		Returns graph with degree centrality attribute added to the nodes
		and those nodes.
	"""

	nodes = nx.degree_centrality(graph)
	nx.set_node_attributes(graph, 'degree_centrality', nodes)

	return graph, nodes

def add_eigenvector_centrality(graph):
	"""
		Adds eigenvector centrality measure to each node in the `graph`.

		Returns graph with eigenvector centrality attribute added to the nodes
		and those nodes.
	"""

	nodes = nx.eigenvector_centrality(graph)
	nx.set_node_attributes(graph, 'eigenvector_centrality', nodes)

	return graph, nodes

# Code reference: https://networkx.github.io/documentation/development/examples/advanced/parallel_betweenness.html

def chunks(nodes, num_chunks):
	"""
		Divides a list of nodes `nodes` into `num_chunks` chunks

		Generator: yields consecutive elements of the list.
	"""

	nodes_iter = iter(nodes)
	while True:
		part = tuple(itertools.islice(nodes_iter, num_chunks))
		if not part:
			return
		yield part

def _betmap(graph_normalized_weight_sources_tuple):
	"""
		Pool for multiprocess only accepts functions with one argument. Uses
		a tuple as its only argument and then unpack it when it's send it to
		`betweenness_centrality_source`.

		Returns betweenness centrality measure for a subgraph.
	"""

	return nx.betweenness_centrality_source(*graph_normalized_weight_sources_tuple)

def parallel_betweenness_centrality(graph, processors):
	"""
		Computes betweenness centrality for `graph` using `processors`
		processors in parallel during computation.

		Returns nodes betweenness centrality measure.
	"""
	pool = Pool(processes=processors)
	num_chunks = int(graph.number_of_nodes()/processors)
	node_chunks = list(chunks(graph.nodes(), num_chunks))
	results = pool.map(_betmap, zip([graph]*num_chunks, [True]*num_chunks, [None]*num_chunks, node_chunks))

	# Reduce the partial solutions
	nodes = results[0]
	for result in results[1:]:
		for node in result:
			nodes[node] += result[node]

	return nodes

def add_betweenness_centrality(graph, processors):
	"""
		Adds betweenness centrality measure to each node in the `graph`.

		Returns graph with betweenness centrality attribute added to the nodes
		and those nodes.
	"""

	nodes = parallel_betweenness_centrality(graph, processors)
	nx.set_node_attributes(graph, 'betweenness_centrality', nodes)

	return graph, nodes

def add_centrality_stats(graph, processors=8):
	"""
		Adds degree, eigenvector and betweenness centrality measures to each
		node in the `graph` using using `processors` processors in parallel
		during computation.

		Returns graph with centrality measures attributes added to the nodes
		and nodes with different measures.
	"""

	graph, degree_nodes = add_degree_centrality(graph)
	graph, eigenvector_nodes = add_eigenvector_centrality(graph)
	graph, betweenness_nodes = add_betweenness_centrality(graph, processors)

	return graph, degree_nodes, eigenvector_nodes, betweenness_nodes

def reduce_graph_size(graph, eigenvector_nodes, percentage=0.01, threshold=100, method='threshold'):
	"""
		Leaves nodes that have eigenvalues they correspond to bigger or equal to
		eigenvalues in `percentage` of highest eigenvalues from `graph` or
		simply `threshold` highest depending on `method` used.

		Returns trimmed graph.
	"""

	x = sorted([(v, k) for (k,v) in eigenvector_nodes.items()], reverse=True)
	eigenvector_nodes = [p[1] for p in x]
	if method == 'percentage':
		right_bound = int(percentage*len(eigenvector_nodes))
	elif method == 'threshold':
		right_bound = threshold
	else:
		raise Exception()
	graph.remove_nodes_from(eigenvector_nodes[right_bound:])
	return graph
