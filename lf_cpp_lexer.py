from pygments.lexer import RegexLexer
from pygments.token import *

class CustomLexer(RegexLexer):

    name = 'LF-C++'
    filenames = ['*.lf']

    tokens = {
        'root': [
            (r'reactor', Keyword),
        ]
    }
