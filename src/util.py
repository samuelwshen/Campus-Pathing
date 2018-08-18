import math
import networkx as nx
import json
from decimal import *
from osmread import parse_file, Way, Relation, Node

"""
Utility functions


Sam Shen
"""

#find closest element of type <myNode> in OSM data, taking in point as a Decimal
def closest_element(point, data):
    closest_dist = 10000000
    closest_elem = None
    for elem in data:
        if not isinstance(elem, Way) and isinstance(elem, myNode):
            #try:
            if distance(point, elem.pos()) < closest_dist:
                closest_dist = distance(point, elem.pos())
                closest_elem = elem
            #except:
            #    print("Excepting on", elem)
    return closest_elem

#discreetize a whole bunch of elems in discreetables based on the nodes parameter
#write to a write_loc as a bunch of coordinate paairs
def batch_discretize(nodes, discreetables, write_loc):
    file = open(write_loc, "w")
    for building in discreetables:
        print("Discretizing: ", building)
        # add the lat/lon as a decimal tuple with the preceding "u'" removed
        true_coord = (Decimal(str(building['latitude']).replace('u\'', '')), Decimal(str(building['longitude']).replace('u\'', '')))
        closest_node = closest_element(true_coord, nodes.values())
        file.write(str(closest_node.pos()) + "\n")
    file.close()

#find distance between two lon/lat tuples of Decimals
def distance(p1, p2):
    dx = abs(Decimal(p1[0] - p2[0]))
    dy = abs(Decimal(p1[1] - p2[1]))
    return Decimal(dx * dx + dy * dy).sqrt()

#initialize our networkx graph object
def init_graph(data):
    nodes = {}   #dictionary, node ID -> myNode obj
    ways = []       #list of ways, ways are tuples of node IDs that we know are connected
    graph = nx.Graph()

    for datum in data:
        if isinstance(datum, Node):
            nodes[datum.id] = myNode(datum)
        elif isinstance(datum, Way):
            ways.append(datum.nodes)

    for way in ways:
        if len(way) == 1:
            print("Welp")
        elif len(way) == 2:
            prev = nodes[way[0]]
            curr = nodes[way[1]]
            graph.add_edge(prev, curr, weight=distance(prev.pos(), curr.pos()))
        else:
            #hardcode get the first two, then increment for the rest
            prev = nodes[way[0]]
            curr = nodes[way[1]]
            for i in range(2, len(way)):
                graph.add_edge(prev, curr, weight=distance(prev.pos(), curr.pos()))
                prev = curr
                curr = nodes[way[i]]
            graph.add_edge(prev, curr, weight=distance(prev.pos(), curr.pos())) #add the last one
    return (graph, nodes)

#wrapper class for node to allow for proper hashing by node ID
class myNode:
    def __init__(self, node):
        assert isinstance(node, Node)   #make sure we have an osmread.Node obj
        self.node = node

    #return id
    def id(self):
        try:
            return self.node.id
        except:
            return None

    #return (lon, lat) tuple
    def pos(self):
        try:
            return (Decimal(self.node.lon), Decimal(self.node.lat))
        except:
            return (None, None)

    def __hash__(self):
        return self.id().__hash__()   #hash of the ID which is just the Long but in int form

def getData(location):
    return parse_file(location)

"""TESTING ZONE"""
count = 0
data = parse_file('../data/berkeley_map.osm')
graph = nx.Graph()      #so we can get pretty autocomplete when we test :)
graph = init_graph(data)[0]
print(graph.number_of_nodes())
print(graph.number_of_edges())
