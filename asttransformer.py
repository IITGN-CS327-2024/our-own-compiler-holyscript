import sys
import os
import lexer
from lark import Lark, Transformer, Tree, Token
from typing import List
from dataclasses import dataclass
from lark import Lark, ast_utils, Transformer, v_args
from lark.tree import Meta
import astclasses


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


from astclasses import *

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
        identifier = children[0]  # The identifier node
        # Skip the first child assuming it is 'LeftParen()'
        values = []
        # Loop over all children except the first (LeftParen) and last (RightParen)
        for child in children[2:-1]:  # Adjust indices appropriately
            if isinstance(child, ASTNode):
                values.append(child)
            elif isinstance(child, list):  # Handle cases where values are within a nested list
                for item in child:
                    if isinstance(item, ASTNode):
                        values.append(item)

        return TupleDeclaration(identifier, values)





    
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
    
    def member_access_expression(self, args):
        def ensure_ast_node(node):
            if isinstance(node, list) and len(node) == 1:
                return node[0]  # Assuming the list contains a single ASTNode
            elif isinstance(node, list) and len(node) > 1:
                # If there are multiple items, this might require more sophisticated handling.
                # For example, you might need to merge or select an appropriate node.
                # This placeholder raises an exception to indicate an unresolved case.
                raise Exception("Complex list encountered in member_access_expression: {}".format(node))
            return node

        if len(args) == 1:
            # Single primary expression with no member access
            return ensure_ast_node(args[0])
        
        elif len(args) == 3 and args[1].type == 'DOT':
            # Dot operation, could be list_op, tuple_op, or array_op
            object_expr = ensure_ast_node(args[0])
            operation = ensure_ast_node(args[2])  # Transform if necessary
            return MemberAccessExpression(object_expr, operation=operation)
        
        elif len(args) == 4 and args[1].type == 'LBRACKET':
            # Indexing operation
            object_expr = ensure_ast_node(args[0])
            index = ensure_ast_node(args[2])  # args[2] should be an expression representing the index
            return MemberAccessExpression(object_expr, index=index)

        else:
            raise Exception("Unhandled syntax in member_access_expression")





    
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

   
    # def oath_pledge(self, children):
    #     # Assuming the structure received here is like:
    #     # [body_statements, 'oath', condition_expression]
    #     # Find 'oath' index to split body and condition
    #     oath_index = next(i for i, child in enumerate(children) if isinstance(child, Token) and child.value == 'oath')
    #     body = CompoundStatement(children[:oath_index])
    #     condition = children[oath_index + 1]

    #     # Create and return a DoWhileLoop node
    #     return DoWhileLoop(body, condition)



    def if_statement(self, children):
        condition = children[1]
        then_block = [children[3]]  # Wrap in a list to match the desired structure
        else_block = [children[5]] if len(children) > 5 else []
        return IfStatement(condition, then_block, else_block)
    
    def iteration_statement(self, args):
        keyword = args[0].value

        if keyword == "chant":
            loop_components = []
            for part in args[1:]:
                if isinstance(part, Tree):
                    loop_components.append(self.transform(part))
                else:
                    loop_components.append(part)
            if len(loop_components) < 7:
                raise ValueError("Incomplete loop structure")
            declaration = loop_components[0] 
            condition = loop_components[2] 
            increment = loop_components[4]  
            body = loop_components[6]     
            return ForLoop(declaration, condition, increment, body)
        
        elif keyword == "oath":
            if len(args) < 4:
                raise ValueError("Incomplete 'oath' loop structure")
            body = self.transform(args[1]) if isinstance(args[1], Tree) else args[1]
            condition = self.transform(args[3]) if isinstance(args[3], Tree) else args[3]
            return DoWhileLoop(body, condition)

        elif keyword == "pledge":
            if len(args) < 5:
                raise ValueError("Incomplete 'pledge' loop structure")
            condition = self.transform(args[2]) if isinstance(args[2], Tree) else args[2]
            body = self.transform(args[4]) if isinstance(args[4], Tree) else args[4]
            return WhileLoop(condition, body)

        else:
            raise ValueError(f"Unsupported iteration statement keyword: {keyword}")



            
    def additive_expression(self, children):
        if len(children) == 1:
            # Just a single term, no actual addition/subtraction, pass it through
            return children[0]
        # Assuming children are [left, operator, right]
        left = children[0]
        operator = children[1].value  # Assuming this is a Token and has a 'value'
        right = children[2]
        return BinaryExpression(left, operator, right)

    def array_declaration(self, children):
        type_specifier = children[0]  # Assuming the type_specifier is the first child
        identifier = children[1]      # Assuming the identifier is the second child
        expressions = children[3:-1] if len(children) > 4 else []  # Check if there are more than four children to include expressions

        return ArrayDeclaration(type_specifier, identifier, expressions)















    def jump_statement(self, children):
    # Ensure that we are accessing the data correctly
        # children might contain directly the keyword Token and optional expression
        if isinstance(children[0], Token):
            keyword = children[0].value
            expression = None
            if len(children) > 1:
                expression = children[1]  # Assume the expression follows the keyword
        else:
            # If it's not as expected, raise an error or handle it appropriately
            raise ValueError("Unexpected structure in jump_statement: {}".format(children))

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
            operator_symbol = None
            if isinstance(operator, GreaterThan):
                operator_symbol = '>'
            # Add more cases for other operator types as needed
            if operator_symbol is not None:
                return BinaryExpression(left_node, operator_symbol, right_node)
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
                elif value.type == 'int':
                    return IntLiteral(int(value.value))
                elif value.type == 'float':
                    return FloatLiteral(float(value.value))
                elif value.type == 'str':
                    return StringLiteral(value.value[1:-1])
                elif value.type == 'bool':
                    return BoolLiteral(value.value)
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
        keyword, return_type, name, _, params, _, body = children

        # Debugging output for understanding the parameter structure
        # print("Params:", [(type(p), p) for p in params])

        # Convert params to the correct format: a list of (type_keyword, identifier value)
        parameters = []
        for param in params:
            if isinstance(param, tuple) and len(param) == 2:
                type_keyword, identifier_token = param
                if isinstance(identifier_token, Token) and identifier_token.type == 'CNAME':
                    parameters.append((type_keyword, identifier_token.value))
                else:
                    raise ValueError("Invalid identifier token in parameters")
            else:
                raise ValueError("Parameter list format error: Each parameter must be a tuple (type_keyword, identifier_token)")

        # Create FunctionDefinition
        return FunctionDefinition(return_type, name.value, parameters, body)




    
    def SIGNED_INT(self, token):
        return IntegerLiteral(int(token))

    def CNAME(self, token):
        return Identifier(token)

    def parameter_list(self, children):
        # Ensure that the number of children is even to form pairs
        if len(children) % 2 != 0:
            raise ValueError("Parameter list parsing error: Expected even number of elements for type-specifier and identifier pairs")

        parameters = []
        # Step through the children two at a time
        for i in range(0, len(children), 2):
            type_specifier = children[i]
            identifier = children[i + 1]

            # Verify that we have the correct types
            if not isinstance(type_specifier, TypeSpecifier) or not isinstance(identifier, Identifier):
                raise ValueError("Parameter list parsing error: Expected TypeSpecifier and Identifier pairs")

            # Append the type specifier and the identifier value
            parameters.append((type_specifier.type_keyword, identifier.value))

        return parameters



    def postfix_expression(self, args):
    # This handles recursive postfix expressions and function calls.
        if len(args) == 1:
            # Directly return the single argument if it's the only one.
            return args[0]

        # Recursive case: check if we are dealing with operators or function calls.
        primary_expr = args[0]
        for i in range(1, len(args), 2):
            operator = args[i]
            if operator.type == 'INCREMENT':
                primary_expr = UnaryExpression(operator='++', operand=primary_expr)
            elif operator.type == 'DECREMENT':
                primary_expr = UnaryExpression(operator='--', operand=primary_expr)
            elif isinstance(operator, Token) and (operator.type == 'INCREMENT' or operator.type == 'DECREMENT'):
                # Handle the case where the operator is a Token instance
                primary_expr = UnaryExpression(operator=operator.value, operand=primary_expr)
            else:
                # If args[i] is a function call or another postfix expression
                continue  # Or handle according to your specific logic

        return primary_expr





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
    
    def array_declaration(self, children):
        # Extract the type specifier and identifier, which are expected to always be present
        type_specifier = children[0]  # This should be an instance of TypeSpecifier
        identifier = children[1]      # This should be an instance of Identifier

        # Extract expressions if present. They are beyond the 3rd element after type_specifier, identifier, and '['
        expressions = children[3:-1] if len(children) > 4 else []

        return ArrayDeclaration(type_specifier, identifier.value, expressions)


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
            elif item.type == 'STRING':
                return StringLiteral(item.value[1:-1])
            elif item.type == 'FLOAT':
                return FloatLiteral(float(item.value))
            elif item.type == 'BOOLEAN' :
                return BoolLiteral(bool(item.value))
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