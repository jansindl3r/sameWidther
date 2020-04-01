# sameWidther
script that accepts OTF/TTF/UFO files and gets you random words of the same width, nice for specimens.

## installing
- install this package via pip
```
python -m pip install sameWidther
```

- install directly from cloned repo, navigate to the repo in your terminal
```
python setup.py install
```

## usage
- you can use it as commandline tool
```
sameWidther Desktop/sameWidth/font.ufo ENG 4000 10 
```

- or directly in your python script
```
from sameWidther import SameWidther, TTFont, Font
# font = SameWidther(Font('font.ufo'), 'ENG')
font = SameWidther(TTFont('font.otf'), 'GER')
print(font.getWords(3000, 10, case='upper'))
```

## arguments
#### positional 
- font - path to OTF/TTF/UFO file that you want to use
- language - three letter code of language that you want to have the words in, ENG/GER available. Or provide existing path to a database in json format of such structure `["word", "house", "word2", ...]`
- width - width of the words
- wordCount - number of words that you need
#### optional - keyword arguments
- threshold - (default: 10) how much in width can the words differ
- case - (default: lower) do you want to lower, upper or capitalize the case of the words?

## word databases
- [ENG] English https://github.com/dwyl/english-words
- [GER] German https://github.com/creativecouple/all-the-german-words

## other resources
- customized OTF/TTF kern dump https://gist.github.com/m4rc1e/59017729923ac4930dcd76823c0acb91

Happy Specimening
