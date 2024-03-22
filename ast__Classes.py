from typing import Union, List
import sys
from dataclasses import dataclass
from lark import Lark, ast_utils, Transformer, v_args
from lark.tree import Meta

class ASTNode:
    pass

# Literal nodes
class IntLiteral(ASTNode):
    def __init__(self, value: int):
        self.value = value

class FloatLiteral(ASTNode):
    def __init__(self, value: float):
        self.value = value

class BoolLiteral(ASTNode):
    def __init__(self, value: bool):
        self.value = value

class StringLiteral(ASTNode):
    def __init__(self, value: str):
        self.value = value

class Identifier(ASTNode):
    def __init__(self, value: str):
        self.value = value

class Operator(ASTNode):
    def __init__(self, value: str):
        self.value = value

class Symbol(ASTNode):
    def __init__(self, value: str):
        self.value = value

class Keyword(ASTNode):
    def __init__(self, value: str):
        self.value = value

class EndOfStatement(ASTNode):
    def __init__(self, value: str):
        self.value = value

# Collection literals
class ListLiteral(ASTNode):
    def __init__(self, elements: List[ASTNode]):
        self.elements = elements

class TupleLiteral(ASTNode):
    def __init__(self, elements: List[ASTNode]):
        self.elements = elements

# Expressions
class FunctionCall(ASTNode):
    def __init__(self, name: str, arguments: List[ASTNode]):
        self.name = name
        self.arguments = arguments

class UnaryExpression(ASTNode):
    def __init__(self, operator: Operator, operand: ASTNode):
        self.operator = operator
        self.operand = operand

class BinaryExpression(ASTNode):
    def __init__(self, left: ASTNode, operator: Operator, right: ASTNode):
        self.left = left
        self.operator = operator
        self.right = right

class ArrayIndexing(ASTNode):
    def __init__(self, array: ASTNode, index: ASTNode):
        self.array = array
        self.index = index

# Statements
class CompoundStatement(ASTNode):
    def __init__(self, declarations: List[ASTNode], statements: List[ASTNode]):
        self.declarations = declarations
        self.statements = statements

class IfStatement(ASTNode):
    def __init__(self, condition: ASTNode, true_branch: ASTNode, false_branch: Union[ASTNode, None]):
        self.condition = condition
        self.true_branch = true_branch
        self.false_branch = false_branch

class WhileLoop(ASTNode):
    def __init__(self, condition: ASTNode, body: ASTNode):
        self.condition = condition
        self.body = body

class FunctionDefinition(ASTNode):
    def __init__(self, return_type: ASTNode, name: str, parameters: List[tuple[ASTNode, str]], body: ASTNode):
        self.return_type = return_type
        self.name = name
        self.parameters = parameters
        self.body = body

class ArrayLiteral(ASTNode):
    def __init__(self, elements: List[ASTNode]):
        self.elements = elements

class Program(ASTNode):
    def __init__(self, statements: List[ASTNode]):
        self.statements = statements

class SelectionStatement(ASTNode):
    def __init__(self, condition: ASTNode, true_branch: ASTNode, false_branch: Union[None, ASTNode]):
        self.condition = condition
        self.true_branch = true_branch
        self.false_branch = false_branch

class IterationStatement(ASTNode):
    def __init__(self, condition: ASTNode, body: ASTNode, declaration: Union[None, ASTNode] = None):
        self.condition = condition
        self.body = body
        self.declaration = declaration

class ListComprehension(ASTNode):
    def __init__(self, declaration: ASTNode, condition: Union[ASTNode, None], body: ASTNode):
        self.declaration = declaration
        self.condition = condition
        self.body = body

class JumpStatement(ASTNode):
    def __init__(self, keyword: str, expression: Union[None, ASTNode] = None):
        self.keyword = keyword
        self.expression = expression

class PreachStatement(ASTNode):
    def __init__(self, expression: ASTNode):
        self.expression = expression

# Declarations
class Declaration(ASTNode):
    def __init__(self, declaration_specifier: Union[None, ASTNode], expression: ASTNode):
        self.declaration_specifier = declaration_specifier
        self.expression = expression

class DeclarationSpecifier(ASTNode):
    def __init__(self, eternal: Union[None, str], type_specifier: ASTNode):
        self.eternal = eternal
        self.type_specifier = type_specifier

class TypeSpecifier(ASTNode):
    def __init__(self, type_keyword: str):
        self.type_keyword = type_keyword

class TupleDeclaration(ASTNode):
    def __init__(self, identifier: str, assignment_expression: ASTNode, value_list: List[ASTNode]):
        self.identifier = identifier
        self.assignment_expression = assignment_expression
        self.value_list = value_list

class ListDeclaration(ASTNode):
    def __init__(self, identifier: str, value_list: List[ASTNode]):
        self.identifier = identifier
        self.value_list = value_list

class ArrayDeclaration(ASTNode):
    def __init__(self, type_specifier: ASTNode, identifier: str, expressions: List[ASTNode]):
        self.type_specifier = type_specifier
        self.identifier = identifier
        self.expressions = expressions

# Utility functions
class BuiltinFunction(ASTNode):
    def __init__(self, name: str, arguments: List[ASTNode]):
        self.name = name
        self.arguments = arguments