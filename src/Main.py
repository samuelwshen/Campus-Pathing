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

firstRun = True

graph, nodes = util.init_graph(util.getData('../data/berkeley_map.osm'))
buildings = json.load(open("../data/buildings.json"))

#only have to run this part once
if firstRun:
    util.batch_discretize(nodes, buildings, '../data/discrete_locs.txt')


str_coords = []         #list of string coordinate pairs
dec_coords = set()      #set of decimal coordinate pairs
discrete_nodes = []
file = open("../data/discrete_locs.txt")
str_coords = file.readlines()                       #read by line
str_coords = [line.strip() for line in str_coords]  #remove /n ending

for str in str_coords:
    dec_coords.add(util.stringToDecimal(str))

for node in nodes.values():
    if node.pos() in dec_coords:
        discrete_nodes.append(node)     #getting the node objs by comparing their coordinates

assert(len(discrete_nodes) == len(dec_coords)), "Not all calculated discrete nodes were found in the graph"

dists = {} #dict from (start, end) building tuples to (straight line path length, optimal path length) tuple
count = 0
avg = 1.0
for b1 in discrete_nodes:
    for b2 in discrete_nodes:
        if b1 is not b2:
            heur = lambda o1, o2 : util.distance(o1.pos(), o2.pos())
            true_dist = heur(b1, b2)
            try:
                dist = nx.algorithms.shortest_paths.astar_path_length(graph, b1, b2, heur)  #optimal path length
                percent_diff = (dist - true_dist) / true_dist * 100
                print(percent_diff)
            except nx.exception.NetworkXNoPath as e:
                print("Warning: two nodes have no path", b1.pos(), b2.pos())
            except nx.exception.NodeNotFound as e:  #when a node isn't part of a Way
                print("Either b1 or b2 not in graph")

