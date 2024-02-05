from fractions import Fraction
from dataclasses import dataclass
from typing import Optional, NewType, Union, List
#######################################
# CONSTANTS
#######################################

DIGITS = '0123456789'
keywords = "be eternal belief else chant pledge oath preach invoke deliver persist retreat trial mercy condemn unite slice".split(
)
booleans = "myth truth".split()
type_keywords = "int float char bool str".split()
whitespace = [" ", "\n", "\f", "\t", "\r", "\v"]
symbols = ", ( ) { } [ ] : ' \" .".split()

list_utils = "cons head tail append insert remove length".split()
array_utils = "head append remove length".split()
tuple_utils = "length".split()

endofstmt=";".split()
symbolic_operators = "+ - * / < > <= >= == != && || ! ? =".split()

#######################################
# ERRORS
#######################################


class Error:
    def __init__(self, pos_start, pos_end, error_name, details):
        self.pos_start = pos_start
        self.pos_end = pos_end
        self.error_name = error_name
        self.details = details
        # Automatically print the error details upon instantiation
        print(self.as_string())

    def as_string(self):
        result = f'{self.error_name}: {self.details}\n'
        result += f'File {self.pos_start.fn}, line {self.pos_start.ln + 1}'
        return result

class IllegalCharError(Error):
    def __init__(self, pos_start, pos_end, details):
        super().__init__(pos_start, pos_end, 'Illegal Character', details)
        # No need to add a print statement here since it's already in the parent class



#######################################
# POSITION
#######################################


class Position:

  def __init__(self, idx, ln, col, fn, ftxt):
    self.idx = idx
    self.ln = ln
    self.col = col
    self.fn = fn  #filename
    self.ftxt = ftxt  #filetext

  def advance(self, current_char):
    self.idx += 1
    self.col += 1

    if current_char == '\n':
      self.ln += 1
      self.col = 0

    return self

  def copy(self):
    return Position(self.idx, self.ln, self.col, self.fn, self.ftxt)


#######################################
# TOKENS
#######################################
@dataclass
class Int:
  value: int


@dataclass
class Float:
  value: float


@dataclass
class Bool:
  value: bool

@dataclass
class EndOfStatement:
  value: str

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
class TypeKeyword:
    value: str

@dataclass
class UtilityFunction:
    value: str


@dataclass
class CharToken:
  value: str


Token = Union[Int, Float, Bool, Keyword, Identifier, Operator, Symbols,
              StringToken, ListToken, Whitespace, CharToken]


class Token:

  def __init__(self, type_, value=None):
    self.type = type_
    self.value = value

  def __repr__(self):
    if self.value: return f'{self.type}:{self.value}'
    return f'{self.type}'


#######################################
# LEXER
#######################################


class Lexer:

  def __init__(self, fn, text):
    self.fn = fn
    self.text = text
    self.pos = Position(-1, 0, -1, fn, text)
    self.current_char = None
    self.advance()
    self.single_char_tokens, self.double_char_tokens = self.generate_token_mappings(
    )

  def advance(self):
    self.pos.advance(self.current_char)
    self.current_char = self.text[self.pos.idx] if self.pos.idx < len(
        self.text) else None

  def peek(self):
    """Peek at the next character without consuming it."""
    peek_pos = self.pos.idx + 1
    if peek_pos < len(self.text):
      return self.text[peek_pos]
    else:
      return ''  # Return an empty string instead of None

  def generate_token_mappings(self):
    single_char_tokens = {}
    double_char_tokens = {}

    # Populate the mappings for symbolic operators
    for op in symbolic_operators:
      if len(op) == 1:
        single_char_tokens[op] = Operator(op)
      elif len(op) == 2:
        double_char_tokens[op] = Operator(op)

    # Adding symbols to single_char_tokens as needed
    for sym in symbols:
      if len(sym) == 1:
        single_char_tokens[sym] = Symbols(sym)

    return single_char_tokens, double_char_tokens

  def make_tokens(self):
    tokens = []
    while self.current_char is not None:
      if self.current_char in whitespace:
        self.advance()
      elif self.current_char in DIGITS:
        tokens.append(self.make_number())
      elif self.current_char == ';':
        tokens.append(EndOfStatement(';'))
        self.advance()
      elif self.current_char == '/' and self.peek(
      ) == '/':  # Detecting start of a comment
        self.skip_comment()
      elif self.current_char == '"':
        tokens.append(self.make_string())  # Handle string literals
      elif self.current_char + self.peek() in self.double_char_tokens:
        double_char = self.current_char + self.peek()
        tokens.append(self.double_char_tokens[double_char])
        self.advance()  # Advance past the first character
        self.advance()  # Advance past the second character
      elif self.current_char in self.single_char_tokens:
        tokens.append(self.single_char_tokens[self.current_char])
        self.advance()
      elif self.current_char == "'":
        tokens.append(self.make_char())  # Handle character literals
      # elif self.current_char == '\n': # Handle newlines, not necessary since focus is semicolons
      #   tokens.append(Whitespace('\n'))
      #   self.advance()
      else:
        # Handle identifiers or keywords
        if self.current_char.isalpha():
          tokens.append(self.make_identifier())
        else:
          pos_start = self.pos.copy()
          char = self.current_char
          self.advance()
          error = IllegalCharError(pos_start, self.pos, "Unable to identify character: " + char)
          return [], error  # Return an empty list and the error object
    return tokens, None

  def skip_comment(self):
    while self.current_char is not None and self.current_char != '\n':
      self.advance()
    self.advance(
    )  # Optional: Skip the newline character as well, if you want to ignore it

  def make_string(self):
      string_val = ''
      self.advance()  # Skip the opening quote

      while self.current_char is not None and self.current_char != '"':
          if self.current_char == '\\':
              self.advance()  # Handle escape sequences if necessary
              if self.current_char == 'n':
                  string_val += '\n'
              elif self.current_char == '"':
                  string_val += '"'
              # Add other escape sequences as needed
          else:
              string_val += self.current_char
          self.advance()

      if self.current_char != '"':
          # Handle unterminated string error
          return None, IllegalCharError(self.pos.copy(), self.pos, "Expected '\"' at the end of string")
      
      self.advance()  # Consume the closing quote
      return StringToken(string_val), None
    
  def extract_identifier(self):
    identifier_str = ''
    while self.current_char is not None and (self.current_char.isalnum() or self.current_char == '_'):
      identifier_str += self.current_char
      self.advance()
    return identifier_str
  
  def make_char(self):
    self.advance()  # Consume the opening quote
    char_val = self.current_char  # Assign the character value
    pos_start = self.pos.copy()
    self.advance()  # Move to the next character

    if self.current_char != "'":
      return None, IllegalCharError(
          pos_start, self.pos,
          "Character literals must be single characters enclosed in single quotes"
      )
    self.advance()  # Consume the closing quote
    return CharToken(char_val), None

  def make_identifier(self):
    identifier_str = ''

    while self.current_char is not None and (self.current_char.isalnum()
                                             or self.current_char == '_'):
      identifier_str += self.current_char
      self.advance()
    # Check if the identifier is a keyword or a regular identifier
    if identifier_str in keywords:
      return Keyword(identifier_str)
    elif identifier_str in booleans:
      return Bool(identifier_str.lower() == 'truth')
    elif identifier_str in type_keywords:
      return TypeKeyword(identifier_str)
  # Check if the identifier is a utility function (list, array, tuple utilities combined)
    elif identifier_str in list_utils + array_utils + tuple_utils:
        return UtilityFunction(identifier_str)
    else:
      return Identifier(identifier_str)

  def make_number(self):
      num_str = ''
      dot_count = 0
      pos_start = self.pos.copy()  # Remember the start of the number for error reporting

      while self.current_char is not None and (self.current_char.isdigit() or self.current_char == '.'):
          if self.current_char == '.':
              dot_count += 1
              num_str += '.'
          else:
              num_str += self.current_char
          self.advance()
      if dot_count > 1:  # After exiting the loop, check if we encountered more than one dot
          return [], IllegalCharError(pos_start, self.pos, f"Multiple decimal points found in number '{num_str}'")
      elif dot_count == 0:
          return Int(int(num_str))
      else:
          return Float(float(num_str))



########## Lists, tuples and arrays #############

###################################################
# add for identifying string literals, list literals, tuple literals, and array literals.
#######################################
# RUN
#######################################


def run(fn, text):
  lexer = Lexer(fn, text)
  tokens, error = lexer.make_tokens()

  return tokens, error
