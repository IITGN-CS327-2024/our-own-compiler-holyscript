from fractions import Fraction
from dataclasses import dataclass
from typing import Optional, NewType
from utils.errors import EndOfStream, EndOfTokens, TokenError, StringError, ListOpError
from utils.datatypes import Num, Bool, Keyword, Symbols, ListUtils, Identifier, StringToken, ListToken, Operator, Whitespace, NumLiteral, BinOp, UnOp, Variable, Let, Assign, If, BoolLiteral, UnOp, ASTSequence, AST, Buffer, ForLoop, Range, Declare, While, DoWhile, Print, funct_call, funct_def, funct_ret, StringLiteral, StringSlice, ListObject, ListCons, ListOp, ListIndex
from core import RuntimeEnvironment


keywords = "summon doom eternal belief else chant pledge oath preach invoke deliver persist retreat trial mercy condemn unite slice".split()
type_keywords = "int float double char bool".split()

symbolic_operators = "+ - * / < > <= >= == != && || !".split()  # Assuming &&, ||, ! as logical and, or, not
# word_operators = "and or not".split()  # Commented out because we've not mentioned this in our documentation yet, will likely not implement
whitespace = [" ", "\n"]
symbols = "; , ( ) { } [ ] ' \" .".split()

list_utils = "cons head tail append insert remove length".split()
array_utils = "head append remove length".split()
tuple_utils = "length".split()  # Assuming you might want to access parts but not modify

r = RuntimeEnvironment()

# Token Definitions
Token = Num | Bool | Keyword | Identifier | Operator | Symbols | StringToken | ListToken | Whitespace

