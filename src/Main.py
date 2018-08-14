"""
A main class to create a graph from OSM data, discretize building locations, and calculate A* distances
using networkx.astar_path()

Calculates walking distances between all pairs of buildings and compares to optimal
straight-line path and horribly unoptimal manhattan distance

Sam Shen
"""

import json, util
from osmread import Node

graph, nodes = util.init_graph(util.getData('../data/berkeley_map.osm'))
buildings = json.load(open("../data/buildings.json"))
discretized_coords = []     #discretized coordinates of buildings to the closest node

for building in buildings:
    #add the lat/lon with the preceding "u'" removed
    true_coord = (float(str(building['latitude']).replace('u\'', '')), float(str(building['longitude']).replace('u\'', '')))
    discretized_coords.append(util.closest_element(true_coord, nodes.values()).pos())

print(discretized_coords)
