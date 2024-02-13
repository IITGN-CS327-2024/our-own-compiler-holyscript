import sys
import os
import lexer

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
        print("Tokens:")
        lexer.print_tokens(tokens)

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
            print("Tokens:")
            lexer.print_tokens(tokens)

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
