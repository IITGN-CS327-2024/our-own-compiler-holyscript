import sys
import os
import lexer
from lark import Lark, Transformer, Tree, Token
from typing import List
from dataclasses import dataclass
from lark import Lark, ast_utils, Transformer, v_args
from lark.tree import Meta
import ast__Classes


class _Ast: 
    pass

class _Statement(_Ast):
    pass

@dataclass
class Value(_Ast):
    value: object

@dataclass
class Name(_Ast):
    name: str

@dataclass
class CodeBlock(_Ast):
    statements: List[_Statement]

@dataclass
class If(_Statement):
    cond: Value
    then: CodeBlock

@dataclass
class SetVar(_Statement):
    name: str
    value: Value

@dataclass
class Print(_Statement):
    value: Value

@dataclass
class Declaration(_Statement):
    specifier: str
    expression: Value

@dataclass
class Preach(_Statement):
    expression: Value

@dataclass
class Belief(_Statement):
    expression: Value
    then_branch: CodeBlock
    else_branch: CodeBlock

@dataclass
class Pledge(_Statement):
    expression: Value
    statement: _Statement

@dataclass
class Oath(_Statement):
    statement: _Statement
    expression: Value

@dataclass
class Chant(_Statement):
    specifier: str
    expression1: Value
    expression2: Value
    expression3: Value
    statement: _Statement

@dataclass
class Persist(_Statement):
    expression: Value

@dataclass
class Retreat(_Statement):
    pass

@dataclass
class Deliver(_Statement):
    expression: Value

@dataclass
class FunctionDef(_Statement):
    return_type: str
    name: str
    parameters: List[str]
    body: CodeBlock

@dataclass
class FunctionCall(_Ast):
    name: str
    arguments: List[Value]


from ast__Classes import *

class ToAst(Transformer):
    def start(self, children):
        children = [child for child in children if child is not None]
        statements = [stmt for stmt in children[0].children if stmt is not None]
        return Program(statements)

    def compound_statement(self, children):
        declarations = [decl for decl in children[:-1] if isinstance(decl, Declaration)]
        statements = [stmt for stmt in children[-1].children if stmt is not None]
        return CompoundStatement(declarations, statements)

    def tuple_declaration(self, children):
        identifier = children[1].value
        assignment_expression = children[2]
        value_list = children[4]
        return TupleDeclaration(identifier, assignment_expression, value_list)

    def list_declaration(self, children):
        identifier = children[1].value
        value_list = children[3]
        return ListDeclaration(identifier, value_list)

    def value_list(self, children):
        values = []
        for child in children:
             if isinstance(child, Lark.Tree):
                values.append(child.children[0])
        return values
        #     pass

    def declaration(self, children):
        if len(children) == 2:
            declaration_specifier = None
            expression = children[1]
        else:
            declaration_specifier = children[0]
            expression = children[2]
        return Declaration(declaration_specifier, expression)

    def declaration_specifier(self, children):
        if len(children) == 1:
            eternal = None
            type_specifier = children[0]
        else:
            eternal = children[0].value
            type_specifier = children[1]
        return DeclarationSpecifier(eternal, type_specifier)


    def type_specifier(self, children):
        if children:
            type_keyword = children[0].value
            return TypeSpecifier(type_keyword)
        else:
            return None

        
    def preach_statement(self, *args):
        expression = args[0]
        return PreachStatement(expression)

    def selection_statement(self, children):
        condition = children[0]
        true_branch = children[1] if len(children) > 1 else None
        false_branch = children[2] if len(children) > 2 else None
        return SelectionStatement(condition, true_branch, false_branch)


    def iteration_statement(self, *args):
        if len(args) == 2:
            condition = args[0]
            body = args[1]
            return IterationStatement(condition, body)
        elif len(args) == 3:
            body = args[0]
            condition = args[1]
            return IterationStatement(condition, body)
        else:
            declaration = args[0]
            condition1 = args[1]
            condition2 = args[2]
            condition3 = args[3]
            body = args[4]
            return IterationStatement(condition1, body, declaration=declaration)
        
    def array_declaration(self, children):
        type_specifier = children[1]
        identifier = children[3].value
        expressions = children[5]
        return ArrayDeclaration(type_specifier, identifier, expressions)

    def jump_statement(self, *args):
        keyword = args[0].value
        expression = args[1] if len(args) > 1 else None
        return JumpStatement(keyword, expression)

    def assignment_expression(self, *args):
        if len(args) == 1:
            return args[0]
        else:
            left = args[0]
            operator = args[1]
            right = args[2]
            return BinaryExpression(left, operator, right)

    def expression(self, *args):
        return args[0]

    # ... (handle other expression types like logical, relational, etc.)

    def primary_expression(self, *args):
        if len(args) == 1:
            value = args[0]
            if isinstance(value, Token):
                if value.type == 'IDENTIFIER':
                    return Identifier(value.value)
                elif value.type == 'INTEGER':
                    return IntLiteral(int(value.value))
                elif value.type == 'FLOAT':
                    return FloatLiteral(float(value.value))
                elif value.type == 'STRING':
                    return StringLiteral(value.value[1:-1])
                elif value.type == 'BOOLEAN':
                    return BoolLiteral(value.value == 'true')
            else:
                return value
        else:
            # Handle other primary expression cases
            pass

    def function_definition(self, children):
        return_type = children[0]
        name = children[1].value
        parameters = children[2]
        body = children[3]
        return FunctionDefinition(return_type, name, parameters, body)
    
    def parameter_list(self, children):
        if len(children) == 0:
            return []
        else:
            parameters = []
            for i in range(0, len(children), 2):
                type_specifier = children[i]
                identifier = children[i + 1].value
                # We'll create a simple tuple instead of using `Parameter`
                parameters.append((type_specifier, identifier))
            return parameters

    def function_body(self, children):
        statements = []
        for stmt in children[1:-1]:
            if isinstance(stmt, (Declaration, IfStatement, IterationStatement, FunctionCall, PreachStatement, JumpStatement)):
                statements.append(stmt)
        return CompoundStatement([], statements)

    def function_call(self, children):
        name = children[0].value
        arguments = children[1]
        return FunctionCall(name, arguments)
    
    def array_declaration(self, *args):
        type_specifier = args[1]
        identifier = args[3].value
        expressions = args[5]
        return ArrayDeclaration(type_specifier, identifier, expressions)

    def list_comprehension(self, *args):
        declaration = args[0]
        condition = args[1] if len(args) > 1 else None
        body = args[2]
        return ListComprehension(declaration, condition, body)

    def array_indexing(self, *args):
        array = args[0]
        index = args[2]
        return ArrayIndexing(array, index)

    def builtin_function(self, *args):
        name = args[0].value
        arguments = args[1:]
        return BuiltinFunction(name, arguments)