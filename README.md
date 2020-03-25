# sameWidther
script that accepts OTF/TTF/UFO files and gets you random words of the same width, nice for specimens.

## arguments
#### positional 
- font - path to OTF/TTF/UFO file that you want to use
- language - three letter code of language that you want to have the words in, ENG/GER available
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
