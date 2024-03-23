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

    def __repr__(self):
        return f"IntLiteral({self.value})"

class FloatLiteral(ASTNode):
    def __init__(self, value: float):
        self.value = value

    def __repr__(self):
        return f"FloatLiteral({self.value})"

class BoolLiteral(ASTNode):
    def __init__(self, value: bool):
        self.value = value

    def __repr__(self):
        return f"BoolLiteral({self.value})"

class StringLiteral(ASTNode):
    def __init__(self, value: str):
        self.value = value

    def __repr__(self):
        return f"StringLiteral('{self.value}')"

class Identifier(ASTNode):
    def __init__(self, value: str):
        self.value = value

    def __repr__(self):
        return f"Identifier('{self.value}')"

class Operator(ASTNode):
    def __init__(self, value: str):
        self.value = value

    def __repr__(self):
        return f"Operator('{self.value}')"

class Symbol(ASTNode):
    def __init__(self, value: str):
        self.value = value

    def __repr__(self):
        return f"Symbol('{self.value}')"
    
class Keyword(ASTNode):
    def __init__(self, value: str):
        self.value = value

    def __repr__(self):
        return f"Keyword('{self.value}')"

class EndOfStatement(ASTNode):
    def __init__(self, value: str):
        self.value = value

    def __repr__(self):
        return f"EndOfStatement('{self.value}')"
# Collection literals
class ListLiteral(ASTNode):
    def __init__(self, elements: List[ASTNode]):
        self.elements = elements

    def __repr__(self):
        elements_str = ', '.join(repr(elem) for elem in self.elements)
        return f"ListLiteral([{elements_str}])"

class TupleLiteral(ASTNode):
    def __init__(self, elements: List[ASTNode]):
        self.elements = elements

    def __repr__(self):
        elements_str = ', '.join(repr(elem) for elem in self.elements)
        return f"TupleLiteral({elements_str})"

# Expressions
class FunctionCall(ASTNode):
    def __init__(self, name: str, arguments: List[ASTNode]):
        self.name = name
        self.arguments = arguments

    def __repr__(self):
        arguments_str = ', '.join(repr(arg) for arg in self.arguments)
        return f"FunctionCall('{self.name}', [{arguments_str}])"

class UnaryExpression(ASTNode):
    def __init__(self, operator: Operator, operand: ASTNode):
        self.operator = operator
        self.operand = operand

    def __repr__(self):
        return f"UnaryExpression({repr(self.operator)}, {repr(self.operand)})"

class BinaryExpression(ASTNode):
    def __init__(self, left: ASTNode, operator: Operator, right: ASTNode):
        self.left = left
        self.operator = operator
        self.right = right

    def __repr__(self):
        return f"BinaryExpression({repr(self.left)}, {repr(self.operator)}, {repr(self.right)})"


class ArrayIndexing(ASTNode):
    def __init__(self, array: ASTNode, index: ASTNode):
        self.array = array
        self.index = index

    def __repr__(self):
        return f"ArrayIndexing({repr(self.array)}, {repr(self.index)})"


# Statements
class CompoundStatement(ASTNode):
    def __init__(self, declarations: List[ASTNode], statements: List[ASTNode]):
        self.declarations = declarations
        self.statements = statements

    def __repr__(self):
        declarations_str = ', '.join(repr(decl) for decl in self.declarations)
        statements_str = ', '.join(repr(stmt) for stmt in self.statements)
        return f"CompoundStatement([{declarations_str}], [{statements_str}])"

class IfStatement(ASTNode):
    def __init__(self, condition: ASTNode, true_branch: ASTNode, false_branch: Union[ASTNode, None]):
        self.condition = condition
        self.true_branch = true_branch
        self.false_branch = false_branch

    def __repr__(self):
        false_branch_str = repr(self.false_branch) if self.false_branch else "None"
        return f"IfStatement({repr(self.condition)}, {repr(self.true_branch)}, {false_branch_str})"


class WhileLoop(ASTNode):
    def __init__(self, condition: ASTNode, body: ASTNode):
        self.condition = condition
        self.body = body

    def __repr__(self):
        return f"WhileLoop({repr(self.condition)}, {repr(self.body)})"

class FunctionDefinition(ASTNode):
    def __init__(self, return_type: ASTNode, name: str, parameters: List[tuple[ASTNode, str]], body: ASTNode):
        self.return_type = return_type
        self.name = name
        self.parameters = parameters
        self.body = body

    def __repr__(self):
        parameters_str = ', '.join(f"{repr(param_type)} {param_name}" for param_type, param_name in self.parameters)
        return f"FunctionDefinition({repr(self.return_type)}, '{self.name}', [{parameters_str}], {repr(self.body)})"

class ArrayLiteral(ASTNode):
    def __init__(self, elements: List[ASTNode]):
        self.elements = elements

    def __repr__(self):
        elements_str = ', '.join(repr(elem) for elem in self.elements)
        return f"ArrayLiteral([{elements_str}])"


class Program(ASTNode):
    def __init__(self, statements: List[ASTNode]):
        self.statements = statements

    def __repr__(self):
        statements_str = '\n'.join(repr(stmt) for stmt in self.statements)
        return f"Program:\n{statements_str}"

class SelectionStatement(ASTNode):
    def __init__(self, condition: ASTNode, true_branch: ASTNode, false_branch: Union[None, ASTNode]):
        self.condition = condition
        self.true_branch = true_branch
        self.false_branch = false_branch

    def __repr__(self):
        false_branch_str = repr(self.false_branch) if self.false_branch else "None"
        return f"SelectionStatement({repr(self.condition)}, {repr(self.true_branch)}, {false_branch_str})"


class IterationStatement(ASTNode):
    def __init__(self, condition: ASTNode, body: ASTNode, declaration: Union[None, ASTNode] = None):
        self.condition = condition
        self.body = body
        self.declaration = declaration

    def __repr__(self):
        declaration_str = repr(self.declaration) if self.declaration else "None"
        return f"IterationStatement({repr(self.condition)}, {repr(self.body)}, {declaration_str})"


class ListComprehension(ASTNode):
    def __init__(self, declaration: ASTNode, condition: Union[ASTNode, None], body: ASTNode):
        self.declaration = declaration
        self.condition = condition
        self.body = body

    def __repr__(self):
        condition_str = repr(self.condition) if self.condition else "None"
        return f"ListComprehension({repr(self.declaration)}, {condition_str}, {repr(self.body)})"

class JumpStatement(ASTNode):
    def __init__(self, keyword: str, expression: Union[None, ASTNode] = None):
        self.keyword = keyword
        self.expression = expression

    def __repr__(self):
        expression_str = repr(self.expression) if self.expression else "None"
        return f"JumpStatement('{self.keyword}', {expression_str})"


class PreachStatement(ASTNode):
    def __init__(self, expression: ASTNode):
        self.expression = expression

    def __repr__(self):
        return f"PreachStatement({repr(self.expression)})"

# Declarations
class Declaration(ASTNode):
    def __init__(self, declaration_specifier: Union[None, ASTNode], expression: ASTNode):
        self.declaration_specifier = declaration_specifier
        self.expression = expression

    def __repr__(self):
        specifier_str = repr(self.declaration_specifier) if self.declaration_specifier else "None"
        return f"Declaration({specifier_str}, {repr(self.expression)})"

class DeclarationSpecifier(ASTNode):
    def __init__(self, eternal: Union[None, str], type_specifier: ASTNode):
        self.eternal = eternal
        self.type_specifier = type_specifier

    def __repr__(self):
        eternal_str = f"'{self.eternal}'" if self.eternal else "None"
        return f"DeclarationSpecifier({eternal_str}, {repr(self.type_specifier)})"


class TypeSpecifier(ASTNode):
    def __init__(self, type_keyword: str):
        self.type_keyword = type_keyword

    def __repr__(self):
        return f"TypeSpecifier('{self.type_keyword}')"

class TupleDeclaration(ASTNode):
    def __init__(self, identifier: str, assignment_expression: ASTNode, value_list: List[ASTNode]):
        self.identifier = identifier
        self.assignment_expression = assignment_expression
        self.value_list = value_list

    def __repr__(self):
        value_list_str = ', '.join(repr(value) for value in self.value_list)
        return f"TupleDeclaration('{self.identifier}', {repr(self.assignment_expression)}, [{value_list_str}])"

class ListDeclaration(ASTNode):
    def __init__(self, identifier: str, value_list: List[ASTNode]):
        self.identifier = identifier
        self.value_list = value_list

    def __repr__(self):
        value_list_str = ', '.join(repr(value) for value in self.value_list)
        return f"ListDeclaration('{self.identifier}', [{value_list_str}])"


class ArrayDeclaration(ASTNode):
    def __init__(self, type_specifier: ASTNode, identifier: str, expressions: List[ASTNode]):
        self.type_specifier = type_specifier
        self.identifier = identifier
        self.expressions = expressions

    def __repr__(self):
        expressions_str = ', '.join(repr(expr) for expr in self.expressions)
        return f"ArrayDeclaration({repr(self.type_specifier)}, '{self.identifier}', [{expressions_str}])"

# Utility functions
class BuiltinFunction(ASTNode):
    def __init__(self, name: str, arguments: List[ASTNode]):
        self.name = name
        self.arguments = arguments

    def __repr__(self):
        arguments_str = ', '.join(repr(arg) for arg in self.arguments)
        return f"BuiltinFunction('{self.name}', [{arguments_str}])"
