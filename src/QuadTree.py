import util, decimal
from osmread import Node
"""
A QuadTree consists of four sub QuadTreess, representing the four quadrants inside a QuadTree's domain
"""

class QuadTree:
    def __init__(self, ullon, ullat, lrlon, lrlat, nodes):
        if len(nodes) != 0:
            self.ullon = ullon
            self.ullat = ullat
            self.lrlon = lrlon
            self.lrlat = lrlat
            self.terminal = False
            self.terminal_node = None
            self.nodes = nodes
            if len(nodes) > 1:
                midlon = (ullon + lrlon) / 2.0
                midlat = (ullat + lrlat) / 2.0
                midtoplon = midlon
                midtoplat = ullat
                midbotlon = midlon
                midbotlat = lrlat
                midleftlon = ullon
                midleftlat = midlat
                midrightlon = lrlon
                midrightlat = midlat
                upperleft, upperright, lowerleft, lowerright = set(), set(), set(), set()
                for node in nodes:
                    if util.filterCoord(ullon, ullat, midlon, midlat, node.pos()):       #upper left quadrant
                        upperleft.add(node)
                    elif util.filterCoord(midtoplon, midtoplat, midrightlon, midrightlat, node.pos()):     #upper right quadrant
                        upperright.add(node)
                    elif util.filterCoord(midleftlon, midleftlat, midbotlon, midbotlat, node.pos()):        #lower left
                        lowerleft.add(node)
                    elif util.filterCoord(midlon, midlat, lrlon, lrlat, node.pos()):        #bottom right
                        lowerright.add(node)
                #the subtree list goes upperlift, upperright, lowerleft, lowerright
                self.subtrees = [QuadTree(ullon, ullat, midlon, midlat, upperleft),
                                 QuadTree(midtoplon, midtoplat, midrightlon, midrightlat, upperright),
                                 QuadTree(midleftlon, midleftlat, midbotlon, midbotlat, lowerleft),
                                 QuadTree(midlon, midlat, lrlon, lrlat, lowerright)]
                if len(upperleft) == 0:
                    self.subtrees[0] = None
                if len(upperright) == 0:
                    self.subtrees[1] = None
                if len(lowerleft) == 0:
                    self.subtrees[2] = None
                if len(lowerright) == 0:
                    self.subtrees[3] = None
            elif len(nodes) == 1:
                self.terminal = True
                self.subtrees = []
                try:
                    self.terminal_node = nodes[0]
                except:
                    self.terminal_node = None

    def isTerminal(self):
        return self.terminal

    def terminalNode(self):
        return self.terminal_node

    #tells you if this quadtree has a terminal node
    #may not have a terminal node for two reasons:
    #not a terminal QuadTree, or is a quadrant with no nodes
    def hasTerminalNode(self):
        return self.terminal_node != None

    #if the coord is in the domain of this QuadTree
    def inDomain(self, coord):
        return util.filterCoord(self.ullon, self.ullat, self.lrlon, self.lrlat, coord)

    def getNodeByCoord(self, coord):
        #as soon as we hit a level where we have a sub quadtree with no nodes, we search all surrounding
        #quadtrees to find the closest element

        if None in self.subtrees:
            calls = []
            for t in self.subtrees:
                if t is not None:
                    call = t.getNodeByCoord(coord)
                    if call is not None:
                        calls.append(call)
            if len(calls) == 0:
                return DummyClass()
            return min(calls, key=lambda x: util.distance(coord, x.pos()))
        if self.isTerminal() and self.hasTerminalNode():
            return self.terminalNode()
        elif self.isTerminal():
            return DummyClass()
        elif self.subtrees[0].inDomain(coord):
            return self.subtrees[0].getNodeByCoord(coord)
        elif self.subtrees[1].inDomain(coord):
            return self.subtrees[1].getNodeByCoord(coord)
        elif self.subtrees[2].inDomain(coord):
            return self.subtrees[2].getNodeByCoord(coord)
        elif self.subtrees[3].inDomain(coord):
            return self.subtrees[3].getNodeByCoord(coord)


class DummyClass:
    def __init__(self):
        self.nothing = None

    def pos(self):
        return (decimal.Decimal(1000000.0), decimal.Decimal(1000000.0))
