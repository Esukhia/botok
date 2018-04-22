from .trie import PyBoTrie
from .stringutils import PyBoTextChunks
from .tokenizer import Tokenizer
from .syllableutils import BoSyl
from .tokenutils import BoMatcher, TokenSplit, SplittingMatcher


class BoTokenizer:
    """
    Convenience class to tokenize a given string.

    """
    def __init__(self, profile, user_word_list=[]):
        """
        :param profile: profile for building the trie. (see config.yaml)
        """
        self.tok = Tokenizer(PyBoTrie(BoSyl(), profile=profile, user_word_list=user_word_list))

    def tokenize(self, string, split_affixes=True):
        """
        :param string: to be tokenized
        :param split_affixes: separates the affixed particles into seperate tokens if True
        :return: list of pybo.tokenizer.Token objects
        """
        preprocessed = PyBoTextChunks(string)
        return self.tok.tokenize(preprocessed, split_affixes=split_affixes)


VERSION = "0.1.0"

__all__ = ['BoTokenizer', 'PyBoTextChunks', 'PyBoTrie', 'Tokenizer',
           'BoSyl', 'BoMatcher', 'TokenSplit', 'SplittingMatcher']
