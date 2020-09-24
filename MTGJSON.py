import json

def getCardData(filePath):
    file = open(filePath, "r")
    cards = json.load(file)
    file.close()

    data = cards["data"]
    allCardNames = set(data.keys())
    for cardName in allCardNames:
        standardCardName = standardizeCardName(cardName)
        if (cardName != standardCardName):
            data[standardCardName] = data[cardName]
            del data[cardName]

    return data

def getColorIdentity(cardName):
    cardName = standardizeCardName(cardName)
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

def standardizeCardName(cardName):
    if (cardName == "Lim-Dûl's Vault"):
        return "Lim-Dul's Vault"
    # edhrec doesn't include split names, so we're normalizing all names
    cardNames = cardName.split(" // ")
    return cardNames[0]

#TODO fetch and cache this file
cardData = getCardData("AtomicCards.json")