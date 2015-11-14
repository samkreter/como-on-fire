from xml.etree import ElementTree
from neo4j import GraphDatabase, Node, Relationship, Path, CypherError

with open('podcasts.opml', 'rt') as f:
    tree = ElementTree.parse(f)

for node in tree.findall('.//outline'):
    url = node.attrib.get('xmlUrl')
    if url:
        print url

#session = GraphDatabase.driver("bolt://localhost").session()

#driver = neo4j.driver("bolt://localhost")
#session = driver.session()
#session.run("CREATE (a:Person {name:'Bob'})")
#for name, in session.run("MATCH (a:Person) RETURN a.name AS name"):
#    print(name)
#session.close()
#
