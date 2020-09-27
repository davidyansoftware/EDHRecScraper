import json

import CardUtil

def getCardData(filePath):
    file = open(filePath, "r")
    cards = json.load(file)
    file.close()

    data = cards["data"]
    allCardNames = set(data.keys())
    for cardName in allCardNames:
        standardCardName = CardUtil.standardizeCardName(cardName)
        if (cardName != standardCardName):
            data[standardCardName] = data[cardName]
            del data[cardName]

    return data

def getColorIdentity(cardName):
    cardName = CardUtil.standardizeCardName(cardName)
    cards = cardData[cardName]
    atomicCard = cards[0]
    colorIdentity = atomicCard["colorIdentity"]
    types = atomicCard["types"]
    if "Land" in types:
        return "Land"
    elif (len(colorIdentity) == 0):
        return "Colorless"
    elif (len(colorIdentity) == 1):
        return colorIdentity[0]
    else:
        return "Multi"

#TODO fetch and cache this file
cardData = getCardData("AtomicCards.json")