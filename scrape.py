import CubeTutor
import EDHRec
from pathlib import Path

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

cubeCards = {}
cubeCards = set(CubeTutor.readCsv("commander_cube.csv"))

outputdir = Path("output")
outputdir.mkdir(exist_ok=True)

potentialCuts = sorted(cubeCards, key=lambda card: percents.get(card, 0))
outputPath = outputdir.joinpath("potentialcuts.txt")
output = open(outputPath, "w")
for card in potentialCuts:
    commanderCount = count.get(card, 0)
    totalPercent = percents.get(card, 0)

    output.write(card)
    output.write("\t")
    output.write(str(commanderCount))
    output.write("\t")
    output.write(str(totalPercent))
    output.write("\n")
output.close()

allCards = set(count.keys())
missingCards = allCards - cubeCards
potentialAdds = sorted(missingCards, key=lambda card: percents.get(card, 0), reverse=True)
outputPath = outputdir.joinpath("potentialadds.txt")
output = open(outputPath, "w")
for card in potentialAdds:
    commanderCount = count.get(card, 0)
    totalPercent = percents.get(card, 0)

    output.write(card)
    output.write("\t")
    output.write(str(commanderCount))
    output.write("\t")
    output.write(str(totalPercent))
    output.write("\n")
output.close()

driver.quit()