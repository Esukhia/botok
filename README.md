<a target="_blank" rel="noopener noreferrer" href="http://www.montypython.net/sounds/sketches/exparrot.wav"> <img src=https://github.com/Esukhia/pybo/blob/master/pybo_logo.png width=150> </a>

# PYBO - Tibetan NLP in Python
[![Build Status](https://travis-ci.org/Esukhia/pybo.svg?branch=master)](https://travis-ci.org/Esukhia/pybo)  [![Coverage Status](https://coveralls.io/repos/github/Esukhia/pybo/badge.svg?branch=master)](https://coveralls.io/github/Esukhia/pybo?branch=master) ![GitHub release](https://img.shields.io/github/release/Esukhia/pybo.svg) [![CodeFactor](https://www.codefactor.io/repository/github/esukhia/pybo/badge)](https://www.codefactor.io/repository/github/esukhia/pybo)[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)


<div><div class="mediaContainer" style="width:220px"><audio id="mwe_player_0" controls="" preload="none" style="width:220px" class="kskin" data-durationhint="31.205238095238" data-startoffset="0" data-mwtitle="Parrot_sketch.ogg" data-mwprovider="local"><source src="//upload.wikimedia.org/wikipedia/en/4/4e/Parrot_sketch.ogg" type="audio/ogg; codecs=&quot;vorbis&quot;" data-title="Original Ogg file (47 kbps)" data-shorttitle="Ogg source" data-width="0" data-height="0" data-bandwidth="47057" /><source src="//upload.wikimedia.org/wikipedia/en/transcoded/4/4e/Parrot_sketch.ogg/Parrot_sketch.ogg.mp3" type="audio/mpeg" data-title="MP3" data-shorttitle="MP3" data-transcodekey="mp3" data-width="0" data-height="0" data-bandwidth="118288" /><track src="/w/api.php?action=timedtext&amp;title=File%3AParrot_sketch.ogg&amp;lang=en&amp;trackformat=srt" kind="subtitles" type="text/x-srt" srclang="en" label="English (en) subtitles" data-dir="ltr" /></audio></div></div>



## Overview

pybo is a word tokenizer for the Tibetan language written in Python. pybo takes in chunks of text and returns lists of words. It provides an easy-to-use, high-performance tokenization pipeline that can serve as a stand-alone solution or be adapted as a complement.


## Getting started

    pip install pybo
    
Or to install from the latest master branch:

    pip install git+https://github.com/Esukhia/pybo.git

## How to use pybo

#### To initiate the tokenizer together with part-of-speech capability: 

    # Initialize the tokenizer
    tok = bo.WordTokenizer('POS')
    
    # Feed it some Tibetan text
    input_str = '༄༅། །རྒྱ་གར་སྐད་དུ། བོ་དྷི་སཏྭ་ཙརྻ་ཨ་བ་ཏ་ར། བོད་སྐད་དུ། བྱང་ཆུབ་སེམས་དཔའི་སྤྱོད་པ་ལ་འཇུག་པ། །སངས་རྒྱས་དང་བྱང་ཆུབ་སེམས་དཔའ་ཐམས་ཅད་ལ་ཕྱག་འཚལ་ལོ། །བདེ་གཤེགས་ཆོས་ཀྱི་སྐུ་མངའ་སྲས་བཅས་དང༌། །ཕྱག་འོས་ཀུན་ལའང་གུས་པར་ཕྱག་འཚལ་ཏེ། །བདེ་གཤེགས་སྲས་ཀྱི་སྡོམ་ལ་འཇུག་པ་ནི། །ལུང་བཞིན་མདོར་བསྡུས་ནས་ནི་བརྗོད་པར་བྱ། །'
    
    # Run the tokenizer
    tokens = tok.tokenize(input_str)
    
#### Now in 'tokens' you have an iterable where each token consist of several meta-data:

    # Access the first token in the iterable
    tokens[0]

This yields:

    text: "༄༅། "
    char_types: |PUNCT|PUNCT|PUNCT|SPACE|
    chunk_type: PUNCT
    start: 0
    len: 4
    syls: None
    pos: PUNCT
    skrt: False
    freq: 0
    
notes:
 - `start` is the starting index of the current token in the input string.
 - `syls` is a list of cleaned syllables, each syllable being represented as a list of indices.
Each index leads to a constituting character within the input string. 

#### How to access all the words in a list 

    # iterate through the tokens object to get all the words in a list
    [t.content for t in tokens]

#### How to get all the nouns in a text

    # extract nouns from the tokens
    [t.content for t in tokens if t.tag == 'NOUNᛃᛃᛃ']
    
These examples highlight the basic principle of accessing attributes within each token object. 

## Acknowledgements

**pybo** is an open source library for Tibetan NLP.

We are always open to cooperation in introducing new features, tool integrations and testing solutions.

Many thanks to the companies and organizations who have supported pybo's development, especially:

* [Khyentse Foundation](https://khyentsefoundation.org) for contributing USD22,000 to kickstart the project 
* The [Barom/Esukhia canon project](http://www.barom.org) for sponsoring training data curation
* [BDRC](https://tbrc.org) for contributing 2 staff for 6 months for data curation

## Maintainance

Build the source dist:

```
rm -rf dist/
python3 setup.py clean sdist
```

and upload on twine (version >= `1.11.0`) with:

```
twine upload dist/*
```

## License

The Python code is Copyright (C) 2019 Esukhia, provided under [Apache 2](LICENSE). 

author: [Drupchen](https://github.com/drupchen)

contributors:
 * [Élie Roux](https://github.com/eroux)
 * [Thubten Rinzin](https://github.com/thubtenrigzin)
 * [Ngawang Trinley](https://github.com/ngawangtrinley)
 * [Mikko Kotila](https://github.com/mikkokotila)
 * [Tenzin](https://github.com/10zinten)
 * Joyce Mackzenzie for reworking the logo
