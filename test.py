# from Lib.sameWidther import *
from sameWidther import *
# font = SameWidther(Font('font.ufo'), 'ENG')
font = SameWidther(TTFont('font.otf'), 'GER')
print('\n'.join(font.getWords(3000, 10, case='upper')))