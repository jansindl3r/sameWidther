"""
get words of same width in given font
"""

import random
import argparse
import os
import json
import pathlib
import defcon

from flattenKern import flatten_gpos_kerning
from datasetManager import downloadDataset

from typing import Union
from fontTools.ttLib import TTFont


__all__ = ["SameWidther", "TTFont", "Font"]


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
        self.database = self.loadDatabase(language)
        random.shuffle(self.database)

    def loadDatabase(self, language: str) -> list:
        """ loads database, either from inbuilt or your own if existing path provided """
        customDatabase = pathlib.Path(language)
        databaseFolder = pathlib.Path(__file__).parent / "databases"

        if customDatabase.exists() and customDatabase.suffix == ".json":
            path = customDatabase.absolute()
        else:
            for i in range(2):
                path = databaseFolder / f"{language.upper()}.json"
                if i == 1 or path.exists():
                    break
                else:
                    downloadDataset(language)

        assert path.exists()

        with open(path, encoding="utf-8") as inputFile:
            data = json.load(inputFile)
        return data

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
        self, wordWidth: float, wordCount: int, threshold: int = 10, case: str = "lower"
    ) -> list:
        sameLongLetters = []
        wordsMissingGlyphs = 0
        for word in self.database:
            word = getattr(str, case)(word)
            currentWordWidth = list(map(lambda x: self.metrics.get(ord(x), None), word))
            if None in currentWordWidth:
                # glyph not in font
                wordsMissingGlyphs += 1
                continue
            pairs = [(word[i], word[i + 1]) for i in range(len(word) - 1)]
            totalWidth: int = sum(currentWordWidth)
            if self.kerning:
                pairsKerning = sum(
                    map(lambda x: self.kerning.get(tuple(map(ord, x)), 0), pairs)
                )
                totalWidth += pairsKerning
            totalWidth /= self.scale # scale widths to 1000 upm
            if wordWidth - threshold < totalWidth <= wordWidth + threshold:
                sameLongLetters.append(word)
                if len(sameLongLetters) == wordCount:
                    break
        else:
            print(
                f"not enough matches. {wordsMissingGlyphs} words contained a missing glyph"
            )
        return sameLongLetters


class Args:
    def __init__(self) -> None:
        parser = argparse.ArgumentParser(
            description="Get words of the same visual width, useful for specimens."
        )
        parser.add_argument(
            "font", type=Path, help="OTF/TTF/UFO file which you want to use"
        )
        parser.add_argument(
            "language",
            type=str,
            help='three letter short for language of word database, currently available [ENG, GER]. Or provide existing path to a existing database. It must be list a list in JSON file. With such structure: ["word", "house", "apple", ...]',
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
        font = defcon.Font(args.font)
    if suffix in [".ttf", ".otf"]:
        font = TTFont(args.font)

    sameWidther = SameWidther(font, args.language)
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
