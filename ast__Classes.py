from typing import Union, List
import sys
from dataclasses import dataclass
from lark import Lark, ast_utils, Transformer, v_args, Tree
from lark.tree import Meta, Tree

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
    
class MemberAccessExpression(ASTNode):
    def __init__(self, object_expr, operation=None, index=None):
        self.object_expr = object_expr  # The object being accessed (e.g., array, list, tuple)
        self.operation = operation      # The operation (e.g., 'head', 'tail') or attribute being accessed
        self.index = index              # The index if it's an indexing operation

    def pretty_print(self, indent=0):
        base_indent = " " * indent
        parts = [f"{base_indent}MemberAccessExpression:"]
        parts.append(self.object_expr.pretty_print(indent + 2))
        if self.operation:
            parts.append(f"{base_indent}  Operation: {self.operation}")
        if self.index:
            parts.append(f"{base_indent}  Index: {self.index.pretty_print(indent + 2)}")
        return "\n".join(parts)

    def __repr__(self):
        return f"MemberAccessExpression({repr(self.object_expr)}, operation={repr(self.operation)}, index={repr(self.index)})"




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
        # Initialize the output string
        output = " " * indent + "VariableDeclaration:\n"

        # Check if declaration_specifier is not None before printing
        if self.declaration_specifier:
            output += self.declaration_specifier.pretty_print(indent + 2) + "\n"
        else:
            output += " " * (indent + 2) + "No Declaration Specifier\n"

        # Check if assignment_expression is not None before printing
        if self.assignment_expression:
            output += self.assignment_expression.pretty_print(indent + 2)
        else:
            output += " " * (indent + 2) + "No Assignment Expression\n"

        return output


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
        ind = '    ' * indent
        result = ind + "{\n"
        
        # Handling declarations if any
        for decl in self.declarations:
            if hasattr(decl, 'pretty_print'):
                result += decl.pretty_print(indent + 1) + "\n"
            else:
                result += ind + "    # Declaration without pretty_print\n"
        
        # Handling statements
        for stmt in self.statements:
            if hasattr(stmt, 'pretty_print'):
                result += stmt.pretty_print(indent + 1) + "\n"
            else:
                result += ind + "    # Statement without pretty_print\n"

        result += ind + "}"
        return result
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

    def pretty_print(self, indent=0):
        indent_str = ' ' * indent
        deeper_indent_str = ' ' * (indent + 4)

        init_str = (self.init.pretty_print(indent + 4) if hasattr(self.init, 'pretty_print') else str(self.init))
        condition_str = (self.condition.pretty_print(indent + 4) if hasattr(self.condition, 'pretty_print') else str(self.condition))
        update_str = (self.update.pretty_print(indent + 4) if hasattr(self.update, 'pretty_print') else str(self.update))
        body_str = (self.body.pretty_print(indent + 4) if hasattr(self.body, 'pretty_print') else str(self.body))

        pretty_str = (
            f"{indent_str}ForLoop:\n"
            f"{deeper_indent_str}Init:\n{init_str}\n"
            f"{deeper_indent_str}Condition:\n{condition_str}\n"
            f"{deeper_indent_str}Update:\n{update_str}\n"
            f"{deeper_indent_str}Body:\n{body_str}"
        )
        return pretty_str

    
class CharLiteral(ASTNode):
    def __init__(self, value):
        self.value = value

    def pretty_print(self, indent=0):
        return f'{" " * indent}CharLiteral(value={self.value})'

    def __repr__(self):
        return f'CharLiteral({repr(self.value)})'

class MultiplicativeExpression(ASTNode):
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

    def __repr__(self):
        return f"{self.__class__.__name__}({self.left}, '{self.operator}', {self.right})"

    def pretty_print(self, indent=0):
        indent_str = ' ' * indent
        left_str = self.left.pretty_print(indent + 2) if hasattr(self.left, 'pretty_print') else str(self.left)
        right_str = self.right.pretty_print(indent + 2) if hasattr(self.right, 'pretty_print') else str(self.right)
        return f"{indent_str}{self.__class__.__name__}:\n{left_str}\n{indent_str}Operator: {self.operator}\n{right_str}"


class IfStatement(ASTNode):
    def __init__(self, condition: ASTNode, true_branch: ASTNode, false_branch: Union[ASTNode, None]):
        self.condition = condition
        self.true_branch = true_branch
        self.false_branch = false_branch
    def pretty_print(self, indent=0):
        ind = '    ' * indent
        result = ind + "if ("
        # Check if condition is a Lark Tree and handle it appropriately
        if isinstance(self.condition, Tree):
            # Handling Tree objects simply as a placeholder; you might need to process them
            result += "Complex Condition Processed for Display"
        else:
            result += self.condition.pretty_print(0)
        result += ") {\n"
        result += self.true_branch.pretty_print(indent + 1) + "\n"
        if self.false_branch:
            result += ind + "} else {\n"
            result += self.false_branch.pretty_print(indent + 1) + "\n"
        result += ind + "}"
        return result
    def __repr__(self):
        false_branch_str = repr(self.false_branch) if self.false_branch else "None"
        return f"IfStatement({repr(self.condition)}, {repr(self.true_branch)}, {false_branch_str})"

class DoWhileLoop(ASTNode):
    def __init__(self, body: ASTNode, condition: ASTNode):
        self.body = body
        self.condition = condition

    def __repr__(self):
        return f"DoWhileLoop(body={repr(self.body)}, condition={repr(self.condition)})"

    def pretty_print(self, indent=0):
        indent_str = ' ' * indent
        body_str = self.body.pretty_print(indent + 2)
        condition_str = self.condition.pretty_print(indent + 2)
        return f"{indent_str}DoWhileLoop:\n{indent_str}  Body:\n{body_str}\n{indent_str}  Condition:\n{condition_str}"

    
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
        # Adjusting indentation for better readability
        ind = '    ' * indent
        # Print return type and function name
        result = f"{ind}{self.return_type.type_keyword} {self.name.value}("
        # Handle parameters
        params_str = ', '.join(f"{ptype} {pname}" for ptype, pname in self.parameters)
        result += params_str + ") {\n"
        # Print the function body using its own pretty_print method
        result += self.body.pretty_print(indent + 1) + "\n"
        result += ind + "}"
        return result
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
    def __init__(self, keyword, expression=None):
        self.keyword = keyword
        self.expression = expression

    def __repr__(self):
        return f"JumpStatement(keyword='{self.keyword}', expression={repr(self.expression)})"

    def pretty_print(self, indent=0):
        indent_str = ' ' * indent
        expr_str = self.expression.pretty_print(indent + 2) if self.expression else ""
        return f"{indent_str}JumpStatement: {self.keyword}\n{expr_str}"



# In ast__Classes.py
class PreachStatement(ASTNode):
    def __init__(self, expression):
        self.expression = expression

    def pretty_print(self, indent=0):
        expression_str = (self.expression.pretty_print(indent + 2)
                          if isinstance(self.expression, ASTNode)
                          else repr(self.expression))
        return f'{" " * indent}PreachStatement(expression={expression_str})'

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
    def __init__(self, identifier, values):
        self.identifier = identifier
        self.values = values

    def pretty_print(self, indent=0):
        indent_str = ' ' * indent
        values_str = ',\n'.join(value.pretty_print(indent + 2) for value in self.values)
        return f"{indent_str}TupleDeclaration:\n{indent_str + '  '}Identifier: {self.identifier.pretty_print(0)}\n{indent_str + '  '}Values:\n{values_str}"

    def __repr__(self):
        values_repr = ', '.join(repr(value) for value in self.values)
        return f"TupleDeclaration({repr(self.identifier)}, [{values_repr}])"



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
        expressions_str = ', '.join([expr.pretty_print(indent + 4) for expr in self.expressions])
        return f"{indent_str}ArrayDeclaration:\n" + \
               f"{indent_str + '  '}Type Specifier: {self.type_specifier.pretty_print(indent + 4)}\n" + \
               f"{indent_str + '  '}Identifier: {self.identifier}\n" + \
               f"{indent_str + '  '}Expressions: {expressions_str}\n"
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
