from osmread import parse_file, Way, Relation, Node
import json
from pprint import pprint



with open('../data/buildings.json') as f:
    data = json.load(f)

#datum of format {u'latitude': u'37.8723', u'name': u'Bancroft Library/University Archives', u'longitude': u'-122.2587'}
for datum in data:
    print(datum['latitude'], datum['longitude'])



build_count = 0
node_count = 0
for entity in parse_file('../data/berkeley_map.osm'):
    if 'building' in entity.tags.keys(): #if a building
        build_count += 1
        #print(entity.tags)
        if isinstance(entity, Node):
            node_count += 1



#print("%d buildings found, %d nodes found" % (build_count, node_count))