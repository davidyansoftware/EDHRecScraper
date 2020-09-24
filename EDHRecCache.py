import time
from pathlib import Path

cacheDir = Path("__edhreccache__")
commanderCacheDir = cacheDir.joinpath("commander")

def cachedCommanderExists(commander):
    cachePath = commanderCacheDir.joinpath(commander)
    return cachePath.exists() and cachePath.is_file() and isFresh(cachePath)

def getCachedCommanderHtml(commander):
    cachePath = commanderCacheDir.joinpath(commander)
    cacheFile = open(cachePath, "r")
    return cacheFile.read()

def cacheCommanderHTML(commander, html):
    cacheDir.mkdir(exist_ok=True)
    commanderCacheDir.mkdir(exist_ok=True)
    cachePath = commanderCacheDir.joinpath(commander)
    cache = open(cachePath, "w")
    cache.write(html)
    cache.close()

def isFresh(file):
    modTime = file.stat().st_mtime
    currTime = time.time()
    return currTime - modTime < 259200 # 3 days