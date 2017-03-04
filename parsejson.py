from os import walk
import json
import operator

directory="jsondata"
cards = []
editions = []
editionUniqId = 1

def getOrElse(mapVal, key, elseVal):
	if key in mapVal:
		return mapVal[key]
	return elseVal


def openFile(fileName):
	global directory, cards, editions, editionUniqId
	with open(directory + "/" + fileName) as json_data:
		cardsData = json.load(json_data)
		i = 0
		while i<len(cardsData):
			#print json.dumps(cardsData[i], sort_keys=True, indent=2, separators=(',', ': '))
			newCard = {}
			newCard["id"] = cardsData[i]["id"]
			newCard["name"] = cardsData[i]["name"]
			newCard["power"] = getOrElse(cardsData[i],"power",-1)
			newCard["toughness"] = getOrElse(cardsData[i],"toughness",-1)
			newCard["types"] = ",".join(cardsData[i]["types"])
			newCard["subtypes"] = ",".join(getOrElse(cardsData[i],"subtypes",""))
			newCard["text"] = cardsData[i]["text"]
			newCard["store_url"] = cardsData[i]["store_url"]
			newCard["colors"] = ",".join(getOrElse(cardsData[i],"colors",""))
			newCard["cost"] = cardsData[i]["cost"]
			newCard["cmc"] = cardsData[i]["cmc"]
			newCard["editions"] = []

			for editionRaw in cardsData[i]["editions"]:
				#print json.dumps(editionRaw, sort_keys=True, indent=2, separators=(',', ': '))
				edition = {}
				edition["id"] = editionUniqId
				edition["set"] = editionRaw["set"]
				edition["set_id"] = editionRaw["set_id"]
				edition["artist"] = editionRaw["artist"]
				edition["image_url"] = editionRaw["image_url"]
				edition["rarity"] = editionRaw["rarity"]

				#store in editions
				editions.append(edition)

				#link to our card
				newCard["editions"].append(editionUniqId)
				editionUniqId += 1

			#store in cards
			cards.append(newCard)
			i+=1

# list all files in dir
files = []
for (dirpath, dirnames, filenames) in walk(directory):
	files = filenames
	break

for file in files:
	print "Processing "+file
	openFile(file)
	break

sqlOut = ""
sqlOut += "CREATE TABLE `cards` (\n"
sqlOut += "id int,\n"
sqlOut += "name varchar(512),\n"
sqlOut += "power int,\n"
sqlOut += "toughness int,\n"
sqlOut += "types varchar(512),\n"
sqlOut += "subtypes varchar(512),\n"
sqlOut += "text varchar(512),\n"
sqlOut += "store_url varchar(512),\n"
sqlOut += "costs varchar(512),\n"
sqlOut += "cost varchar(512),\n"
sqlOut += "cmc varchar(512),\n"
sqlOut += "editions varchar(512)\n"
sqlOut += ")\n\n"


for card in cards:
	sqlLine = "INSERT INTO `cards` ("
	sortedCard = sorted(card.items(), key=operator.itemgetter(0))
	fields = []
	for field in sortedCard:
		fields.append(field[0])
	sqlLine += ",".join(fields)+") VALUES ("
	data = []
	for field in sortedCard:
		if type(field[1]) is unicode or type(field[1]) is str:
			data.append("\""+(field[1]).encode('utf-8').strip().replace("\"", "\\\"")+"\"")
		elif type(field[1]) is int:
			data.append(""+str(field[1])+"")
		elif type(field[1]) is list:
			data.append("\""+(",".join(map(str,field[1])))+"\"")
		else:
			print "Unknown field"+str(type(field[1]))
			os.exit(1)
	sqlLine += ",".join(data)+");\n"
	sqlOut += sqlLine

print sqlOut