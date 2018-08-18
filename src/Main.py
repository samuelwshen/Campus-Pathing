"""
A main class to create a graph from OSM data, discretize building locations, and calculate A* distances
using networkx.astar_path()

Calculates walking distances between all pairs of buildings and compares to optimal
straight-line path and horribly unoptimal manhattan distance

Sam Shen
"""

import json, util
import networkx as nx
from decimal import *
from osmread import Node


graph, nodes = util.init_graph(util.getData('../data/berkeley_map.osm'))
buildings = json.load(open("../data/buildings.json"))

util.batch_discretize(nodes, buildings, '../data/discrete_locs.txt')

"""
dists = {} #dict from (start, end) building tuples to (straight line path length, optimal path length) tuple
count = 0
avg = 1.0
for b1 in discrete_nodes:
    for b2 in discrete_nodes:
        if b1 is not b2:
            heur = lambda o1, o2 : util.distance(o1.pos(), o2.pos())
            true_dist = heur(b1, b2)
            dist = nx.algorithms.shortest_paths.astar_path_length(graph, b1, b2, heur)  #optimal path length
            percent_diff = (dist - true_dist) / true_dist
            print(percent_diff)
"""
