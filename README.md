This python package provides [pygments](https://pygments.org/) lexers for Lingua Franca and its various target dialects.

## Overview

The Lingua Franca lexer implemented in this package is relatively simple.
It provides rules for all keywords, the built-in type `time`, simple comments, time literals, connection operators and a few specialized rules for all named  reactor elements (state, ports, actions, etc.).
Everything that is enclosed in `{=...=}` and everything that is not matched by this LF lexer, is forwarded to the lexer of the target language.
This ensures that for instance target types are highlighted properly, irregardless of whether they are used within target code blocks or not.

The following languages and aliases are provided by this package:

- lf-c
- lf-cpp
- lf-python, lf-py
- lf-rust, lf-rs
- lf-typescript, lf-ts

## Installation

As with any Python package, I recommend to use a virtual environment to install this package and all its dependencies in.
There are several tool for managing virtual environments available. For instance you could do:
```
virtualenv ~/virtualenvs/lf-lexer -p python3
source ~/virtualenvs/lf-lexer/bin/activate
```
However, you can also skip this step if you rather have the package installed in your user environment.

To install the package, clone the repository and then run the following command from within the repository root:
```
pip install .
```

## Usage

### Command Line

Pygements provides a CLI tool called `pygmentize`. For example, you can use it to produce an image containing highlighted LF code like so:
```
pygmentize path/to/Example.lf -o out.png
```
Note that pygments automatically selects the right language. For this it processes both the file extension and the target declaration in it.
Therefore, auto detection should work fine as long as your file uses the `.lf` suffix and contains a valid target declaration. In all other cases, it is better to specify the language using the `-l` flag. For instance to use the Python target of LF, use `-l lf-py`.

### LaTeX

Most prominently, pygments is used by the "minted" LaTeX package to create beautiful code listings with proper code highlighting.
Using this is as simple as adding `\usepackage{minted}` and then adding `minted` blocks containing the code to be highlighted.
There is an example document at `example/example.tex`.
The only caveat is, that one needs to add the `-shell-escape` option when running latex.
The example document, can be build like this:
```
latexmk -pdf -shell-escape example/example.tex
```
