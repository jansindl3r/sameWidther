import json
import argparse
import os

from getKern.flatten_gpos_kerntable import flatten_gpos_kerning
from pathlib import Path
from random import shuffle
from typing import Union

try:
    from fontTools.ttLib import TTFont
except:
    print("pease install fontTools with pip")
try:
    from defcon import Font
except:
    print("please install defcon with pip")
    quit()


class SameWidther:
    def __init__(self, font: Union[TTFont, Font]) -> None:
        self.font = font
        if type(font) == TTFont:
            self.kerning = self.TTF_OTF_kerning
            self.metrics = self.TTF_OTF_metrics
        if type(font) == Font:
            self.kerning = self.UFO_kerning
            self.metrics = self.UFO_metrics

    @property
    def UFO_kerning(self) -> dict:
        return self.font.kerning

    @property
    def UFO_metrics(self) -> dict:
        return {glyph.name: glyph.width for glyph in self.font}

    @property
    def TTF_OTF_kerning(self) -> dict:
        flattened = flatten_gpos_kerning(font)
        if flattened:
            kerning = {(left, right): value for left, right, value in flattened}
            return kerning
        else:
            return {}

    @property
    def TTF_OTF_metrics(self) -> dict:
        hmtx = font.get("hmtx")
        widths = {k: hmtx[k][0] for k in font.getGlyphOrder()}
        return widths

    def getWords(
        self, database: list, wordWidth: float, wordCount: int, threshold: int = 10,
    ) -> list:
        sameLongLetters = []
        for word in database:
            currentWordWidth = sum(map(lambda x: self.metrics[x], word))
            pairs = [(word[i], word[i + 1]) for i in range(len(word) - 1)]
            if self.kerning:
                pairsKerning = sum(map(lambda x: self.kerning.get(x, 0), pairs))
                totalWidth = currentWordWidth + pairsKerning
            else:
                totalWidth = currentWordWidth
            if wordWidth - threshold < totalWidth <= wordWidth + threshold:
                sameLongLetters.append(word)
                if len(sameLongLetters) == wordCount:
                    break
        else:
            print("not enough matches")
        return sameLongLetters


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Get words of the same width, nice for specimens."
    )
    parser.add_argument(
        "font", type=Path, help="OTF/TTF/UFO file which you want to use"
    )
    parser.add_argument("language", type=lambda x:x.upper(), help="three letter short for language of word database, currently available [ENG, GER]")
    parser.add_argument(
        "width",
        type=float,
        help="""How wide should the words be? Width of font's units. (400-500) is normally width of a letter""",
    )
    parser.add_argument("wordCount", type=int, help="How many words you need?")
    parser.add_argument(
        "-t", "--threshold", type=float, default=10, help="(optional) Threshold for the width"
    )

    args = parser.parse_args()

    assert f'{args.language}.json' in os.listdir('databases'), 'database not found in the script\'s directory'

    suffix = args.font.suffix.lower()
    if suffix == '.ufo':
        font = Font(args.font)
    if suffix in ['.ttf', '.otf']:
        font = TTFont(args.font)

    with open(Path("databases") / f"{args.language}.json") as inputFile:
        database = json.load(inputFile)
        shuffle(database)
        sameWidther = SameWidther(font)
        print("\n".join(sameWidther.getWords(database, args.width, args.wordCount, threshold=args.threshold)))
