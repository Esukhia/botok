# coding: utf-8
from types import FunctionType
from pathlib import Path

from .pipelinebase import PipelineBase
from ..vars import Ids

from .preprocess import *
from .tokenize import *
from .modify import *
from .format import *

builtin_pipes = {
    # a. Preprocessing
    'prep': {
        'dummy': lambda x: x,
        'basic_cleanup': basic_cleanup,
        'basic_keeps_lines': basic_keeps_lines,
    },
    # b. Tokenizers
    'tok': {
        'space_tok': space_tok,
        'word_tok': word_tok,
        'chunk_tok': chunk_tok,
    },
    # c. Modifiers
    'mod': {
        'dummy': lambda x: x,
        'words_raw_text': words_raw_text,
        'words_raw_types': words_raw_types,
        'words_error_types': words_error_types,
        'words_error_concs': words_error_concs,
        'chunks_raw_text': chunks_raw_text,
    },
    # d. Formatters
    'form': {
        'dummy': lambda x: x,
        'plaintext': plaintext,
        'basic_concs': basic_conc,
        'stats_types': stats_types,
    }
}


class Text:
    """
    Takes as input:
        - a string to process
        - the Path object of a file to process

    including a custom pipeline is as simple as:
        - subclassing Text class
        - creating a new @property method like the built in ones while providing your own arguments to self.__process()
    """
    def __init__(self, input, out_file=None):
        """
        if input == str: return a string
        if input == Path:
                            1. out_file != None: write to given Path object
                            2. out_file == None: write to cwd and append "_pybo" to file name
        """
        self.input = input
        if isinstance(input, str):
            if out_file:
                assert isinstance(out_file, Path)
                self.out_file = out_file
            else:
                self.out_file = None
        elif isinstance(input, Path):
            if not out_file:
                self.out_file = Path.cwd() / f'{input.stem}_pybo{input.suffix}'
            else:
                self.out_file = out_file
        else:
            raise TypeError('input should either be a string, or a Path object')

    @property
    def tokenize_on_spaces(self):
        return self.__process('basic_cleanup', 'space_tok', 'dummy', 'plaintext')

    @property
    def tokenize_words_raw_text(self):
        return self.__process('basic_cleanup', 'word_tok', 'words_raw_text', 'plaintext', wordtok_profile='GMD')

    @property
    def tokenize_words_raw_lines(self):
        return self.__process('basic_keeps_lines', 'word_tok', 'words_raw_text', 'plaintext', wordtok_profile='GMD')

    @property
    def tokenize_chunks_plaintext(self):
        return self.__process('basic_keeps_lines', 'chunk_tok', 'chunks_raw_text', 'plaintext')

    @property
    def list_word_types(self):
        return self.__process('basic_keeps_lines', 'chunk_tok', 'words_raw_types', 'stats_types', wordtok_profile='GMD')

    def custom_pipeline(self, preprocessor, tokenizer, modifier, formatter, wordtok_profile=None):
        """
        every pipe should be either the name of an existing pipe as found in builtin_pipes or a function
        """
        return self.__process(preprocessor, tokenizer, modifier, formatter, wordtok_profile)

    def __process(self, preprocessor, tokenizer, modifier, formatter, wordtok_profile=None):
        profile, pipes = self.__create_pipeline(preprocessor, tokenizer, modifier, formatter, wordtok_profile)
        pipeline = PipelineBase(profile, pipes=pipes)
        if self.out_file:
            return pipeline.pipe_file(self.input, self.out_file)
        else:
            return pipeline.pipe_str(self.input)

    @staticmethod
    def __create_pipeline(preprocessor, tokenizer, modifier, formatter, wordtok_profile=None):
        profile = {}
        pipes = {'prep': {}, 'tok': {}, 'mod': {}, 'form': {}}
        for a, b, c in [('prep', Ids.prep, preprocessor), ('tok', Ids.tok, tokenizer), ('mod', Ids.mod, modifier),
                        ('form', Ids.form, formatter)]:
            if isinstance(c, FunctionType):
                pipes[a].update({b: c})
                profile[a] = b
            elif isinstance(c, str):
                profile[a] = c
                assert c in builtin_pipes[a]
                pipes[a][c] = builtin_pipes[a][c]
            else:
                raise SyntaxError('Should be either a function or a string')

        if wordtok_profile and isinstance(wordtok_profile, str):
            profile['wordtok_profile'] = wordtok_profile
        return profile, pipes
