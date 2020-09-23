import CubeTutor
import EDHRec
import DiskWrite

driver = EDHRec.createDriver()

count = {}
percents = {}
synergies = {}

commanders = CubeTutor.readTxt("commanders.txt")
for commander in commanders:
    cards = EDHRec.getCommander(driver, commander, 10)
    for card in cards:
        count[card.name] = count.get(card.name, 0) + 1
        percents[card.name] = percents.get(card.name, 0) + int(card.percent)
        synergies[card.name] = synergies.get(card.name, 0) + int(card.synergy)

edhrecCards = set(count.keys())
cubeCards = set(CubeTutor.readCsv("commander_cube.csv"))
missingCards = edhrecCards - cubeCards

potentialCuts = sorted(cubeCards, key=lambda card: percents.get(card, 0))
DiskWrite.writeToFile("potentialcuts.txt", potentialCuts, count, percents)

potentialAdds = sorted(missingCards, key=lambda card: percents.get(card, 0), reverse=True)
DiskWrite.writeToFile("potentialadds.txt", potentialAdds, count, percents)

driver.quit()