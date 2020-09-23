from pathlib import Path

outputDir = Path("output")

def writeToFile(fileName, cardList, count, percents):
    outputDir.mkdir(exist_ok=True)
    outputPath = outputDir.joinpath(fileName)
    output = open(outputPath, "w")
    for card in cardList:
        commanderCount = count.get(card, 0)
        totalPercent = percents.get(card, 0)

        output.write(card)
        output.write("\t")
        output.write(str(commanderCount))
        output.write("\t")
        output.write(str(totalPercent))
        output.write("\n")
    output.close()