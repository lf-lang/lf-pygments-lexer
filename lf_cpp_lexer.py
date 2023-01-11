from pygments.lexer import DelegatingLexer, RegexLexer, bygroups
from pygments.lexers.c_cpp import CppLexer
from pygments.token import *

class CustomLexer(DelegatingLexer):

    name = 'LF-C++'
    filenames = ['*.lf']

    def __init__(self, **options):
        super().__init__(CppLexer, LFLexer, **options)



class LFLexer(RegexLexer):
    tokens = {
        'root': [
            (r'({=)(\s*)(.*?)(\s*)(=})', bygroups(Punctuation, Whitespace, Other, Whitespace, Punctuation)),
            (r'reactor', Keyword)
        ]
    }
