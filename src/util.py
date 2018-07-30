import math
from osmread import parse_file, Way, Relation, Node
"""
Utility functions


Sam Shen
"""

#find closest element of type <elem_type> in OSM data
def closest_element(point, elem_type, data):
    closest_dist = 10000000
    closest_elem = None
    for elem in data:
        if isinstance(elem, elem_type):
            try:
                temp_lonlat = (elem.lon, elem.lat)
                if distance(point, temp_lonlat) < closest_dist:
                    closest_dist = distance(point, temp_lonlat)
                    closest_elem = elem
            except:
                print("Attempting to access lat/lon of %s failed" % str(elem))
    return closest_elem

#find distance between two lon/lat tuples
def distance(p1, p2):
    dx = abs(p1[0] - p2[0])
    dy = abs(p1[1] - p2[1])
    return math.sqrt(dx**2 + dy**2)



"""TESTING ZONE"""
data = parse_file('../data/berkeley_map.osm')
datum = next(data)
test_tuple = (datum.lon + 0.000001, datum.lat + 0.000002)
print(closest_element(test_tuple, object, data))
print(test_tuple)