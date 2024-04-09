from typing import Union, List
import sys
from dataclasses import dataclass
from lark import Lark, ast_utils, Transformer, v_args
from lark.tree import Meta

class ASTNodeMeta(type):
    def __new__(mcs, name, bases, dct):
        if name != 'ASTNode':
            def repr_func(self):
                attrs = ', '.join(f'{k}={repr(v)}' for k, v in vars(self).items() if not k.startswith('__'))
                return f"{name}({attrs})"
            dct['__repr__'] = repr_func
        return super().__new__(mcs, name, bases, dct)

class ASTNode(metaclass=ASTNodeMeta):
    def pretty_print(self, indent=0):
        raise NotImplementedError("Subclasses should implement pretty_print")

class IntegerLiteral(ASTNode):
    def __init__(self, value):
        self.value = value

    def pretty_print(self, indent=0):
        return f'{" " * indent}IntegerLiteral(value={self.value})'

    def __repr__(self):
        return f'IntegerLiteral({repr(self.value)})'

class Identifier(ASTNode):
    def __init__(self, name):
        self.name = name

    def pretty_print(self, indent=0):
        return f'{" " * indent}Identifier(name={self.name})'

    def __repr__(self):
        return f'Identifier({repr(self.name)})'
    
class StringLiteral(ASTNode):
    def __init__(self, value):
        self.value = value

    def pretty_print(self, indent=0):
        return f'{" " * indent}StringLiteral(value={self.value})'

    def __repr__(self):
        return f'StringLiteral({repr(self.value)})'
# Literal nodes
class VariableDeclaration(ASTNode):
    def __init__(self, declaration_specifier, assignment_expression):
        self.declaration_specifier = declaration_specifier
        self.assignment_expression = assignment_expression

    def __repr__(self):
        return f"VariableDeclaration({self.declaration_specifier}, {self.assignment_expression})"
    
    def pretty_print(self, indent=0):
        indent_str = ' ' * indent
        return f"{indent_str}VariableDeclaration:\n" + \
               f"{self.declaration_specifier.pretty_print(indent + 2)}\n" + \
               f"{self.assignment_expression.pretty_print(indent + 2)}"


class IntLiteral(ASTNode):
    def __init__(self, value: int):
        self.value = value

    def __repr__(self):
        return f"IntLiteral({self.value})"
    def pretty_print(self, indent=0):
        indent_str = ' ' * indent
        return f"{indent_str}IntLiteral: {self.value}"

class FloatLiteral(ASTNode):
    def __init__(self, value: float):
        self.value = value
    def pretty_print(self, indent=0):
        return ' ' * indent + f"FloatLiteral: {self.value}"
    def __repr__(self):
        return f"FloatLiteral({self.value})"

class BoolLiteral(ASTNode):
    def __init__(self, value: bool):
        self.value = value

    def __repr__(self):
        return f"BoolLiteral({self.value})"
    def pretty_print(self, indent=0):
        return ' ' * indent + f"BoolLiteral: {self.value}"

class StringLiteral(ASTNode):
    def __init__(self, value: str):
        self.value = value
    def pretty_print(self, indent=0):
        return ' ' * indent + f"StringLiteral: '{self.value}'"
    def __repr__(self):
        return f"StringLiteral('{self.value}')"

class Identifier(ASTNode):
    def __init__(self, value: str):
        self.value = value

    def __repr__(self):
        return f"Identifier('{self.value}')"
    def pretty_print(self, indent=0):
        indent_str = ' ' * indent
        return f"{indent_str}Identifier: {self.value}"

class Operator(ASTNode):
    def __init__(self, value: str):
        self.value = value
    def pretty_print(self, indent=0):
        return ' ' * indent + f"Operator: {self.value}"
    def __repr__(self):
        return f"Operator('{self.value}')"

class Symbol(ASTNode):
    def __init__(self, value: str):
        self.value = value
    def pretty_print(self, indent=0):
        return ' ' * indent + f"Symbol: {self.value}"
    def __repr__(self):
        return f"Symbol('{self.value}')"
    
class Keyword(ASTNode):
    def __init__(self, value: str):
        self.value = value
    def pretty_print(self, indent=0):
        return ' ' * indent + f"{self.__class__.__name__}: {self.value}"
    def __repr__(self):
        return f"Keyword('{self.value}')"

class EndOfStatement(ASTNode):
    def __init__(self, value: str):
        self.value = value
    def pretty_print(self, indent=0):
        return ' ' * indent + f"{self.__class__.__name__}: {self.value}"
    def __repr__(self):
        return f"EndOfStatement('{self.value}')"
# Collection literals


class ListLiteral(ASTNode):
    def __init__(self, elements: List[ASTNode]):
        self.elements = elements
    def pretty_print(self, indent=0):
        indent_str = ' ' * indent
        elements_str = ',\n'.join(elem.pretty_print(indent + 2) for elem in self.elements)
        return f"{indent_str}ListLiteral:\n{elements_str}"
    def __repr__(self):
        elements_str = ', '.join(repr(elem) for elem in self.elements)
        return f"ListLiteral([{elements_str}])"

class TupleLiteral(ASTNode):
    def __init__(self, elements: List[ASTNode]):
        self.elements = elements
    def pretty_print(self, indent=0):
        indent_str = ' ' * indent
        elements_str = ',\n'.join(elem.pretty_print(indent + 2) for elem in self.elements)
        return f"{indent_str}TupleLiteral:\n{elements_str}"
    def __repr__(self):
        elements_str = ', '.join(repr(elem) for elem in self.elements)
        return f"TupleLiteral({elements_str})"

# Expressions
class FunctionCall(ASTNode):
    def __init__(self, name: str, arguments: List[ASTNode]):
        self.name = name
        self.arguments = arguments
    def pretty_print(self, indent=0):
        indent_str = ' ' * indent
        arguments_str = ',\n'.join(arg.pretty_print(indent + 2) for arg in self.arguments)
        return f"{indent_str}FunctionCall: {self.name}\n{arguments_str}"
    def __repr__(self):
        arguments_str = ', '.join(repr(arg) for arg in self.arguments)
        return f"FunctionCall('{self.name}', [{arguments_str}])"

class Expression(ASTNode):
    pass

class Literal(Expression):
    def __init__(self, value):
        self.value = value
    def pretty_print(self, indent=0):
        return ' ' * indent + f"{self.__class__.__name__}: {self.value}"

class UnaryExpression(ASTNode):
    def __init__(self, operator: Operator, operand: ASTNode):
        self.operator = operator
        self.operand = operand
    def pretty_print(self, indent=0):
        indent_str = ' ' * indent
        return f"{indent_str}UnaryExpression:\n" + \
               f"{self.operator.pretty_print(indent + 2)}\n" + \
               f"{self.operand.pretty_print(indent + 2)}"
    def __repr__(self):
        return f"UnaryExpression({repr(self.operator)}, {repr(self.operand)})"
class BeliefKeyword(ASTNode):
    def __init__(self):
        pass

    def pretty_print(self, indent=0):
        return f'{" " * indent}BeliefKeyword'

    def __repr__(self):
        return 'BeliefKeyword()'

class LeftParen(ASTNode):
    def __init__(self):
        pass

    def pretty_print(self, indent=0):
        return f'{" " * indent}LeftParen'

    def __repr__(self):
        return 'LeftParen()'

class GreaterThan(ASTNode):
    def __init__(self):
        pass

    def pretty_print(self, indent=0):
        return f'{" " * indent}GreaterThan'

    def __repr__(self):
        return 'GreaterThan()'

class LeftBrace(ASTNode):
    def __init__(self):
        pass

    def pretty_print(self, indent=0):
        return f'{" " * indent}LeftBrace'

    def __repr__(self):
        return 'LeftBrace()'
    
class UtilityFunctionCall(ASTNode):
    def __init__(self, function_name, expression):
        self.function_name = function_name
        self.expression = expression

    def pretty_print(self, indent=0):
        indent_str = ' ' * indent
        expression_str = self.expression.pretty_print(indent + 2) if isinstance(self.expression, ASTNode) else ' ' * (indent + 2) + repr(self.expression)
        return f"{indent_str}UtilityFunctionCall:\n{indent_str}  Function: {self.function_name}\n{expression_str}"

    def __repr__(self):
        return f'UtilityFunctionCall("{self.function_name}", {repr(self.expression)})'


class RightBrace(ASTNode):
    def __init__(self):
        pass

    def pretty_print(self, indent=0):
        return f'{" " * indent}RightBrace'

    def __repr__(self):
        return 'RightBrace()'

class BinaryExpression(ASTNode):
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

    def pretty_print(self, indent=0):
        indent_str = ' ' * indent
        left_str = self.left.pretty_print(indent + 2) if isinstance(self.left, ASTNode) else ' ' * (indent + 2) + repr(self.left)
        right_str = self.right.pretty_print(indent + 2) if isinstance(self.right, ASTNode) else ' ' * (indent + 2) + repr(self.right)
        return f"{indent_str}BinaryExpression:\n{left_str}\n{indent_str}  {self.operator}\n{right_str}"

    def __repr__(self):
        return f'BinaryExpression({repr(self.left)}, "{self.operator}", {repr(self.right)})'


class ArrayIndexing(ASTNode):
    def __init__(self, array: ASTNode, index: ASTNode):
        self.array = array
        self.index = index
    def pretty_print(self, indent=0):
        indent_str = ' ' * indent
        return f"{indent_str}ArrayIndexing:\n" + \
               self.array.pretty_print(indent + 2) + "\n" + \
               self.index.pretty_print(indent + 2)
    def __repr__(self):
        return f"ArrayIndexing({repr(self.array)}, {repr(self.index)})"


# Statements
class CompoundStatement(ASTNode):
    def __init__(self, declarations: List[ASTNode], statements: List[ASTNode]):
        self.declarations = declarations
        self.statements = statements
    def pretty_print(self, indent=0):
        indent_str = ' ' * indent
        declarations_str = '\n'.join(decl.pretty_print(indent + 2) for decl in self.declarations)
        statements_str = '\n'.join(stmt.pretty_print(indent + 2) for stmt in self.statements)
        return f"{indent_str}CompoundStatement:\n" + \
               f"{declarations_str}\n{statements_str}"
    def __repr__(self):
        declarations_str = ', '.join(repr(decl) for decl in self.declarations)
        statements_str = ', '.join(repr(stmt) for stmt in self.statements)
        return f"CompoundStatement([{declarations_str}],\n{statements_str})"


class ArrayAccess(ASTNode):
    def __init__(self, array: ASTNode, index: ASTNode):
        self.array = array
        self.index = index

    def pretty_print(self, indent=0):
        indent_str = ' ' * indent
        array_str = self.array.pretty_print(indent + 2)
        index_str = self.index.pretty_print(indent + 2)
        return f"{indent_str}ArrayAccess:\n" + \
               f"{array_str}\n" + \
               f"{index_str}"

    def __repr__(self):
        return f"ArrayAccess({repr(self.array)}, {repr(self.index)})"
    
class ForLoop(ASTNode):
    def __init__(self, init: ASTNode, condition: ASTNode, update: ASTNode, body: ASTNode):
        self.init = init
        self.condition = condition
        self.update = update
        self.body = body
        
    def __repr__(self):
        return f"ForLoop({repr(self.init)}, {repr(self.condition)}, {repr(self.update)}, {repr(self.body)})"
    
class CharLiteral(ASTNode):
    def __init__(self, value):
        self.value = value

    def pretty_print(self, indent=0):
        return f'{" " * indent}CharLiteral(value={self.value})'

    def __repr__(self):
        return f'CharLiteral({repr(self.value)})'


class IfStatement(ASTNode):
    def __init__(self, condition: ASTNode, true_branch: ASTNode, false_branch: Union[ASTNode, None]):
        self.condition = condition
        self.true_branch = true_branch
        self.false_branch = false_branch
    def pretty_print(self, indent=0):
        indent_str = ' ' * indent
        true_branch_str = self.true_branch.pretty_print(indent + 2)
        false_branch_str = self.false_branch.pretty_print(indent + 2) if self.false_branch else ''
        return f"{indent_str}IfStatement:\n" + \
               self.condition.pretty_print(indent + 2) + "\n" + \
               f"{true_branch_str}\n{false_branch_str}"
    def __repr__(self):
        false_branch_str = repr(self.false_branch) if self.false_branch else "None"
        return f"IfStatement({repr(self.condition)}, {repr(self.true_branch)}, {false_branch_str})"

class DoWhileLoop(ASTNode):
    def __init__(self, body: ASTNode, condition: ASTNode):
        self.body = body
        self.condition = condition

    def pretty_print(self, indent=0):
        indent_str = ' ' * indent
        body_str = self.body.pretty_print(indent + 2)
        return f"{indent_str}DoWhileLoop:\n" + \
               body_str + "\n" + \
               self.condition.pretty_print(indent + 2)

    def __repr__(self):
        return f"DoWhileLoop({repr(self.body)}, {repr(self.condition)})"
    
class WhileLoop(ASTNode):
    def __init__(self, condition: ASTNode, body: ASTNode):
        self.condition = condition
        self.body = body
    def pretty_print(self, indent=0):
        indent_str = ' ' * indent
        body_str = self.body.pretty_print(indent + 2)
        return f"{indent_str}WhileLoop:\n" + \
               self.condition.pretty_print(indent + 2) + "\n" + \
               body_str
    def __repr__(self):
        return f"WhileLoop({repr(self.condition)}, {repr(self.body)})"

class FunctionDefinition(ASTNode):
    def __init__(self, return_type: ASTNode, name: str, parameters: List[tuple[ASTNode, str]], body: ASTNode):
        self.return_type = return_type
        self.name = name
        self.parameters = parameters
        self.body = body
    def pretty_print(self, indent=0):
        indent_str = ' ' * indent
        params_str = ', '.join([p.pretty_print(0) for p in self.parameters])
        body_str = '\n'.join([stmt.pretty_print(indent + 4) for stmt in self.body])
        return f"{indent_str}FunctionDefinition: {self.name}\n" + \
               f"{indent_str}    Return Type: {self.return_type}\n" + \
               f"{indent_str}    Parameters: {params_str}\n" + \
               f"{indent_str}    Body:\n{body_str}"
    def __repr__(self):
        parameters_str = ', '.join(f"{repr(param_type)} {param_name}" for param_type, param_name in self.parameters)
        return f"FunctionDefinition({repr(self.return_type)}, '{self.name}', [{parameters_str}], {repr(self.body)})"

class ArrayLiteral(ASTNode):
    def __init__(self, elements: List[ASTNode]):
        self.elements = elements
    def pretty_print(self, indent=0):
        indent_str = ' ' * indent
        elements_str = ',\n'.join(elem.pretty_print(indent + 2) for elem in self.elements)
        return f"{indent_str}ArrayLiteral:\n{elements_str}"
    def __repr__(self):
        elements_str = ', '.join(repr(elem) for elem in self.elements)
        return f"ArrayLiteral([{elements_str}])"


# class Program(ASTNode):
#     def __init__(self, declarations, statements):
#         self.declarations = declarations
#         self.statements = statements

#     def __repr__(self):
#         return f"Program(declarations={self.declarations}, statements={self.statements})"
    
class Program(ASTNode):
    def __init__(self, statements):
        self.statements = statements
    def pretty_print(self, indent=0):
        indent_str = ' ' * indent
        statements_str = '\n'.join(stmt.pretty_print(indent + 2) for stmt in self.statements)
        return f"{indent_str}Program:\n{statements_str}"
    def __repr__(self):
        return f"Program({', '.join(repr(stmt) for stmt in self.statements)})"

class SelectionStatement(ASTNode):
    def __init__(self, condition: ASTNode, true_branch: ASTNode, false_branch: Union[None, ASTNode]):
        self.condition = condition
        self.true_branch = true_branch
        self.false_branch = false_branch
    def pretty_print(self, indent=0):
        indent_str = ' ' * indent
        true_branch_str = self.true_branch.pretty_print(indent + 2)
        false_branch_str = f"\n{self.false_branch.pretty_print(indent + 2)}" if self.false_branch else ""
        return f"{indent_str}SelectionStatement:\n" + \
               self.condition.pretty_print(indent + 2) + "\n" + \
               true_branch_str + false_branch_str
    def __repr__(self):
        false_branch_str = repr(self.false_branch) if self.false_branch else "None"
        return f"SelectionStatement({repr(self.condition)}, {repr(self.true_branch)}, {false_branch_str})"


class IterationStatement(ASTNode):
    def __init__(self, condition: ASTNode, body: ASTNode, declaration: Union[None, ASTNode] = None):
        self.condition = condition
        self.body = body
        self.declaration = declaration
    def pretty_print(self, indent=0):
        indent_str = ' ' * indent
        body_str = self.body.pretty_print(indent + 2)
        declaration_str = f"{self.declaration.pretty_print(indent + 2)}\n" if self.declaration else ""
        return f"{indent_str}IterationStatement:\n" + \
               declaration_str + \
               self.condition.pretty_print(indent + 2) + "\n" + \
               body_str
    def __repr__(self):
        declaration_str = repr(self.declaration) if self.declaration else "None"
        return f"IterationStatement({repr(self.condition)}, {repr(self.body)}, {declaration_str})"


class ListComprehension(ASTNode):
    def __init__(self, declaration: ASTNode, condition: Union[ASTNode, None], body: ASTNode):
        self.declaration = declaration
        self.condition = condition
        self.body = body
    def pretty_print(self, indent=0):
        indent_str = ' ' * indent
        condition_str = f"\n{self.condition.pretty_print(indent + 2)}" if self.condition else ""
        body_str = self.body.pretty_print(indent + 2)
        return f"{indent_str}ListComprehension:\n" + \
               self.declaration.pretty_print(indent + 2) + \
               condition_str + "\n" + \
               body_str
    def __repr__(self):
        condition_str = repr(self.condition) if self.condition else "None"
        return f"ListComprehension({repr(self.declaration)}, {condition_str}, {repr(self.body)})"

class JumpStatement(ASTNode):
    def __init__(self, keyword: str, expression: Union[None, ASTNode] = None):
        self.keyword = keyword
        self.expression = expression
    def pretty_print(self, indent=0):
        indent_str = ' ' * indent
        expression_str = f": {self.expression.pretty_print(indent)}" if self.expression else ""
        return f"{indent_str}JumpStatement: {self.keyword}{expression_str}"
    def __repr__(self):
        expression_str = repr(self.expression) if self.expression else "None"
        return f"JumpStatement('{self.keyword}', {expression_str})"


# In ast__Classes.py
class PreachStatement(ASTNode):
    def __init__(self, expression):
        self.expression = expression

    def pretty_print(self, indent=0):
        return f'{" " * indent}PreachStatement(expression={self.expression.pretty_print(indent + 2)})'

    def __repr__(self):
        return f'PreachStatement({repr(self.expression)})'



# Declarations
class Declaration(ASTNode):
    def __init__(self, declaration_specifier: Union[None, ASTNode], expression: ASTNode):
        self.declaration_specifier = declaration_specifier
        # self.type_specifier = type_specifier
        # self.identifier = identifier
        self.expression = expression

    def pretty_print(self, indent=0):
        indent_str = ' ' * indent
        specifier_str = self.declaration_specifier.pretty_print(indent + 2) if self.declaration_specifier else "None"
        return f"{indent_str}Declaration:\n" + \
               specifier_str + "\n" + \
               self.expression.pretty_print(indent + 2)
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
    def pretty_print(self, indent=0):
        indent_str = ' ' * indent
        eternal_str = f"Eternal={self.eternal}, " if self.eternal else ""
        type_specifier_str = self.type_specifier.pretty_print(indent + 4) if self.type_specifier else "TypeSpecifier=None"
        return f"{indent_str}DeclarationSpecifier: {eternal_str}\n{type_specifier_str}"



class TypeSpecifier(ASTNode):
    def __init__(self, type_keyword: str):
        self.type_keyword = type_keyword

    def __repr__(self):
        return f"TypeSpecifier('{self.type_keyword}')"
    def pretty_print(self, indent=0):
        indent_str = ' ' * indent
        return f"{indent_str}TypeSpecifier: {self.type_keyword}"

class TupleDeclaration(ASTNode):
    def __init__(self, identifier: str, assignment_expression: ASTNode, value_list: List[ASTNode]):
        self.identifier = identifier
        self.assignment_expression = assignment_expression
        self.value_list = value_list
    def pretty_print(self, indent=0):
        indent_str = ' ' * indent
        values_str = ',\n'.join([val.pretty_print(indent + 4) for val in self.value_list])
        return f"{indent_str}TupleDeclaration:\n" + \
               self.identifier.pretty_print(indent + 4) + "\n" + \
               self.assignment_expression.pretty_print(indent + 4) + "\n" + \
               f"{indent_str}    Values:\n{values_str}"
    def __repr__(self):
        value_list_str = ', '.join(repr(value) for value in self.value_list)
        return f"TupleDeclaration('{self.identifier}', {repr(self.assignment_expression)}, [{value_list_str}])"

class ListDeclaration(ASTNode):
    def __init__(self, identifier: str, value_list: List[ASTNode]):
        self.identifier = identifier
        self.value_list = value_list
    def pretty_print(self, indent=0):
        indent_str = ' ' * indent
        values_str = ',\n'.join([val.pretty_print(indent + 4) for val in self.value_list])
        return f"{indent_str}ListDeclaration:\n" + \
               self.identifier.pretty_print(indent + 4) + "\n" + \
               f"{indent_str}    Values:\n{values_str}"
    def __repr__(self):
        value_list_str = ', '.join(repr(value) for value in self.value_list)
        return f"ListDeclaration('{self.identifier}', [{value_list_str}])"


class ArrayDeclaration(ASTNode):
    def __init__(self, type_specifier: ASTNode, identifier: str, expressions: List[ASTNode]):
        self.type_specifier = type_specifier
        self.identifier = identifier
        self.expressions = expressions
    def pretty_print(self, indent=0):
        indent_str = ' ' * indent
        expressions_str = ',\n'.join([expr.pretty_print(indent + 4) for expr in self.expressions])
        return f"{indent_str}ArrayDeclaration:\n" + \
               self.type_specifier.pretty_print(indent + 4) + "\n" + \
               self.identifier.pretty_print(indent + 4) + "\n" + \
               f"{indent_str}    Expressions:\n{expressions_str}"
    def __repr__(self):
        expressions_str = ', '.join(repr(expr) for expr in self.expressions)
        return f"ArrayDeclaration({repr(self.type_specifier)}, '{self.identifier}', [{expressions_str}])"

# Utility functions
class BuiltinFunction(ASTNode):
    def __init__(self, name: str, arguments: List[ASTNode]):
        self.name = name
        self.arguments = arguments
    def pretty_print(self, indent=0):
        indent_str = ' ' * indent
        arguments_str = ',\n'.join(arg.pretty_print(indent + 2) for arg in self.arguments)
        return f"{indent_str}BuiltinFunction: {self.name}\n{arguments_str}"
    def __repr__(self):
        arguments_str = ', '.join(repr(arg) for arg in self.arguments)
        return f"BuiltinFunction('{self.name}', [{arguments_str}])"
