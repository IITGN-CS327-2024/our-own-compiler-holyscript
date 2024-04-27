import sys
import os
import lexer
from lark import Lark, Transformer, Tree
from lark import ast_utils
import asttransformer, astclasses
from anytree import Node, RenderTree
import astclasses
from wasm_generator import WATGenerator  # Import the WAT generator
import subprocess

# Load your grammar from the file
with open('mygrammar.lark') as file:
    grammar = file.read()
parser = Lark(grammar, start='start', parser='earley')

transformer = ast_utils.create_transformer(sys.modules[__name__], asttransformer.ToAst())

def read_holy_script_file(file_path):
    try:
        with open(file_path, 'r') as file:
            content = file.read()
            # print("File Content Read:", content)  # Debug: Print content to verify it's read correctly
            return content
    except IOError as e:
        print(f"Error reading file {file_path}: {e}")
        return None

class SemanticAnalyzer:
    def __init__(self):
        self.symbol_table = {}
        self.scope_stack = ['global']

    def analyze(self, node):
        node_type = type(node).__name__
        if node_type == "Program":
            print("Analyzing program")
            for statement in node.statements:
                if self.analyze(statement) == -1:
                    return "Code contains semantic errors"
            return "Code analyzed successfully"
        
        elif node_type == "VariableDeclaration":
            return self.handle_variable_declaration(node)
        elif node_type == "PreachStatement":
            return self.handle_preach_statement(node)
        elif node_type in ["IntegerLiteral", "CharLiteral", "StringLiteral", "BoolLiteral", "FloatLiteral"]:
            return self.get_literal_type(node_type)
        elif node_type == "CompoundStatement":
            return self.handle_compound_statement(node)
        elif node_type == "Identifier":
            return self.handle_identifier(node)
        elif node_type == "IfStatement":
            return self.handle_if_statement(node)
        elif node_type == "BinaryExpression":
            return self.handle_binary_expression(node)
        elif node_type in ["LeftBrace", "RightBrace"]:
            return None  # Ignore braces as they are not semantically relevant
        elif node_type == "TupleDeclaration":
            return self.handle_tuple_declaration(node)
        elif node_type == "ForLoop":
            return self.handle_for_loop(node)
        elif node_type == "WhileLoop":
            return self.handle_while_loop(node)
        else:
            print(f"Unhandled node type: {node_type}")
            return -1
    def handle_preach_statement(self, node):
        # Analyze the expression within the PreachStatement to ensure it's valid
        expression_result = self.analyze(node.expression)
        if expression_result == -1:
            print("Error evaluating expression in preach statement")
            return -1
        print(f"Preach statement evaluated: {node.expression.value}")
        return 0
    def handle_for_loop(self, node):
        self.enter_scope()
        self.analyze(node.init)
        condition_type = self.analyze(node.condition)
        if condition_type != 'boolean':
            print("Error: Loop condition is not a boolean")
            self.exit_scope()
            return -1
        self.analyze(node.update)
        result = self.analyze(node.body)
        self.exit_scope()
        return result
    def handle_tuple_declaration(self, node):
        tuple_values = [self.analyze(value) for value in node.values]
        if not all(v == tuple_values[0] for v in tuple_values):  # Ensuring all elements are of the same type
            print("Error: Tuple elements have different types")
            return -1
        self.symbol_table[node.identifier.value] = {'type': f"tuple({tuple_values[0]})", 'scope': self.scope_stack[-1]}
        return 0
    def get_literal_type(self, node_type):
        type_mapping = {
            'IntegerLiteral': 'int',
            'CharLiteral': 'char',
            'StringLiteral': 'str',
            'BoolLiteral': 'boolean',
            'FloatLiteral': 'float'
        }
        return type_mapping.get(node_type, None)

    def handle_variable_declaration(self, node):
        var_type = node.declaration_specifier.type_specifier.type_keyword
        identifier = node.assignment_expression.left.value
        self.symbol_table[identifier] = {'type': var_type, 'scope': self.scope_stack[-1]}  # Pre-declare variable
        expression_result = self.analyze(node.assignment_expression)

        if not self.is_type_compatible(var_type, expression_result):
            print(f"Error: Type mismatch for '{identifier}' ({var_type} expected, got {expression_result}).")
            return -1
        print(f"Added '{identifier}' of type '{var_type}' to the symbol table in scope '{self.scope_stack[-1]}'.")
        return 0


    def handle_identifier(self, node):
        identifier = node.value
        if identifier in self.symbol_table:
            return self.symbol_table[identifier]['type']
        print(f"Error: Identifier '{identifier}' is not declared.")
        return -1

    def handle_binary_expression(self, node):
        left_type = self.analyze(node.left)
        right_type = self.analyze(node.right)

        # Define operator types
        comparison_operators = {'==', '!=', '<', '>', '<=', '>=', '&&', '||'}
        arithmetic_operators = {'+', '-', '*', '/', '%', '|=', '&=', '+=', '-=', '*=', '/=', '%='}

        # Handle comparison (resulting in boolean)
        if node.operator in comparison_operators:
            if left_type != right_type:
                print(f"Type mismatch in comparison: {left_type} vs. {right_type}")
                return -1
            return 'boolean'

        # Handle arithmetic (resulting in type of operands)
        elif node.operator in arithmetic_operators:
            if left_type == right_type:
                return left_type
            print(f"Type mismatch in arithmetic: {left_type} vs. {right_type}")
            return -1

        # Handle assignment (simple equality is a special case)
        elif node.operator == '=':
            if left_type == right_type:
                return right_type
            print(f"Type mismatch in assignment: {left_type} cannot be assigned to {right_type}")
            return -1

        else:
            print(f"Unhandled operator: {node.operator}")
            return -1
    def handle_while_loop(self, node):
        self.enter_scope()
        condition_result = self.analyze(node.condition)
        if condition_result != 'boolean':
            print("Error: Condition in while loop is not boolean.")
            self.exit_scope()
            return -1
        
        body_result = self.analyze(node.body)
        self.exit_scope()
        return body_result if body_result != -1 else -1
        
        body_result = self.analyze(node.body)
        self.exit_scope()
        return body_result if body_result != -1 else -1
    def handle_compound_statement(self, node):
        self.enter_scope()
        for statement in node.statements:
            if self.analyze(statement) == -1:
                self.exit_scope()
                return -1
        self.exit_scope()
        return 0
    def handle_if_statement(self, node):
        condition_result = self.analyze(node.condition)
        if condition_result != 'boolean':
            print("Error: Condition in if statement is not a boolean expression")
            return -1
        # Handle the branches
        true_branch_result = self.handle_compound_statement(node.true_branch)
        false_branch_result = 0  # Default to successful if no else branch
        if node.false_branch:
            false_branch_result = self.handle_compound_statement(node.false_branch)

        if true_branch_result == -1 or false_branch_result == -1:
            return -1
        return 0

    def enter_scope(self):
        self.scope_stack.append({})

    def exit_scope(self):
        if len(self.scope_stack) > 1:
            self.scope_stack.pop()
    def is_type_compatible(self, expected_type, actual_type):
        return expected_type == actual_type
    



def convert_wat_to_wasm(wat_file, wasm_file):
    try:
        subprocess.run(['wat2wasm', wat_file, '-o', wasm_file], check=True)
    except subprocess.CalledProcessError as e:
        print("Failed to convert WAT to WASM:", e)




def run_script(text, file_path):
    start_marker = "summon HolyScript"
    end_marker = "doom"
    start_idx = text.find(start_marker)
    end_idx = text.find(end_marker)

    if start_idx != -1 and end_idx != -1 and end_idx > start_idx:
        start_idx += len(start_marker)
        script_text = text[start_idx:end_idx].strip()
    else:
        print("Error: Script must be enclosed between 'summon HolyScript' and 'doom'.")
        return

    tokens, error = lexer.run(file_path, script_text)
    if error:
        print(error.as_string())
        return

    script = " ".join(str(token) for token in tokens)
    tree = parser.parse(script)
    my_ast = transformer.transform(tree)
    semantic_analyzer = SemanticAnalyzer()
    semantic_output = semantic_analyzer.analyze(my_ast)

    if semantic_output != "Code analyzed successfully":
        print("Semantic analysis failed:", semantic_output)
        return

    # Generate WAT code from the AST
    wat_generator = WATGenerator()
    wat_code = wat_generator.generate_wat(my_ast)
    output_path = file_path.replace('.holy', '.wat')

    # Write the generated WAT code to a file
    with open(output_path, 'w') as output_file:
        output_file.write(wat_code)
    print(f"WAT file generated at {output_path}")

    # Convert the generated WAT file to a WASM file
    wasm_output_path = output_path.replace('.wat', '.wasm')
    convert_wat_to_wasm(output_path, wasm_output_path)
    print(f"WASM file generated at {wasm_output_path}")

def is_holy_script_file(file_path):
    return os.path.isfile(file_path) and file_path.endswith('.holy')

def run_cli():
    print("""
══════════════════════════════════════
Welcome, faithful coder, to the HolyScript CLI.
Here, thou mayest execute thy scripts line by line,
as if whispering directly into the ears of the machine.

Type 'exit' to depart.
══════════════════════════════════════
""")
    while True:
        line = input('HolyScript>>> ')
        if line.strip().lower() == 'exit':
            print("Farewell, till we meet again in the realm of code.")
            break

        tokens, error = lexer.run('<stdin>', line)
        if error:
            print(error.as_string())
        else:
            values = []
            for token in tokens:
                values.append(str(token))
            # Print the values separated by commas
            # print(" ".join(values))
            script = (" ".join(values))
            tree = parser.parse(script)
            print(tree.pretty())
            my_ast = transformer.transform(tree)
            print(my_ast)
            print(my_ast.pretty_print())
            # print(transform_ast_string(my_ast))
            semantic_analyzer = SemanticAnalyzer()
            output  = semantic_analyzer.analyze(my_ast)
            # print(output)

if __name__ == "__main__":
    if len(sys.argv) == 2:
        file_path = sys.argv[1]
        if is_holy_script_file(file_path):
            text = read_holy_script_file(file_path)
            if text is not None:
                run_script(text, file_path)
            else:
                print(f"Failed to read the sacred text: {file_path}")
        else:
            print(f"The provided scripture '{file_path}' is not found or lacks the sacred .holy suffix.")
    else:
        run_cli()
