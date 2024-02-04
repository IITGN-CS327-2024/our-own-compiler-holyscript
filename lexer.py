from fractions import Fraction
from dataclasses import dataclass
from typing import Optional, NewType, Union
from utils.errors import EndOfStream, EndOfTokens, TokenError, StringError, ListOpError
from utils.datatypes import Num, Bool, Keyword, Symbols, ListUtils, Identifier, StringToken, ListToken, Operator, Whitespace, NumLiteral, BinOp, UnOp, Variable, Let, Assign, If, BoolLiteral, UnOp, ASTSequence, AST, Buffer, ForLoop, Range, Declare, While, DoWhile, Print, funct_call, funct_def, funct_ret, StringLiteral, StringSlice, ListObject, ListCons, ListOp, ListIndex
from core import RuntimeEnvironment


keywords = "summon doom eternal belief else chant pledge oath preach invoke deliver persist retreat trial mercy condemn unite slice".split()
type_keywords = "int float double char bool str".split()

symbolic_operators = "+ - * / < > <= >= == != && || ! ?".split()  # Assuming &&, ||, ! as logical and, or, not
# word_operators = "and or not".split()  # Commented out because we've not mentioned this in our documentation yet, will likely not implement
whitespace = [" ", "\n", "\f", "\t", "\r", "\v"]
symbols = "; , ( ) { } [ ] ' \" .".split()

list_utils = "cons head tail append insert remove length".split()
array_utils = "head append remove length".split()
tuple_utils = "length".split()  # Assuming you might want to access parts but not modify

r = RuntimeEnvironment()

# Token Definitions
Token = Int | Float | Bool | Keyword | Identifier | Operator | Symbols | StringToken | ListToken | Whitespace

@dataclass
class Int:
    value: Int

@dataclass
class Float:
    value: Float
  
@dataclass
class Bool:
    value: bool

@dataclass
class Keyword:
    value: str

@dataclass
class Identifier:
    name: str

@dataclass
class Operator:
    value: str

@dataclass
class Symbols:
    value: str

@dataclass
class StringToken:
    value: str

@dataclass
class ListToken:
    elements: list

@dataclass
class Whitespace:
    value: str

@dataclass
class Stream:
    source: str
    pos: int

    def from_string(string: str, position: int = 0):
        """
        Creates a stream from a string. Position reset to 0.
        """
        return Stream(string, position)

    def next_char(self):
        """
        Returns the next character in the stream.
        """
        if self.pos >= len(self.source):
            raise EndOfStream()
        self.pos += 1
        return self.source[self.pos - 1]

    def unget(self):
        """
        Moves the stream back one character.
        """
        assert self.pos > 0
        self.pos -= 1

def word_to_token(word):
    if word in keywords:
        return Keyword(word)
    if word == "True":
        return Bool(True)
    if word == "False":
        return Bool(False)
    if word in symbolic_operators:
        return Operator(word)
    if word in symbols:
        return Symbols(word)
    if word in whitespace:
        return Whitespace(word)
    return Identifier(word)


@dataclass
class Lexer:
    stream: Stream
    save: Token = None

    def from_stream(s):
        return Lexer(s)

    def next_token(self) -> Token:
        try:
            match self.stream.next_char():
                case c if c.isdigit():
                    n = int(c)
                    # Handle different bases.
                    while True:
                        try:
                            c = self.stream.next_char()
                            if c.isdigit():
                                n = n * 10 + int(c)
                            else:
                                self.stream.unget()
                                return Num(n)
                        except EndOfStream:
                            return Num(n)

                case c if c.isalpha():
                    s = c
                    while True:
                        try:
                            c = self.stream.next_char()
                            if c.isalnum():
                                s += c
                            else:
                                self.stream.unget()
                                if s in keywords:
                                    return Keyword(s)
                                return Identifier(s)
                        except EndOfStream:
                            if s in keywords:
                                return Keyword(s)
                            return Identifier(s)

                case c if c in '+-*/<>=!':
                    return Operator(c)

                case c if c in ";,(){}[]'\".":
                    return Symbols(c)

                case c if c in ' \n':
                    return Whitespace(c)

        except EndOfStream:
            raise EndOfTokens()

    def peek_token(self):
        """
        Peeks at the next token, but doesn't advance the stream.
        """
        if self.save is not None:
            return self.save
        self.save = self.next_token()
        return self.save

    def match(self, expected):
        """
        Matches the next token to the expected token.
        """
        if self.peek_token() == expected:
            return self.advance()
        else:
            raise TokenError(f"Expected {expected}, got {self.peek_token()}")

    def advance(self):
        """
        Advances the stream by one token.
        """
        assert self.save is not None
        self.save = None

    def __iter__(self):
        return self

    def __next__(self):
        try:
            self.curr_token = self.next_token()
            return self.curr_token
        except EndOfTokens:
            raise StopIteration

