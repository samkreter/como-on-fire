from xml.etree import ElementTree
from neo4j import GraphDatabase, Node, Relationship, Path, CypherError
import urllib2


session = GraphDatabase.driver("bolt://localhost").session()

result = urllib2.urlopen('https://www.gocolumbiamo.com/PSJC/Services/911/911dispatch/fire_georss.php').read()
tree = ElementTree.fromstring(result)
	

for node in tree.iter('item'):
    title = node[1].text
    desc = node[2].text  
#url = node.attrib.get('xmlUrl')


session.run("""MERGE (a:Item {id: {in_id} })""", in_id=in_id) on 
#for name, in session.run("MATCH (a:Person) RETURN a.name AS name"):
#    print(name)
#session.close()
#
