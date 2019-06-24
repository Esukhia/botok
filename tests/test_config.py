# coding: utf8
from pybo import Config
from pathlib import Path


def test_config():
    config = Config()

    # default config filename
    assert config.filename.name == 'pybo.yaml'  # config.filename is a Path object

    # paths for trie content
    main, custom = config.get_tok_data_paths('POS')
    # each profile contains one or more sections
    assert [m for m in main] == ['lexica_bo', 'pos']
    # each element in a Path object leading to a resource file
    assert isinstance(main['pos'][0], Path)

    # custom files to overwrite the existing trie can be added as follows
    assert len(custom) == 0
    main, custom = config.get_tok_data_paths('POS', modifs='trie_data/')
    assert [c for c in custom] == ['lexica_bo', 'lemmas'] == [t.parts[-1] for t in Path('trie_data/').glob('*')]

    # overwriting the main profile
    main, custom = config.get_tok_data_paths('trie_data/', mode='custom')
    assert [m for m in main] == ['lexica_bo', 'lemmas']