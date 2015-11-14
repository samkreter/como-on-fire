from xml.etree import ElementTree
from neo4j import GraphDatabase, Node, Relationship, Path, CypherError
import urllib2
from bs4 import BeautifulSoup


session = GraphDatabase.driver("bolt://localhost").session()

resultEMS = urllib2.urlopen('https://www.gocolumbiamo.com/PSJC/Services/911/911dispatch/fire_georss.php').read()
treeEMS = ElementTree.fromstring(resultEMS)

resultPolice = urllib2.urlopen('https://www.gocolumbiamo.com/PSJC/Services/911/911dispatch/police_georss.php').read()
treePolice = BeautifulSoup(resultPolice)


def getEmergencyType(truck):
    if truck[0] == "M":
      return "Medical"
    else:
      return "Fire"

def getTruckType(truck):
    if truck[:2] == "SN":
      return "Snozzle"
    elif truck[0] == "S":
      return "Squad"
    elif truck[0] == "Q":
      return "Quint"
    elif truck[0] == "E":
      return "Engine"
    elif truck[0] == "L":
      return "Ladder"
    elif truck[0] == "M":
      return "Medic"

def getStationNum(truck):
    if truck == "" or truck is None:
	return ""
    digit = ""
    for s in truck:
        if s.isdigit():
            digit += s
    return int(digit) if digit != "" else -1


for node in treeEMS.iter('item'):
    emergencyMarker = "EMS"
    pubDate = node[0].text
    title = node[1].text
    desc = node[2].text
    geolat = float(node[3].text)
    geolong = float(node[4].text)
    callDateTime = node[5].text
    address = node[6].text
    displayName = node[7].text
    in_id = node[8].text
    timestamp = int(node[9].text)
    callDatalat = float(node[10].text)
    callDatalong = float(node[11].text)
    agency = node[12].text
    FDids = node[13].text
    trucks = node[14].text.split(" - ") if node[14].text is not None else " "
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
                 a.emergencyType={emergencyType},
                 a.FDids={FDids}
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
                   'emergencyType':emergencyMarker
                   'FDids':FDids})
    for truck in trucks:
        truckType = getTruckType(truck)
        truckStatNum = getStationNum(truck)
        emergencyType = getEmergencyType(truck)
        session.run("""MATCH(item:Item {id: {in_id}})
                     MERGE (truck:Truck {id: {truck}})
                     set truck.type={truckType}
                         truck.emergencyType={emergencyType}
                     MERGE (truck)-[:Dispatch]->(item)
                     """,{'truck':truck,'in_id':in_id,'emergencyType':emergencyType})

for node in treePolice.find_all('item'):
    emergencyType = "Police"
    pubDate = node.find('pubDate').text
    title = node.find('title').text
    desc = node.find('description').text
    geolat = float(node.find('geo:lat').text)
    geolong = float(node.find('geo:long').text)
    callDateTime = node.find('calldata:CallDateTime').text
    address = node.find('calldata:Address').text
    aptLot = node.find('calldata:AptLot').text
    displayName = node.find('calldata:ExtNatureDisplayName').text
    in_id = node.find('calldata:InNum').text
    timestamp = int(node.find('calldata:Timestamp').text)
    callDatalat = float(node.find('calldata:Latitude').text)
    callDatalong = float(node.find('calldata:Longitude').text)
    gridLoc = node.find('calldata:GridLoc').text
    disp = node.find('calldata:Disp').text
    session.run("""MERGE (a:Item {id: {in_id}})
             set a.pubDate={pubDate},
                 a.emergencyType={emergencyType},
                 a.title={title},
                 a.desc={desc},
                 a.geolat={geolat},
                 a.geolong={geolong},
                 a.callDateTime={callDateTime},
                 a.address={address},
                 a.aptLot={aptLot},
                 a.displayName={displayName},
                 a.timestamp={timestamp},
                 a.callDatalat={callDatalat},
                 a.callDatalong={callDatalong},
                 a.gridLoc={gridLoc},
                 a.disp={disp}
                 """, {'in_id':in_id,
                   'pubDate':pubDate,
                   'title':title,
                   'desc':desc,
                   'geolat':geolat,
                   'geolong':geolong,
                   'callDateTime':callDateTime,
                   'address':address,
                   'aptLot':aptLot,
                   'displayName':displayName,
                   'timestamp':timestamp,
                   'callDatalat':callDatalat,
                   'callDatalong':callDatalong,
                   'gridLoc':gridLoc,
                   'emergencyType':emergencyType,
                   'disp':disp})


#for name, in session.run("MATCH (a:Person) RETURN a.name AS name"):
#    print(name)
#session.close()
#
