def standardizeCardName(cardName):
    if (cardName == "Lim-Dûl's Vault"):
        return "Lim-Dul's Vault"
    # cubetutor doesn't include split names, so we're normalizing all names
    cardNames = cardName.split(" // ")
    return cardNames[0]