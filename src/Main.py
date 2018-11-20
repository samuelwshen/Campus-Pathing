"""
A main class to create a graph from OSM data, discretize building locations, and calculate A* distances
using networkx.astar_path()

Calculates walking distances between a random sampling of buildings and compares to optimal
straight-line path

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

assert(len(discrete_nodes) == len(dec_coords)), "Not all calculated discrete nodes were found in the graph %d vs %d" %(len(discrete_nodes), len(dec_coords))

util.find_distances_naive(graph, discrete_nodes, SAMPLE_REPEAT_SIZE, SAMPLE_SIZE_SQRT)
#util.find_distances_floyd_warshall(graph, discrete_nodes)


