import os
import re
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

import CardUtil
import EDHRecCache

#TODO lazy load this
def createDriver():
    options = Options()
    options.add_argument("start-maximized")
    options.add_argument("enable-automation")
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-browser-side-navigation")
    options.add_argument("--disable-gpu")

    driverPath = ChromeDriverManager().install()
    driver = webdriver.Chrome(executable_path=driverPath, options=options)

    return driver

class Card:
    def __init__(self, name, percent, synergy):
        self.name = name
        self.percent = percent
        self.synergy = synergy

def getCommander(driver, commander, threshold):
    print(commander)
    commanderHtml = getCommanderHtml(driver, commander)
    soup = BeautifulSoup(commanderHtml, 'html.parser')

    cardsDivs = soup.findAll("div", attrs={"class": "cardlist"})
    cardContainers = []
    for cardsDiv in cardsDivs:
        divs = cardsDiv.findAll("div", attrs={"class": "card__container"})
        for cardContainer in divs:
            cardContainers.append(cardContainer)

    cards = []
    for cardContainer in cardContainers:
        cardNameDiv = cardContainer.find("div", attrs={"class": "card__name"})
        cardName = cardNameDiv.text
        cardLabelDiv = cardContainer.find("div", attrs={"class": "card__label"})
        cardLabel = cardLabelDiv.text
        (percent, synergy) = re.findall(r"([-]?\d+)%", cardLabel)

        if (int(percent) > threshold):
            cardName = CardUtil.standardizeCardName(cardName)
            card = Card(cardName, int(percent), int(synergy))
            cards.append(card)

    return cards

def formatEdhrecUrl(card):
    card = card.replace(" ", "-")
    card = card.replace("'", "")
    card = card.replace(",", "")
    return card

def getCommanderHtml(driver, commander):
    commander = formatEdhrecUrl(commander)

    if (EDHRecCache.cachedCommanderExists(commander)):
        return EDHRecCache.getCachedCommanderHtml(commander)

    url = "https://edhrec.com/commanders/" + commander
    try:
        driver.get(url)
    except Exception:
        driver.quit()
        raise

    # sleep serves dual purpose of:
    # rate limiting
    # waiting for clientside rendering
    time.sleep(3)

    html = driver.page_source
    EDHRecCache.cacheCommanderHTML(commander, html)
    return html