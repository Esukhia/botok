# coding: utf-8
from enum import Enum, unique, IntEnum, auto


AFFIX_SEP = 'ᛃ'
OOV = 'OOV'
TSEK = '་'
NAMCHE = 'ཿ'
SHAD = '།'
AA_TSEK = 'འ་'
HASH = '#'

CharMarkers = IntEnum('CharMarkers', [
    # regular Tibetan
    'CONS',
    'SUB_CONS',
    'VOW',
    'TSEK',
    # punctuation
    'NORMAL_PUNCT',
    'SPECIAL_PUNCT',
    # others
    'NUMERAL',
    'SYMBOL',
    'IN_SYL_MARK',
    'NON_BO_NON_SKRT',
    # sanskrit
    'SKRT_CONS',
    'SKRT_SUB_CONS',
    'SKRT_VOW',
    'SKRT_LONG_VOW',
    # other languages
    'CJK',
    'LATIN',
    # misc
    'OTHER',
    'TRANSPARENT'
], start=1)
char_values = {c.value: c.name for c in CharMarkers}

ChunkMarkers = IntEnum('ChunkMarkers', [
    # languages
    'BO',
    'LATIN',
    'CJK',
    'OTHER',
    # tibetan textual content
    'TEXT',  # replaces syl
    # tibetan non-textual content
    'PUNCT',
    'NON_PUNCT',
    'SPACE',
    'NON_SPACE',
    'SYM',
    'NON_SYM',
    'NUM',
    'NON_NUM'
], start=100)
chunk_values = {c.value: c.name for c in ChunkMarkers}

WordMarkers = IntEnum('WordMarkers', [
    'WORD',
    'OOV'
], start=1000)
word_values = {w.value: w.name for w in WordMarkers}
