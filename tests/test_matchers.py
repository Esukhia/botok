# coding: utf8
from botok import *
from pathlib import Path

from helpers import pos_tok

rules_path = Path(__file__).parent / "resources"
main, custom = Config().get_adj_data_paths("basic", rules_path)


input_str = " མཐའི་རྒྱ་མཚོའི་གླིང་། ཤི་བཀྲ་ཤིས་  tr བདེ་་ལེ གས། བཀྲ་ཤིས་བདེ་ལེགས་ཀཀ"
tokens = pos_tok.tokenize(input_str, split_affixes=False)

# IMPORTANT: all the tests have merely been adapted after refactorisation.
# They should be split in tests per file that also show the expected behaviour of every matcher.


def test_cql_query():
    query = '[text="ན"] []'
    q = Query(query)
    assert q


def test_dummy_cql():
    test = [
        {"word": "This", "lemma": "this", "tag": "Det"},
        {"word": "is", "lemma": "be", "tag": "Verb"},
        {"word": "it", "lemma": "it", "tag": "Pron"},
        {"word": ".", "lemma": ".", "tag": "Punct"},
    ]
    q = '[lemma="this" & tag="Det"] [tag!="ADJ"]'

    matcher = CQLMatcher(q)
    matched = matcher.match(test)
    assert matched == [(0, 1)]


def test_regex_in_cql_query():
    test = [
        {"word": "This", "lemma": "this", "tag": "Det"},
        {"word": "is", "lemma": "be", "tag": "Verb"},
        {"word": "it", "lemma": "it", "tag": "Pron"},
        {"word": ".", "lemma": ".", "tag": "Punct"},
    ]
    q = '[lemma="[^\n\s]+s" & tag="Det"] [tag!="ADJ"]'

    matcher = CQLMatcher(q)
    matched = matcher.match(test)
    expected = [test[m]["word"] for match in matched for m in match]
    assert expected == ["This", "is"]


def test_cql():
    query = '[pos="NOUN" & text!=""] []'
    matcher = CQLMatcher(query)
    slices = matcher.match(tokens)
    slice_strings = [
        tuple([tokens[i].text for i in range(start, end + 1)]) for start, end in slices
    ]
    assert slices == [(0, 1), (1, 2), (2, 3), (5, 6), (7, 8), (9, 10), (10, 11)]
    assert slice_strings == [
        (" མཐའི་", "རྒྱ་མཚོའི་"),
        ("རྒྱ་མཚོའི་", "གླིང་"),
        ("གླིང་", "། "),
        ("བཀྲ་ཤིས་  ", "tr "),
        ("བདེ་་ལེ གས", "། "),
        ("བཀྲ་ཤིས་", "བདེ་ལེགས་"),
        ("བདེ་ལེགས་", "ཀཀ"),
    ]


def test_token_split():
    ts = TokenSplit(
        tokens[3],
        1,
        token_changes='[chunk_type="SPACE" & pos="PUNCT" & affix_host="False"] []',
    )
    first, second = ts.split()
    assert first.chunk_type == "SPACE"
    assert first.pos == "PUNCT"


def test_token_merge():
    tm = TokenMerge(tokens[0], tokens[1])
    merged = tm.merge()
    assert merged


def test_match_split():
    match_query = '[pos="NOUN" & text!=""] []'
    replace_idx = 1  # slot number in match query
    split_idx = 1  # char index in token.content where split should occur
    replace = '[chunk_type="XXX" & pos="xxx"] []'

    sm = SplittingMatcher(match_query, replace_idx, split_idx, tokens, replace)
    split_tokens = sm.split_on_matches()
    assert len(tokens) == 12
    assert len(split_tokens) == 19


def test_match_merge():
    match_query = '[pos="NOUN" & text!=""] []'
    replace_idx = 1  # slot number in match query
    replace = '[chunk_type="XXX" & pos="xxx"]'

    mm = MergingMatcher(match_query, replace_idx, tokens, replace)
    merged_tokens = mm.merge_on_matches()
    assert len(tokens) == 12
    assert len(merged_tokens) == 7


def test_match_replace():
    match_query = '[pos="NOUN" & text!=""] []'
    replace_idx = 1
    replace = '[chunk_type="XXX" & pos="xxx"]'

    ReplacingMatcher(match_query, replace_idx, tokens, replace).replace_on_matches()
    assert len(tokens) == 12
    assert tokens[1].pos == "xxx"
    assert tokens[4].pos == "VERB"


def test_adjust_tokens():
    string = "ལ་ལ་ལ་ལ་ལ་བ་ཡོད།"
    token_list = pos_tok.tokenize(string, split_affixes=False)
    at = AdjustTokens(main=main, custom=custom)
    adjusted = at.adjust(token_list)
    assert token_list[0].text == "ལ་ལ་"
    assert token_list[1].text == "ལ་ལ་"

    assert adjusted[0].text == "ལ་"
    assert adjusted[0].pos == "PART"
    assert adjusted[1].text == "ལ་ལ་"
    assert adjusted[1].pos == "PART"
    assert adjusted[2].text == "ལ་"
    assert adjusted[2].pos == "PART"


def test_last_token():
    token1 = Token()
    token1.pos = "NOUN"

    token2 = Token()
    token2.pos = "VERB"

    matcher = CQLMatcher('[pos="NOUN"]')
    slices = matcher.match([token1, token2])
    assert slices == [(0, 0)]

    matcher = CQLMatcher('[pos="VERB"]')
    slices = matcher.match([token1, token2])
    assert slices == [(1, 1)]


def test_merge_dagdra():
    token_list = pos_tok.tokenize("བཀྲ་ཤིས་-པ་")
    token_list = [
        t for t in token_list if t.text != "-"
    ]  # remove the "-" inserted to ensure we have two tokens
    mp = MergeDagdra()
    mp.merge(token_list)
    assert len(token_list) == 1 and token_list[0].text == "བཀྲ་ཤིས་པ་"

    token_list = pos_tok.tokenize("བཀྲ་ཤིས་-པའོ།")
    token_list = [
        t for t in token_list if t.text != "-"
    ]  # remove the "-" inserted to ensure we have two tokens
    mp.merge(token_list)
    assert len(token_list) == 3 and token_list[0].text == "བཀྲ་ཤིས་པ"
