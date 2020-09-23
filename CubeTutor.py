import csv

def readTxt(filePath):
    cards = []
    cardsFile = open(filePath, "r")
    for card in cardsFile:
        card = card.strip("\n")
        cards.append(card)
    return cards

def readCsv(filePath):
    cards = []
    cardsFile = open(filePath, "r")
    for line in csv.reader(cardsFile, quotechar="\"", delimiter=",", quoting=csv.QUOTE_ALL):
        card = line[0]
        card = card.strip("\"")
        cards.append(card)
    return cards