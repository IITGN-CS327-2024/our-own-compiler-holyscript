import sys
import os
import lexer
from lark import Lark, Transformer, Tree
from typing import List
from dataclasses import dataclass
from lark import Lark, ast_utils, Transformer, v_args
from lark.tree import Meta
import ast__Classes
import ast_Transformer

this_module = sys.modules[__name__]

# Load your grammar from the file
with open('mygrammar.lark') as file:
    grammar = file.read()
parser = Lark(grammar, start='start', parser='earley')


transformer = ast_utils.create_transformer(this_module, ast_Transformer.ToAst())

def read_holy_script_file(file_path):
    try:
        with open(file_path, 'r') as file:
            return file.read()
    except IOError as e:
        print(f"Error reading file {file_path}: {e}")
        return None

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
    else:
            values = []
            for token in tokens:
                if isinstance(token, lexer.Identifier):
                    values.append("IDENTIFIER")
                elif isinstance(token, lexer.Int):
                    values.append("INTEGER")
                elif isinstance(token, lexer.Float):
                    values.append("FLOAT")
                elif isinstance(token, lexer.StringToken):
                    values.append("STRING")
                elif isinstance(token, lexer.Bool):
                    values.append("BOOLEAN")
                elif isinstance(token, lexer.EndOfStatement):
                    values.append("ENDOFSTMT")
                else:
                    values.append(str(token))
            # Print the values separated by commas
            # print(" ".join(values))
            script = (" ".join(values))
            # print(script)
            tree = parser.parse(script)
            print(tree.pretty())
            my_ast = transformer.transform(tree)
            print(my_ast)

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
                if isinstance(token, lexer.Identifier):
                    values.append("IDENTIFIER")
                elif isinstance(token, lexer.Int):
                    values.append("INTEGER")
                elif isinstance(token, lexer.Float):
                    values.append("FLOAT")
                elif isinstance(token, lexer.StringToken):
                    values.append("STRING")
                elif isinstance(token, lexer.Bool):
                    values.append("BOOLEAN")
                elif isinstance(token, lexer.EndOfStatement):
                    values.append("ENDOFSTMT")
                else:
                    # Convert the token to a string for all other token types
                    values.append(str(token))
            # Print the values separated by commas
            # print(" ".join(values))
            script = (" ".join(values))
            tree = parser.parse(script)
            my_ast = transformer.transform(tree)
            print(my_ast)

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
        # pass