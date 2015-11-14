from xml.etree import ElementTree
from neo4j import GraphDatabase, Node, Relationship, Path, CypherError
import urllib2


result = urllib2.urlopen('https://www.gocolumbiamo.com/PSJC/Services/911/911dispatch/fire_georss.php').read()
tree = ElementTree.fromstring(result)
	

for node in tree.iter('item'):
	print node[2].text  
#url = node.attrib.get('xmlUrl')


#session = GraphDatabase.driver("bolt://localhost").session()

#driver = neo4j.driver("bolt://localhost")
#session = driver.session()
#session.run("CREATE (a:Person {name:'Bob'})")
#for name, in session.run("MATCH (a:Person) RETURN a.name AS name"):
#    print(name)
#session.close()
#
