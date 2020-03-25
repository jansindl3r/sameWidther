import json
from fontTools.ttLib import TTFont
from getKern.flatten_gpos_kerntable import flatten_gpos_kerning
from pathlib import Path
from random import shuffle
from typing import Union
from defcon import Font

class SameWidther:

    def __init__(
        self, 
        font
    ):
        self.font = font
        if type(font) == TTFont:
            self.kerning = self.TTF_OTF_kerning
            self.metrics = self.TTF_OTF_metrics  
        if type(font) == Font:
            self.kerning = self.UFO_kerning
            self.metrics = self.UFO_metrics

    @property
    def UFO_kerning(self):
        return self.font.kerning

    @property
    def UFO_metrics(self):
        return {glyph.name: glyph.width for glyph in self.font}

    @property
    def TTF_OTF_kerning(self):
        flattened = flatten_gpos_kerning(font)
        if flattened:
            kerning = {(left, right): value for left, right, value in flattened}
            return kerning
        else:
            return {}

    @property
    def TTF_OTF_metrics(self):
        hmtx = font.get('hmtx')
        widths = {k:hmtx[k][0] for k in font.getGlyphOrder()}
        return widths

    def getWords(self,        
        database: list,
        wordWidth: float, 
        wordCount: int, 
        threshold: int = 10,
):
        sameLongLetters = []
        for word in database:
            currentWordWidth = sum(map(lambda x:self.metrics[x], word))
            pairs = [(word[i], word[i+1]) for i in range(len(word)-1)]
            if self.kerning:
                pairsKerning = sum(map(lambda x:self.kerning.get(x, 0), pairs))
                totalWidth = currentWordWidth+pairsKerning
            else:
                totalWidth = currentWordWidth
            if wordWidth-threshold < totalWidth <= wordWidth+threshold:
                sameLongLetters.append(word)
                if len(sameLongLetters) == wordCount:
                    break
        else:
            print('not enough matches')
        return sameLongLetters


font = Font('font.ufo')
# font = TTFont('font.otf')
with open(Path('databases')/'ENG.json') as inputFile:
    database = json.load(inputFile)
    shuffle(database)

print(SameWidther(font).getWords(database, 4000, 10, 10))

