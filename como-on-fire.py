from xml.etree import ElementTree
from neo4j import GraphDatabase, Node, Relationship, Path, CypherError
import urllib2


session = GraphDatabase.driver("bolt://localhost").session()

result = urllib2.urlopen('https://www.gocolumbiamo.com/PSJC/Services/911/911dispatch/fire_georss.php').read()
tree = ElementTree.fromstring(result)
	

for node in tree.iter('item'):
    pubDate = node[0].text
    title = node[1].text
    desc = node[2].text
    geolat = node[3].text
    geolong = node[4].text
    callDateTime = node[5].text
    address = node[6].text
    displayName = node[7].text  
    in_id = node[8].text
    timestamp = node[9].text
    callDatalat = node[10].text
    callDatalong = node[11].text
    agency = node[12].text
    FDids = node[13].text
    trucks = node[14].text
    


session.run("""MERGE (a:Item {id: {in_id}})
             set a.pubDate={pubDate}, 
                 a.title={title},
                 a.desc={desc},
                 a.geolat={geolat},
                 a.geolong={geolong},
                 a.callDateTime={callDateTime},
                 a.address={address},
                 a.displayName={displayName},
                 a.timestamp={timestamp},
                 a.callDatalat={callDatalat},
                 a.callDatalong={callDatalong},
                 a.agency={agency},
                 a.FDids={FDids},
                 a.trucks={trucks}
                 """, {'in_id':in_id,
                   'pubDate':pubDate,
                   'title':title,
                   'desc':desc,
                   'geolat':geolat,
                   'geolong':geolong,
                   'callDateTime':callDateTime,
                   'address':address,
                   'displayName':displayName,
                   'timestamp':timestamp,
                   'callDatalat':callDatalat,
                   'callDatalong':callDatalong,
                   'agency':agency,
                   'FDids':FDids,
                   'trucks':trucks}) 
#for name, in session.run("MATCH (a:Person) RETURN a.name AS name"):
#    print(name)
#session.close()
#
