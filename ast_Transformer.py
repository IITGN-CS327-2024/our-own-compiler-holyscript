import sys
import os
import lexer
from lark import Lark, Transformer, Tree, Token
from typing import List
from dataclasses import dataclass
from lark import Lark, ast_utils, Transformer, v_args
from lark.tree import Meta
import ast__Classes


# class _Ast: 
#     pass

# class _Statement(_Ast):
#     pass

# @dataclass
# class Value(_Ast):
#     value: object

# @dataclass
# class Name(_Ast):
#     name: str

# @dataclass
# class CodeBlock(_Ast):
#     statements: List[_Statement]

# @dataclass
# class If(_Statement):
#     cond: Value
#     then: CodeBlock

# @dataclass
# class SetVar(_Statement):
#     name: str
#     value: Value

# @dataclass
# class Print(_Statement):
#     value: Value

# @dataclass
# class Declaration(_Statement):
#     specifier: str
#     expression: Value

# @dataclass
# class Preach(_Statement):
#     expression: Value

# @dataclass
# class Belief(_Statement):
#     expression: Value
#     then_branch: CodeBlock
#     else_branch: CodeBlock

# @dataclass
# class Pledge(_Statement):
#     expression: Value
#     statement: _Statement

# @dataclass
# class Oath(_Statement):
#     statement: _Statement
#     expression: Value

# @dataclass
# class Chant(_Statement):
#     specifier: str
#     expression1: Value
#     expression2: Value
#     expression3: Value
#     statement: _Statement

# @dataclass
# class Persist(_Statement):
#     expression: Value

# @dataclass
# class Retreat(_Statement):
#     pass

# @dataclass
# class Deliver(_Statement):
#     expression: Value

# @dataclass
# class FunctionDef(_Statement):
#     return_type: str
#     name: str
#     parameters: List[str]
#     body: CodeBlock

# @dataclass
# class FunctionCall(_Ast):
#     name: str
#     arguments: List[Value]


from ast__Classes import *

def remove_none(lst):
    flat_list = []
    for sublist in lst:
        if isinstance(sublist, list):
            flat_list.extend(remove_none(sublist))
        elif sublist is not None:
            flat_list.append(sublist)
    return flat_list

class ToAst(Transformer):

    # def start(self, children):
    #     statements = []
    #     for child in children:
    #         if isinstance(child, Tree):
    #             statements.append(self.transform(child))
    #         else:
    #             statements.append(child)
    #     return Program(statements)

    def start(self, children):
        return Program(children)
    
    def statement(self, children):
        return children[0]



    # def compound_statement(self, children):
    #     declarations = [decl for decl in children[:-1] if isinstance(decl, Declaration)]
    #     statements = [stmt for stmt in children[-1].children if stmt is not None]
    #     return CompoundStatement(declarations, statements)
    
    
    def compound_statement(self, children):
        declarations = [child for child in children if isinstance(child, Declaration)]
        statements = [child for child in children if not isinstance(child, Declaration)]
        return CompoundStatement(declarations, statements)

    def tuple_declaration(self, children):
        identifier = Identifier(children[1].value)
        assignment_expression = children[2]
        value_list = children[4]
        return TupleDeclaration(identifier, assignment_expression, value_list)
    
    def literal(self, children):
        return Literal(children[0])

    def list_declaration(self, children):
        identifier = Identifier(children[1].value)
        value_list = children[3]
        return ListDeclaration(identifier, value_list)

    # def value_list(self, children):
    #     values = []
    #     for child in children:
    #          if isinstance(child, Lark.Tree):
    #             values.append(child.children[0])
    #     return values
        #     pass

    def value_list(self, children):
        return [child for child in children if child is not None]

    def declaration(self, children):
        if isinstance(children[0], ArrayDeclaration):
            array_declaration = children[0]
            return array_declaration
        else:
            # Otherwise, we have a variable declaration with an optional specifier
            declaration_specifier = children[0] if isinstance(children[0], DeclarationSpecifier) else None
            assignment_expression = children[1] if declaration_specifier else children[0]
            return VariableDeclaration(declaration_specifier, assignment_expression)


    
    # def declaration(self, children):
    #     children = remove_none(children)
    #     return Declaration(children[0], children[1], children[2])


    # def declaration_specifier(self, children):
    #     if len(children) == 1:
    #         eternal = None
    #         type_specifier = children[0]
    #     else:
    #         eternal = children[0].value
    #         type_specifier = children[1]
    #     return DeclarationSpecifier(eternal, type_specifier)

    def declaration_specifier(self, children):
        eternal = children[0].value if len(children) == 2 else None
        type_specifier = children[-1]
        return DeclarationSpecifier(eternal, type_specifier)
    
    def type_specifier(self, children):
        if children:
            type_keyword = children[0].value
            return TypeSpecifier(type_keyword)
        else:
            return None
    
    def array_access(self, items):
        # Assuming items = [array, index]
        array, index = items
        return ArrayAccess(array, index)
        
    def while_loop(self, children):
        condition = children[1]
        body = children[3]
        return WhileLoop(condition, body)
    
    def CHAR_SEQUENCE(self, token):
        # Remove the single quotes from the token value
        char_value = token[1:-1]
        return CharLiteral(char_value)
    
    def preach_statement(self, items):
        # Assuming items = ['preach', '(', expression, ')']
        _, _, expression, _ = items
        # Ensure expression is an ASTNode instance
        expression_node = expression[0] if isinstance(expression, list) else expression
        return PreachStatement(expression_node)
   
    # def preach_statement(self, children):
    #     if len(children) >= 2:
    #         expression = children[0]  # The expression is the second child
    #         return PreachStatement(expression)
    #     else:
    #         # Handle the case where the children list does not have an element at index 1
    #         # For example, you can raise an error or handle it in some other way
    #         raise ValueError("Invalid preach_statement: missing expression")

    def KEYWORD_BELIEF(self, token):
        return BeliefKeyword()

    def LPAREN(self, token):
        return LeftParen()
    
    def GT(self, token):
        return GreaterThan()

    def LBRACE(self, token):
        return LeftBrace()

    def RBRACE(self, token):
        return RightBrace()
    
    def selection_statement(self, children):
        # Assuming children = ['belief', '(', expression, ')', compound_statement, 'else', compound_statement]
        belief_keyword, _, condition, _, true_branch, *else_part = children
        false_branch = else_part[1] if len(else_part) == 2 else None
        return IfStatement(condition, true_branch, false_branch)

    # Add more methods for other constructs...


    # Add more methods for other constructs...


    # def selection_statement(self, children):
    #     condition = children[0]
    #     true_branch = children[1] if len(children) > 1 else None
    #     false_branch = children[2] if len(children) > 2 else None
    #     return SelectionStatement(condition, true_branch, false_branch)

   
    def do_while_loop(self, items):
        # Assuming items = [body, condition]
        body, condition = items
        return DoWhileLoop(body, condition)

    def if_statement(self, children):
        condition = children[1]
        then_block = [children[3]]  # Wrap in a list to match the desired structure
        else_block = [children[5]] if len(children) > 5 else []
        return IfStatement(condition, then_block, else_block)
    
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
        
    def additive_expression(self, children):
        if len(children) == 1:
            # Just a single term, no actual addition/subtraction, pass it through
            return children[0]
        # Assuming children are [left, operator, right]
        left = children[0]
        operator = children[1].value  # Assuming this is a Token and has a 'value'
        right = children[2]
        return BinaryExpression(left, operator, right)

    def array_declaration(self, args):
        # Assuming args = [TypeKeyword(value='array'), Operator(value='<'), type_specifier, Operator(value='>'), identifier, Operator(value='='), LBRACKET, expression, RBRACKET, EndOfStatement(value=';')]
        array_type = args[2]
        identifier = args[4]
        elements = args[7]
        return ArrayDeclaration(array_type, identifier, elements)

    def jump_statement(self, *args):
        keyword = args[0].value
        expression = args[1] if len(args) > 1 else None
        return JumpStatement(keyword, expression)

    def assignment_expression(self, items):
        if len(items) == 3:
            # Assuming items = [left, operator, right]
            left, operator, right = items
            # Ensure left and right are ASTNode instances
            if isinstance(left, list):
                left = left[0] if left else None
            if isinstance(right, list):
                right = right[0] if right else None
            return BinaryExpression(left, operator.value, right)
        else:
            # If it's not a binary expression, just return the single item
            return items[0] if items else None

    def relational_expression(self, items):
        if len(items) == 3:
            # Assuming items = [left, operator, right]
            left, operator, right = items
            left_node = self.convert_to_ast_node(left)
            right_node = self.convert_to_ast_node(right)
            # Use the type of the operator object to determine the operator symbol
            if isinstance(operator, GreaterThan):
                operator_symbol = '>'
            # Add more cases for other operator types as needed
            return BinaryExpression(left_node, operator_symbol, right_node)
        else:
            # If it's not a relational expression, just return the single item
            return self.convert_to_ast_node(items[0]) if items else None

    def utility_function(self, items):
        # Assuming items = ['length', '(', expression, ')']
        function_name, _, expression, _ = items
        return UtilityFunctionCall(function_name, expression)
    
    def expression(self, children):
        if len(children) == 1:
            return children[0]
        else:
            return BinaryExpression(children[0], children[1], children[2])

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

    # def function_definition(self, children):
        # return_type = children[0]
        # name = children[1].value
        # parameters = children[2]
        # body = children[3]
        # return FunctionDefinition(return_type, name, parameters, body)
    
    def function_definition(self, children):
        return_type, name, parameters, body = children
        return FunctionDefinition(return_type, name, parameters, body)
    
    def SIGNED_INT(self, token):
        return IntegerLiteral(int(token))

    def CNAME(self, token):
        return Identifier(token)

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
    
    def variable_declaration(self, children):
        # Assuming children structure: [TypeSpecifier, Identifier, '=', Expression]
        type_specifier, identifier, _, initial_value = children
        return VariableDeclaration(type_specifier, identifier, initial_value)

    # In ast_Transformer.py

    def binary_expression(self, items):
        if len(items) == 3:
            # Assuming items = [left, operator, right]
            left, operator, right = items
            # Convert left and right to ASTNode instances if they are not already
            left_node = self.convert_to_ast_node(left)
            right_node = self.convert_to_ast_node(right)
            return BinaryExpression(left_node, operator, right_node)
        else:
            # If it's not a binary expression, just return the single item
            return self.convert_to_ast_node(items[0]) if items else None


    def convert_to_ast_node(self, item):
        if isinstance(item, Tree):
            # If the item is a Tree, transform it into an AST node using the appropriate transformation method
            return self.transform(item)
        elif isinstance(item, list):
            # If the item is a list, check if it contains a single element and convert it
            # If it contains more than one element, convert each element and return the list
            if len(item) == 1:
                return self.convert_to_ast_node(item[0])
            else:
                return [self.convert_to_ast_node(sub_item) for sub_item in item]
        elif isinstance(item, Token):
            # Convert tokens to appropriate AST nodes based on their type
            if item.type == 'CNAME':
                return Identifier(item.value)
            elif item.type == 'SIGNED_INT':
                return IntegerLiteral(int(item.value))
            # Add more cases for other token types as needed
        return item

    
    def block(self, children):
        # Filter out any None children, which might be placeholders for optional grammar parts
        statements = [self.transform(child) for child in children if child is not None]
        return CompoundStatement(statements)

    # def binary_expression(self, children):
    #     left, operator_token, right = children
    #     operator = operator_token.value  # Assuming operator_token is a Token and has a 'value' attribute
    #     left_node = self.transform(left)
    #     right_node = self.transform(right)
    #     return BinaryExpression(left=left_node, operator=operator, right=right_node)
    
    def SINGLE_QUOTE_STR(self, token):
        # Remove the single quotes from the token value
        string_value = token[1:-1]
        return StringLiteral(string_value)
    
    def unary_expression(self, children):
        operator = children[0]  # Assuming the operator is a terminal node or already transformed
        operand = self.transform(children[1])
        
        return UnaryExpression(operator=operator, operand=operand)

    def builtin_function(self, *args):
        name = args[0].value
        arguments = args[1:]
        return BuiltinFunction(name, arguments)
    
    @staticmethod
    def token_to_value(token):
        if isinstance(token, Token):
            return token.value
        return token

    def __default__(self, data, children, meta):
        if children:
            if len(children) == 1:
                return children[0]
            return Tree(data, children)
        return data
