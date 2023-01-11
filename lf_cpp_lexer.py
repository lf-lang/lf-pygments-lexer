from pygments.lexer import DelegatingLexer, RegexLexer, bygroups
from pygments.lexers.c_cpp import CppLexer
from pygments.token import *

import re

class CustomLexer(DelegatingLexer):

    name = 'LF-C++'
    filenames = ['*.lf']

    def __init__(self, **options):
        super().__init__(CppLexer, LFLexer, **options)



class LFLexer(RegexLexer):

    flags = re.MULTILINE | re.DOTALL

    tokens = {
        'root': [
            (r'({=)(\s*)(.*?)(\s*)(=})', bygroups(Punctuation, Whitespace, Other, Whitespace, Punctuation)),
            (r'#.*?$', Comment),
            (r'\/\/.*?$', Comment),
            (r'\/\*.*?\*\/', Comment),
            (r'(target)(\s*)(.*?)(\s*)$', bygroups(Keyword, Whitespace, Name.Builtin, Whitespace)),
            (r'main', Keyword),
            (r'(reactor)(\s*)(\w*)', bygroups(Keyword, Whitespace, Name.Class))
        ]
    }
