import CubeTutor
import DiskWrite
import EDHRec
import MTGJSON

driver = EDHRec.createDriver()

count = {}
percents = {}
synergies = {}

totalPercent = 0
totalSynergy = 0

commanders = CubeTutor.readTxt("commanders.txt")
for commander in commanders:
    cards = EDHRec.getCommander(driver, commander, 10)
    for card in cards:
        color = MTGJSON.getColorIdentity(card.name)

        if (count.get(color) is None):
            count[color] = {}
        count[color][card.name] = count[color].get(card.name, 0) + 1

        percent = int(card.percent)
        if (percents.get(color) is None):
            percents[color] = {}
        percents[color][card.name] = percents[color].get(card.name, 0) + percent
        totalPercent += percent

        synergy = int(card.synergy)
        if (synergies.get(color) is None):
            synergies[color] = {}
        synergies[color][card.name] = synergies[color].get(card.name, 0) + synergy
        totalSynergy += synergy

driver.quit()

allCubeCards = set(CubeTutor.readCsv("commander_cube.csv"))
cubeCards = {}
for card in allCubeCards:
    color = MTGJSON.getColorIdentity(card)
    if(cubeCards.get(color) is None):
        cubeCards[color] = []
    cubeCards[color].append(card)

for color in count.keys():
    edhrecCards = set(count[color].keys())
    colorCards = set(cubeCards[color])
    missingCards = edhrecCards - colorCards

    potentialCuts = sorted(colorCards, key=lambda card: percents[color].get(card, 0))
    DiskWrite.writeToFile(color + "_cuts.txt", potentialCuts, count[color], percents[color])

    potentialAdds = sorted(missingCards, key=lambda card: percents[color].get(card, 0), reverse=True)
    DiskWrite.writeToFile(color + "_adds.txt", potentialAdds, count[color], percents[color])

print("Total Percent: " + str(totalPercent))
print("Total Synergy: " + str(totalSynergy))