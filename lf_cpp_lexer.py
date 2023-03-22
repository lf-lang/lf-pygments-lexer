from pygments.lexer import DelegatingLexer, RegexLexer, bygroups, words, include
from pygments.lexers.c_cpp import CppLexer
from pygments.token import *

import re

# Known limitations:
#  - The comment rules do not support nested comments
#  - For target properties that have a hyphen in there name, the hyphen is
#    highlighted like an operator

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
            # single colons are punctuation, double colons will be handled by the target lexer
            (r'(?<!:):(?!:)', Punctuation),
            # custom rules
            (r'(target)(\s*)(Cpp)', bygroups(Keyword, Whitespace, Name.Builtin)),
            (r'(reactor)(\s*)(\w*)', bygroups(Keyword, Whitespace, Name.Class)),
            (r'(input)([.*?])?(\s*)(\w*)', bygroups(Keyword, Other, Whitespace, Name.Variable)),
            (r'(output)([.*?])?(\s*)(\w*)', bygroups(Keyword, Other, Whitespace, Name.Variable)),
            (r'(action)(\s*)(\w*)', bygroups(Keyword, Whitespace, Name.Variable)),
            (r'(state)(\s*)(\w*)', bygroups(Keyword, Whitespace, Name.Variable)),
            (r'(\w*)(\s*)(=)(\s*)(new)', bygroups(Name.Variable, Whitespace, Operator, Keyword)),
            # keywords
            (words(('input', 'output', 'state', 'new', 'public', 'private', 'preamble', 'import',
                    'from', 'reaction', 'main', 'reactor', 'after', 'deadline', 'logical',
                    'physical', 'action'), prefix=r'\b', suffix=r'\b'), Keyword),
            # builtins
            (words(('startup', 'shutdown'), prefix=r'\b', suffix=r'\b'), Name.Builtin),
            (words(('time',), prefix=r'\b', suffix=r'\b'), Keyword.Type),
            # time value with unit
            (r'(\d+)(\s*)('+'|'.join(time_units)+r')', bygroups(Number.Integer, Whitespace, Name.Builtin)),
            # Operators
            (r'->', Operator),
            (r'~>', Operator),
            # Everything else
            (r'.', Other)
        ],
}
