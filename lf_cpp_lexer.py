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
            (r'({=)(.*?)(=})', bygroups(Punctuation, Other, Punctuation)),
            # comments
            (r'#.*?$', Comment),
            (r'\/\/.*?$', Comment),
            (r'\/\*.*?\*\/', Comment),
            # optional semicolon
            (r';', Punctuation),
            # treat a single colon separately if it is preceded of followed by a whitespace
            (r'(:)(\s)', bygroups(Punctuation, Whitespace)),
            (r'(\s)(:)', bygroups(Whitespace, Punctuation)),
            #(r'(^::^:)', Punctuation),
            # custom rules
            (r'(target)(\s*)(Cpp)', bygroups(Keyword, Whitespace, Name.Builtin)),
            (r'(reactor)(\s*)(\w*)', bygroups(Keyword, Whitespace, Name.Class)),
            # keywords
            (words(('input', 'output', 'state', 'new', 'public', 'private', 'preamble', 'import', 'from', 'reaction', 'main', 'reactor', 'after', 'deadline')), Keyword),
            # builtins
            (words(('startup', 'shutdown')), Name.Builtin),
            # time value with unit
            (r'(\d+)(\s*)('+'|'.join(time_units)+r')', bygroups(Number.Integer, Whitespace, Name.Builtin)),
            # Operators 
            (r'->', Operator),
            (r'~>', Operator),
            # Everything else
            (r'.', Other)
        ],
}
