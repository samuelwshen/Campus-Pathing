import math
import networkx as nx
import json
from decimal import *
from osmread import parse_file, Way, Relation, Node

"""
Utility functions


Sam Shen
"""

#find closest element of type <myNode> in data, taking in point as a Decimal
def closest_element(point, data):
    return min(data, key=lambda a : distance(a.pos(), point))


#discreetize a whole bunch of elems in discreetables based on the nodes parameter
#write to a write_loc as a bunch of coordinate paairs
def batch_discretize(nodes, discreetables, write_loc):
    print("batch discretize", len(nodes))
    file = open(write_loc, "w")
    count = 1
    for building in discreetables:
        print("{} / {}".format(count, len(discreetables)))
        # add the lat/lon as a decimal tuple with the preceding "u'" removed
        true_coord = (Decimal(str(building['longitude']).replace('u\'', '')), Decimal(str(building['latitude']).replace('u\'', '')))
        closest_node_pos = closest_element(true_coord, nodes.values()).pos()
        to_write = closest_node_pos[0].to_eng_string() + ", " + closest_node_pos[1].to_eng_string()
        file.write(to_write + "\n")
        count += 1
    file.close()

#find distance between two lon/lat tuples of Decimals
def distance(p1, p2):
    dx = abs(Decimal(p1[0] - p2[0]))
    dy = abs(Decimal(p1[1] - p2[1]))
    return Decimal(dx * dx + dy * dy).sqrt()

#initialize our networkx graph object
def init_graph(data):
    nodes = {}   #dictionary, node ID -> myNode obj
    nodes_to_return = {} #dict, node ID -> myNode obj, filtered for nodes that are in a way
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
            nodes_to_return[way[0]] = prev
            nodes_to_return[way[1]] = curr
            graph.add_edge(prev, curr, weight=distance(prev.pos(), curr.pos()))
        else:
            #hardcode get the first two, then increment for the rest
            prev = nodes[way[0]]
            curr = nodes[way[1]]
            nodes_to_return[way[0]] = prev
            nodes_to_return[way[1]] = curr
            for i in range(2, len(way)):
                graph.add_edge(prev, curr, weight=distance(prev.pos(), curr.pos()))
                prev = curr
                curr = nodes[way[i]]
                nodes_to_return[way[i]] = curr
            graph.add_edge(prev, curr, weight=distance(prev.pos(), curr.pos())) #add the last one
    print("Init graph", len(nodes_to_return))
    return (graph, nodes_to_return)

"""
Takes a string of format 'Decimal, Decimal' and converts it into a tuple of decimals
"""
def stringToDecimal(str):
    split = str.split(", ")
    d1 = Decimal(split[0])
    d2 = Decimal(split[1])
    return (d1, d2)

#wrapper class for node to allow for proper hashing by node ID
class myNode:
    def __init__(self, node):
        assert isinstance(node, Node), "Cannot pass in a type %s" % type(node)   #make sure we have an osmread.Node obj
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

