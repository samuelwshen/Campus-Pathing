"""
A main class to create a graph from OSM data, discretize building locations, and calculate A* distances
using networkx.astar_path()

Calculates walking distances between all pairs of buildings and compares to optimal
straight-line path and horribly unoptimal manhattan distance

Sam Shen
"""

import json, util, sys
import networkx as nx
from decimal import *
from osmread import Node

FIRST_RUN = False
SAMPLE_REPEAT_SIZE = 3 #the number of times to sample
SAMPLE_SIZE_SQRT = 8   #the squareroot of the sample size

graph, nodes = util.init_graph(util.getData('../data/berkeley_map.osm'))
print("Initialized graph...")
buildings = json.load(open("../data/buildings.json"))

#only have to run this part once
if FIRST_RUN:
    util.batch_discretize(nodes, buildings, '../data/discrete_locs.txt')


str_coords = []         #list of string coordinate pairs
dec_coords = set()      #set of decimal coordinate pairs
discrete_nodes = []     #the nodes that represent discrete buildings
try:
    file = open("../data/discrete_locs.txt")
except:
    print("Did you download discrete_locs.txt OR run batch discretizing by setting FIRST_RUN to true?")
    sys.exit()
str_coords = file.readlines()                       #read by line
str_coords = [line.strip() for line in str_coords]  #remove /n ending

for str in str_coords:
    dec_coords.add(util.stringToDecimal(str))

for node in nodes.values():
    if node.pos() in dec_coords:
        discrete_nodes.append(node)     #getting the node objs by comparing their coordinates to the discrete building coordinates

assert(len(discrete_nodes) == len(dec_coords)), "Not all calculated discrete nodes were found in the graph"

dists = {} #dict from (start, end) building tuples to (straight line path length, optimal path length) tuple
count = 0
avg = Decimal()
avgs = []
for i in range(SAMPLE_REPEAT_SIZE):
    l1 = util.pick(SAMPLE_SIZE_SQRT, discrete_nodes, [])      #pick any SAMPLE_SIZE_SQRT unique nodes
    l2 = util.pick(SAMPLE_SIZE_SQRT, discrete_nodes, l1)      #pick SAMPLE_SIZE_SQRT excluding those in l1
    for b1 in l1:
        for b2 in l2:
            if b1 is not b2:
                heur = lambda o1, o2 : util.distance(o1.pos(), o2.pos())
                true_dist = heur(b1, b2)
                try:
                    dist = nx.algorithms.shortest_paths.astar_path_length(graph, b1, b2, heur)  #optimal path length
                    percent_of_true_dist = dist / true_dist * 100
                    avg += percent_of_true_dist
                    count += 1
                    print("%f%% of straight line distance" %percent_of_true_dist)
                except nx.exception.NetworkXNoPath as e:
                    print("Warning: two nodes have no path", b1.pos(), b2.pos())
                except nx.exception.NodeNotFound as e:  #when a node isn't part of a Way
                    print("Either b1 or b2 not in graph")
    avg = avg / count
    avgs.append(avg)
print("Average percent of straight line distance: %f" %(sum(avgs)/len(avgs)))

