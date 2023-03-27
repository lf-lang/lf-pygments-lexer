from pygments.lexer import DelegatingLexer, RegexLexer, bygroups, words, include
from pygments.lexers.c_cpp import CLexer, CppLexer
from pygments.lexers.javascript import TypeScriptLexer
from pygments.lexers.python import PythonLexer
from pygments.lexers.rust import RustLexer
from pygments.token import *

import re

__all__ = ["LFLexer", "LFCLexer", "LFCppLexer", "LFPythonLexer", "LFRustLexer", "LFTypeScriptLexer"]

# Known limitations:
#  - The comment rules do not support nested comments
#  - For target properties that have a hyphen in there name, the hyphen is
#    highlighted like an operator

time_units = [
    "nsec",
    "nsecs",
    "ns",
    "usec",
    "usecs",
    "us",
    "msec",
    "msecs",
    "ms",
    "sec",
    "secs",
    "s",
    "second",
    "seconds",
    "min",
    "mins",
    "m",
    "minute",
    "minutes",
    "hour",
    "hours",
    "h",
    "day",
    "days",
    "d",
    "week",
    "weeks",
]

keywords = (
    "input",
    "output",
    "state",
    "new",
    "public",
    "private",
    "preamble",
    "import",
    "from",
    "reaction",
    "main",
    "reactor",
    "after",
    "deadline",
    "logical",
    "physical",
    "action",
    "federated",
)


class LFCLexer(DelegatingLexer):
    name = "Lingua Franca with C target"
    aliases = ["lf-c"]
    filenames = ["*.lf"]

    def __init__(self, **options):
        super().__init__(CLexer, LFLexer, **options)

    def analyse_text(text):
        return re.search(r"^\s*target\s*C\b", text, re.M) and 1.0

class LFCppLexer(DelegatingLexer):
    name = "Lingua Franca with C++ target"
    aliases = ["lf-cpp"]
    filenames = ["*.lf"]

    def __init__(self, **options):
        super().__init__(CppLexer, LFLexer, **options)

    def analyse_text(text):
        return re.search(r"^\s*target\s*Cpp\b", text, re.M) and 1.0


class LFPythonLexer(DelegatingLexer):
    name = "Lingua Franca with Python target"
    aliases = ["lf-python", "lf-py"]
    filenames = ["*.lf"]

    def __init__(self, **options):
        super().__init__(PythonLexer, LFLexer, **options)

    def analyse_text(text):
        return re.search(r"^\s*target\s*Python\b", text, re.M) and 1.0


class LFRustLexer(DelegatingLexer):
    name = "Lingua Franca with Rust target"
    aliases = ["lf-rust", "lf-rs"]
    filenames = ["*.lf"]

    def __init__(self, **options):
        super().__init__(RustLexer, LFLexer, **options)

    def analyse_text(text):
        return re.search(r"^\s*target\s*Rust\b", text, re.M) and 1.0


class LFTypeScriptLexer(DelegatingLexer):
    name = "Lingua Franca with TypeScript target"
    aliases = ["lf-typescript", "lf-ts"]
    filenames = ["*.lf"]

    def __init__(self, **options):
        super().__init__(TypeScriptLexer, LFLexer, **options)

    def analyse_text(text):
        return re.search(r"^\s*target\s*TypeScript\b", text, re.M) and 1.0


class LFLexer(RegexLexer):
    flags = re.MULTILINE | re.DOTALL

    tokens = {
        "root": [
            # target code blocks
            (r"({=)(.*?)(=})", bygroups(Punctuation, Other, Punctuation)),
            # comments
            (r"#.*?$", Comment),
            (r"\/\/.*?$", Comment),
            (r"\/\*.*?\*\/", Comment),
            # optional semicolon
            (r";", Punctuation),
            # single colons are punctuation, double colons will be handled by the target lexer
            (r"(?<!:):(?!:)", Punctuation),
            # custom rules
            (
                r"(\btarget)(\s*)(C\b|Cpp|Python|Rust|TypeScript)",
                bygroups(Keyword, Whitespace, Name.Builtin),
            ),
            (r"(\breactor)(\s*)(\w*)", bygroups(Keyword, Whitespace, Name.Class)),
            (r"(\binput)([.*?])?(\s*)(\w*)", bygroups(Keyword, Other, Whitespace, Name.Variable)),
            (r"(\boutput)([.*?])?(\s*)(\w*)", bygroups(Keyword, Other, Whitespace, Name.Variable)),
            (r"(\baction)(\s*)(\w*)", bygroups(Keyword, Whitespace, Name.Variable)),
            (r"(\bstate)(\s*)(\w*)", bygroups(Keyword, Whitespace, Name.Variable)),
            (r"(\w*)(\s*)(=)(\s*)(new)", bygroups(Name.Variable, Whitespace, Operator, Whitespace, Keyword)),
            # keywords
            (words(keywords, prefix=r"\b", suffix=r"\b"), Keyword),
            # builtins
            (words(("startup", "shutdown"), prefix=r"\b", suffix=r"\b"), Name.Builtin),
            (words(("time",), prefix=r"\b", suffix=r"\b"), Keyword.Type),
            # time value with unit
            (
                r"(\d+)(\s*)(" + "|".join(time_units) + r")",
                bygroups(Number.Integer, Whitespace, Name.Builtin),
            ),
            # Operators
            (r"->", Operator),
            (r"~>", Operator),
            # Everything else
            (r".", Other),
        ],
    }
