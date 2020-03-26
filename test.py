import unittest
from Lib.sameWidther import SameWidther, TTFont, Font

class SameWidtherTest(unittest.TestCase):
    def __init__(self):
        self.fonts = [
            SameWidther(Font('font.ufo'), 'ENG'),
            SameWidther(Font('font.ufo'), 'GER'),
            SameWidther(TTFont('font.otf'), 'GER'),
            SameWidther(TTFont('font.ttf'), 'GER')
        ]

    def test_getWords(self, width=3000, length=5):
        for font in fonts:
            self.assertEqual(len(font.getWords(width, length)), length)

if __name__ == '__main__':
    SameWidtherTest()
    unittest.main()

    