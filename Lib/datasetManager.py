"""
Download manager for word databases. If database is not present locally in the module. It will be downloaded from links defined in resources.json.
"""

import json
import urllib.request as request
import urllib.error as error
from pathlib import Path
from typing import Union

__all__ = ["checkWordIsAlpha", "downloadDataset"]
parent = Path(__file__).parent.absolute()


def checkWordIsAlpha(word: str) -> Union[str, None]:
    for letter in word:
        if not letter.isalpha():
            break
    else:
        return word
    return None


def downloadDataset(language: str) -> None:
    language = language.upper()
    with open(parent / "resources.json") as inputFile:
        resources = json.load(inputFile)

    data = resources.get(language)
    assert data, f"{language} doesn't know where to be downloaded from."

    link, keepCol, splitWhere, dataSorted = data

    try:
        data = request.urlopen(link)
    except error.HTTPError as e:
        print(f"HTTP error: {e.code}")
    except error.URLError as e:
        print(f"URL error: {e.reason}")

    assert data

    dataToWrite = data.read().decode("utf-8").splitlines()
    if dataSorted:
        maxLength = 60_000
        if len(dataToWrite) > maxLength:
            dataToWrite = dataToWrite[:maxLength]

    if keepCol != True:
        dataToWrite = map(lambda x: x.split(splitWhere)[keepCol], dataToWrite)

    dataToWrite = list(filter(checkWordIsAlpha, dataToWrite))

    with open( parent / f"databases/{language}.json", "w+", encoding="utf-8") as outputFile:
        json.dump(dataToWrite, outputFile, ensure_ascii=False)
