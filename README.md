# sameWidther
This is a tool for getting words of same visual width. It accepts OTF/TTF/UFO files and gets you random words of the same visual width, useful for example for type specimens.

## installing
1. Install directly from this cloned repo. This way you will always get the most recent version. Navigate to the repo in your terminal and execute this command
    ```
    python setup.py install
    ```
1. Install this package via pip. This won't be updated that often but it offer more convenient way of installing a package.
    ```
    python -m pip install sameWidther
    ```

## usage
- you can use it as commandline tool
    ```
    sameWidther Desktop/sameWidth/font.ufo ENG 4000 10 
    ```

- or directly in your python script
    ```
    from sameWidther import SameWidther, TTFont, Font
    # font = SameWidther(Font('font.ufo'), 'ENG') # for UFOs
    font = SameWidther(TTFont('font.otf'), 'GER') # for OTFs, TTFs
    print(font.getWords(3000, 10, case='upper'))
    ```

## arguments
1. positional 
    * `font` - path to OTF/TTF/UFO file that you want to use
    * `language` - three letter code of language that you want to have the words in, ENG/GER available locally. Other languages under three letter code 639-2/B are available too. SameWidther's dataset manager will download them on the first request. You can also provide existing path to a database in json format of such structure `["word", "house", "word2", ...]`
    * `width` - width of the words
    * `wordCount` - number of words that you need
1. optional - keyword arguments
    * threshold - (default: 10) how much in width can the words differ
    * case - (default: lower) do you want to lower, upper or capitalize the case of the words?

## word databases
- [ENG] English https://github.com/dwyl/english-words
- [GER] German https://github.com/creativecouple/all-the-german-words
- for other available languages see `Lib/resources.json`

## other resources
- customized OTF/TTF kern dump https://gist.github.com/m4rc1e/59017729923ac4930dcd76823c0acb91


Happy Specimening
