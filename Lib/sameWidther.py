import argparse
import os
import json

from random import shuffle
from pathlib import Path
from flattenKern import flatten_gpos_kerning
from typing import Union
from fontTools.ttLib import TTFont
from defcon import Font

__all__ = ['SameWidther', 'TTFont', 'Font']

class SameWidther:
    def __init__(self, font: Union[TTFont, Font], language: str) -> None:
        self.font = font
        if type(font) == TTFont:
            self.uni_name = self.TTF_OTF_unicodeMap
            self.name_uni = {v: k for k, v in self.uni_name.items()}
            self.kerning = self.TTF_OTF_kerning
            self.metrics = self.TTF_OTF_metrics
            unitsPerEm = self.font["head"].unitsPerEm
        if type(font) == Font:
            self.uni_name = self.UFO_unicodeMap
            self.name_uni = {v: k for k, v in self.uni_name.items()}
            self.kerning = self.UFO_kerning
            self.metrics = self.UFO_metrics
            unitsPerEm = self.font.info.unitsPerEm
        self.scale = unitsPerEm / 1000
        with open(
            Path(__file__).parent/'databases'/f"{language}.json", encoding="utf-8"
        ) as inputFile:
            self.database = json.load(inputFile)
        shuffle(self.database)
    

    @property
    def UFO_kerning(self) -> dict:
        return self.font.kerning

    @property
    def UFO_metrics(self) -> dict:
        return {glyph.unicode: glyph.width for glyph in self.font}

    @property
    def UFO_unicodeMap(self) -> dict:
        return {glyph.unicode: glyph.name for glyph in self.font}

    @property
    def TTF_OTF_kerning(self) -> dict:
        flattened = flatten_gpos_kerning(self.font)
        if flattened:
            kerning = {
                (self.name_uni.get(left), self.name_uni.get(right)): value
                for left, right, value in flattened
            }
            return kerning
        else:
            return {}

    @property
    def TTF_OTF_metrics(self) -> dict:
        hmtx = self.font.get("hmtx")
        widths = {self.name_uni.get(k): hmtx[k][0] for k in self.font.getGlyphOrder()}
        return widths

    @property
    def TTF_OTF_unicodeMap(self) -> dict:
        return self.font.getBestCmap()

    def getWords(
        self, wordWidth: float, wordCount: int, threshold: int = 10, case: str = 'lower'
    ) -> list:
        sameLongLetters = []
        for word in self.database:
            word = getattr(str, case)(word)
            currentWordWidth = sum(map(lambda x: self.metrics[ord(x)], word))
            pairs = [(word[i], word[i + 1]) for i in range(len(word) - 1)]
            if self.kerning:
                pairsKerning = sum(
                    map(lambda x: self.kerning.get(tuple(map(ord, x)), 0), pairs)
                )
                totalWidth = currentWordWidth + pairsKerning
            else:
                totalWidth = currentWordWidth
            totalWidth /= self.scale
            if wordWidth - threshold < totalWidth <= wordWidth + threshold:
                sameLongLetters.append(word)
                if len(sameLongLetters) == wordCount:
                    break
        else:
            print("not enough matches")
        return sameLongLetters


class Args:
    def __init__(self) -> None:
        parser = argparse.ArgumentParser(
            description="Get words of the same width, nice for specimens."
        )
        parser.add_argument(
            "font", type=Path, help="OTF/TTF/UFO file which you want to use"
        )
        parser.add_argument(
            "language",
            type=lambda x: x.upper(),
            help="three letter short for language of word database, currently available [ENG, GER]",
        )
        parser.add_argument(
            "width",
            type=float,
            help="""How wide should the words be? Width of font's units. (400-500) is normally width of a letter""",
        )
        parser.add_argument("wordCount", type=int, help="How many words you need?")
        parser.add_argument(
            "-t",
            "--threshold",
            type=float,
            default=10,
            help="(optional, default:10) Threshold for the width",
        )
        parser.add_argument(
            "-c",
            "--case",
            type=str,
            default="lower",
            help="(optional, default:lower) change case of the words [upper, lower, capitalize]",
        )
        self.parser = parser.parse_args()


def run(args) -> None:
    suffix = args.font.suffix.lower()
    if suffix == ".ufo":
        font = Font(args.font)
    if suffix in [".ttf", ".otf"]:
        font = TTFont(args.font)

    sameWidther = SameWidther(font, 'ENG')
    print(
        "\n".join(
            sameWidther.getWords(
                args.width, args.wordCount, threshold=args.threshold, case=args.case
            )
        )
    )

def main() -> None:
    args = Args()
    run(args.parser)

if __name__ == "__main__":
    main()
