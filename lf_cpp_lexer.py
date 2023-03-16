from pygments.lexer import DelegatingLexer, RegexLexer, bygroups, words, include
from pygments.lexers.c_cpp import CppLexer
from pygments.token import *

import re


time_units = [
    'nsec', 'nsecs', 'ns',
    'usec', 'usecs', 'us',
    'msec', 'msecs', 'ms',
    'sec', 'secs', 's', 'second', 'seconds',
    'min', 'mins', 'm', 'minute', 'minutes',
    'hour', 'hours', 'h',
    'day', 'days', 'd',
    'week', 'weeks',
]


class CustomLexer(DelegatingLexer):

    name = 'LF-C++'
    filenames = ['*.lf']

    def __init__(self, **options):
        super().__init__(CppLexer, LFLexer, **options)



class LFLexer(RegexLexer):

    flags = re.MULTILINE | re.DOTALL

    tokens = {
        'root': [
            # target code blocks
            (r'({=)(\s*)(.*?)(\s*)(=})', bygroups(Punctuation, Whitespace, Other, Whitespace, Punctuation)),
            # comments
            (r'#.*?$', Comment),
            (r'\/\/.*?$', Comment),
            (r'\/\*.*?\*\/', Comment),
            # optional semicolon
            (r';', Punctuation),
            # target declaration
            (r'(target)(\s*)(.*?)(\s*)$', bygroups(Keyword, Whitespace, Name.Builtin, Whitespace)),
            (r'main', Keyword),
            (r'(reactor)(\s*)(\w*)', bygroups(Keyword, Whitespace, Name.Class)),
            # expressions
            include('expression'),
        ],
        'expression': [
            # time value with unit
            (r'(\d+)(\s*)('+'|'.join(time_units)+r')', bygroups(Number.Integer, Whitespace, Name.Builtin)),
            # other expressions
            include('numbers'),
            include('strings'),
        ],
        'numbers': [
            (r'(\d+\.\d*|\d*\.\d+)([eE][+-]?[0-9]+)?j?', Number.Float),
            (r'\d+[eE][+-]?[0-9]+j?', Number.Float),
            (r'\d+?', Number.Integer),
        ],
        'strings': [
            (r'".*?"', String.Double),
            (r"'.'" , String.Char),
            (r"'.*?'", String.Single),
        ],
    }
