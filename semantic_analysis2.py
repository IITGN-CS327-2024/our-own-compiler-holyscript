from lark import Lark
from lark.tree import Tree  # Import the Tree class

import sys 
grammar = """
start: program
program: statement+

statement: assignment | print_statement | variable_declaration |  if_else_statement | while_loop | closure_definition |  function_definition | unary_operation_assign | exception_handling_statement | function_call_statement | tuple_statement | array_declaration | array_operation_stms| string_ops_stms | respond_stms 
COMMENT_MULTI: /\$\*.*?\*\$/s
COMMENT: /\$.*/ 

integer : /[0-9][0-9]*/
identifier:/[a-zA-Z_][a-zA-Z0-9_]*/
compareop :  EQEQ | NOTEQ | LTEQ |GTEQ |GT | LT
binaryop : PLUS | MINUS| MUL| INT_DIV| MODULO| AND| OR| POWER
PLUS  : "+" 
MINUS : "-" 
MUL   : "*"
INT_DIV : "/"
EQEQ  : "=="
NOTEQ  :"!="
GT    : ">"
LT    : "<"
GTEQ  : ">="
LTEQ  : "<="
MODULO: "%"
AND   : "and"
OR     :"or"
POWER  :"**"
boolean: TRUE | FALSE
TRUE: "true"
FALSE: "false"
unaryop : PLPL | MIMI
PLPL: "++"
MIMI: "--"

string:/"[^"]*"/
INT : "int" 
BOOL : "bool" 
STRINGK : "string" 
VOID : "void" 
variable_type: INT | BOOL | STRINGK | VOID

variable_declaration: "assign"  variable_type ":" identifier "=" expression   ";"


assignment: identifier "=" expression ";"
print_statement: "prnt" "(" expression ")" ";"

expression:  identifier | integer | boolean |  string  | unary_operation| binary_operation | compare_operation | function_call | tuple_operations | array_operation | string_ops
unary_operation : expression unaryop
binary_operation : expression binaryop expression 
unary_operation_assign :  expression unaryop ";"
compare_operation : expression compareop expression

if_else_statement : "agar"  expression "{" program "}" | "agar"  expression "{" program "}" baki_s | "agar"  expression "{" program "}" nahi_to_s
baki_s : ("baki" expression "{" program "}" )+ | ("baki" expression "{" program "}" )+  nahi_to_s 
nahi_to_s : "nahito"  "{" program "}" 

while_loop: "jabtak" expression "{" program "}" 

function_definition : "func"  ":"  variable_type identifier "(" ")" "{"  program  "}" | "func"  ":"  variable_type identifier "(" parameter_list ")" "{" program  "}" 
parameter_list : parameter | parameter ("," parameter)+

parameter :  variable_type ":" identifier 

function_call : identifier "(" ")"  | identifier "(" argument_values ")"
argument_values : expression | expression ("," expression)+ 

function_call_statement : identifier "(" ")"  ";" | identifier "(" argument_values ")" ";"
respond_stms :  "respond"  expression ";"

closure_definition  :  "func" ":"  variable_type identifier "(" parameter_list ")" "{" program  "func"  ":"  variable_type identifier "(" parameter_list ")" "{"  program      "}" program  "}"

exception_handling_statement : "try" "{" program "throw"  identifier ";" "}"  "catch"  "(" identifier ")" "{" program "}"

tuple_statement : "let"  "tuple" ":" identifier "=" "("  argument_values ")" ";"
tuple_operations : identifier "." "at" "(" expression ")"  


array_declaration : "assign"  variable_type ":" identifier "("  expression  ")" ";"| "assign"  variable_type ":" identifier "("  expression  ")" "=" "[" argument_values "]" ";"

array_operation : identifier "." ("size" | "head" | "tail") "(" ")"   |  identifier "[" expression "]"  


array_operation_stms : identifier "[" expression "]" "="  expression ";"

slice : "slice"
concat : "concat"
string_ops : identifier "." slice "(" expression "," expression ")" | identifier "." concat "(" identifier ")" 
string_ops_stms : identifier "." slice "(" expression "," expression ")" ";" | identifier "." concat "(" identifier ")" ";"

%import common.LETTER
%import common.DIGIT
%import common.SPECIAL_CHARACTER
%import common.WS
%ignore WS
%ignore COMMENT
%ignore COMMENT_MULTI
"""

# Load the code from a file
if len(sys.argv) != 2:
    print("Run by terminal, give the path of sample's files python, path like testcases/sample1.ajnv")
    sys.exit(1)

file_path = sys.argv[1]

# Load the code from a file
with open(file_path, 'r') as file:
    code = file.read()
""" 
file_path = 'testcases/sample1.ajnv'  # Update with your file path
with open(file_path, 'r') as file:
    code = file.read()
"""
# Create the Lark parser
parser = Lark(grammar, start="start", parser='lalr')

# Parse the code
tree = parser.parse(code)
#print(tree)

# Display the  AST
#print("AST:\n", tree.pretty())
""" """
from lark import Tree, Token

def remove_expression_nodes(tree):
    new_children = []
    for node in tree.children:
        # If the node is a Tree and its data is "expression",
        # add its children directly to the list of new children
        if isinstance(node, Tree) and node.data == "expression":
            new_children.extend(node.children)
        # If the node is not a Tree or its data is not "expression",
        # process it recursively
        else:
            if isinstance(node, Tree):
                new_child = remove_expression_nodes(node)
                if new_child is not None:
                    new_children.append(new_child)
            else:
                new_children.append(node)
    # Return a new tree without the "expression" nodes
    if new_children:
        return Tree(tree.data, new_children)
    else:
        return None

# Parse the code
tree = parser.parse(code)

# Remove the "expression" nodes from the AST
tree_without_expression = remove_expression_nodes(tree)
#print(tree_without_expression)
# Display the modified AST
#print("AST without expression nodes:\n", tree_without_expression.pretty())
""" 
def print_tree(tree, indent=0):
    if isinstance(tree, Tree):
        if tree.data not in ['statement', 'program', 'expression']:
            print("  " * indent + tree.data)
        for child in tree.children:
            print_tree(child, indent + 1)
    else:
        print("  " * indent + str(tree))

# Print the modified AST in a tree-like structure
print("AST without expression nodes:")
print_tree(tree_without_expression)
"""
from lark import Lark, Tree
from anytree import Node, RenderTree

# Your grammar and code loading code here

# Parse the code
tree = parser.parse(code)

# Remove the "expression" nodes from the AST
tree_without_expression = remove_expression_nodes(tree)

# Function to recursively convert Lark tree to Anytree tree
def lark_to_anytree(lark_tree):
    if isinstance(lark_tree, Tree):
        # Create a node for the current tree node
        node = Node(lark_tree.data)
        # Recursively convert and add children
        for child in lark_tree.children:
            child_node = lark_to_anytree(child)
            child_node.parent = node
        return node
    else:
        # Create a leaf node for tokens
        return Node(str(lark_tree))

# # Convert the Lark tree to Anytree tree
# anytree_tree = lark_to_anytree(tree_without_expression)

# # Render and display the Anytree tree
# for pre, fill, node in RenderTree(anytree_tree):
#     print("%s%s" % (pre, node.name))


anytree_tree1 = lark_to_anytree(tree)

# Render and display the Anytree tree
for pre, fill, node in RenderTree(anytree_tree1):
    print("%s%s" % (pre, node.name))



class SemanticAnalyzer:
    def __init__(self):
        self.symbol_table = {}  # Symbol table to store declared identifiers
        self.scope_stack = []   # Stack to keep track of scopes

    def analyze(self, tree):
        if tree.data == "start":
            # Traverse each statement in the program
            self.scope_stack = ["global"]
            for child in tree.children:
                output = self.analyze(child)
                if (output == -1):
                    return "Code Contains semantic errors"

        elif tree.data == "program":
            # Traverse each statement in the program
            for statement in tree.children:
                output = self.analyze(statement)
                if(output==-1):
                    return -1 
        elif tree.data == "statement":
            # Traverse each statement in the program
            for statement in tree.children:
                output = self.analyze(statement)
                if(output == -1):
                    return -1 

        elif tree.data == "variable_declaration":
            # Extract variable type, identifier, and expression
            var_type = tree.children[0].children[0]
            identifier = tree.children[1].children[0].value 
            expression_tree = tree.children[2]
            expression_type = self.analyze(expression_tree)
            print("expression_type", expression_type)
            print("variable_declaration", var_type, identifier)
            if identifier in self.symbol_table and self.symbol_table[identifier]['scope'] == self.scope_stack[-1]:
                print(f"Error: Identifier {identifier} already declared in this scope.")
                return -1
                #print(f"Found identifier '{identifier}' in scope {scope}.")
            elif expression_type != var_type :
                print(f"Error: type of identifier {identifier} {var_type} doesn't matches with the expression type {expression_type}")
                return -1 
            else:
                # Add the identifier to the symbol table with the current scope
                self.symbol_table[identifier] = {'type': var_type, 'scope': self.scope_stack[-1]}
                #print(f"Added '{identifier}' of type '{var_type}' to symbol table in scope {self.scope_stack[-1]}.")
        elif tree.data == "identifier":
            # Extract identifier value
            identifier = tree.children[0]

            # Check if the identifier is declared in any enclosing scope
            found = False
            for scope in reversed(self.scope_stack):
                if identifier in self.symbol_table and self.symbol_table[identifier]['scope'] == scope:
                    found = True
                    return self.symbol_table[identifier]['type']
                    #print(f"Found identifier '{identifier}' in scope {scope}.")
            if not found:
                print(f"Error: Identifier '{identifier}' hasn't been declared in any enclosing scope.")
                return -1 

        elif tree.data == "assignment":
            # Extract variable type, identifier, and expression
            identifier_tree = tree.children[0]
            expression_tree = tree.children[1]
            #print("assignment", identifier_tree.children[0], expression_tree.children[0])
            type_of_exp = self.analyze(expression_tree)
            type_of_iden = self.analyze(identifier_tree)
            # Check if the identifier is already declared
            if type_of_exp == type_of_iden and type_of_exp != -1:
                return 1 
            else:
                # Add the identifier to the symbol table
                print(f"Error: Type of Identifier {identifier_tree.children[0]} isn't same with right side expression {type_of_exp} declared.")
                return -1 
        elif tree.data == "print_statement":
            expression_tree = tree.children[0]
            #print("print_statement",expression_tree )
            return self.analyze(expression_tree)

        elif tree.data == "if_else_statement":
            # Extract expression and program
            expression_tree = tree.children[0]
            program_tree = tree.children[1].children[0]
            print("if_else", expression_tree, program_tree)
            # Perform type checking for the condition expression
            condition_type = self.analyze(expression_tree)
            print("condition_type", condition_type)
            if condition_type != "bool":
                print("Error: Condition expression in if statement must evaluate to boolean.")
                return -1

            # Analyze the program inside the if block
            self.analyze(program_tree)
            
            # Analyze each "baki_s" statement
            #print(tree.children[2].children[4])
            #print(len(tree.children[2].children))
            baki_s_tree = tree.children[2]

            for i in range(len(tree.children[2].children)):
                # comparision condition 
                print("i", i)
                print(baki_s_tree.children[i].data)
                if(baki_s_tree.children[i].data == "nahi_to_s"):
                    break 
                elif i%2 == 0:
                    baki_tree_comp = baki_s_tree.children[i]
                    #print(baki_s_tree)
                    print(baki_tree_comp)
                    #print(baki_tree)
                    baki_condition_type = self.analyze(baki_tree_comp)
                    if baki_condition_type != "bool":
                        print("Error: Condition expression in baki_s statement must evaluate to boolean.")
                        return -1
                    # Analyze the program inside the baki_s block
                    
                else: 
                    print("baki" , baki_s_tree.children[i])
                    self.analyze(baki_s_tree.children[i])

            if(baki_s_tree.children[-1].data == "nahi_to_s"):
                nahi_to_tree = baki_s_tree.children[-1]
                #print(baki_s_tree)
                self.analyze(nahi_to_tree.children[0])
                  
                 
        elif tree.data == "while_loop":
            expression_tree = tree.children[0]
            program_tree = tree.children[1].children[0]
            #print("while_loop", expression_tree)
            #print(program_tree)
            # Perform type checking for the condition expression
            condition_type = self.analyze(expression_tree)
            print("condition_type", condition_type)
            if condition_type != "bool":
                print("Error: Condition expression in while statement must evaluate to boolean.")
                return -1

            # Analyze the program inside the if block
            self.analyze(program_tree)
        
        elif tree.data == "unary_operation_assign":
            # Extract expression and unary operation
            expression_tree = tree.children[0]
            unary_operator = tree.children[1].children[0]

            # Analyze the expression to get its type
            expression_type = self.analyze(expression_tree)

            if expression_type == "int":
                return "int"
            else:
                print(f"Error: Unary operation '{unary_operator}' can only be applied to integer type.")
                return -1

        elif tree.data == "function_definition":
            # Extract function details
            function_type = tree.children[0].children[0]
            function_name = tree.children[1].children[0].value
            print("Function:", function_type, function_name)
            # Create a new scope for the function
            self.scope_stack.append(function_name)
            # Analyze function body
            # Analyze parameter list
            param_list_tree = tree.children[2]
            paramater_list = []
            for param_tree in param_list_tree.children:
                param_type = param_tree.children[0].children[0]
                param_name = param_tree.children[1].children[0].value
                print("Parameter:", param_type, param_name)
                paramater_list.append(param_type)
                # Add parameters to the symbol table
                self.symbol_table[param_name] = {'type': param_type, 'scope': function_name}
            # Analyze function body
            self.symbol_table[function_name] = {'type': function_type, 'scope': self.scope_stack[-1], 'paramaters': paramater_list}

            function_body_tree = tree.children[3]
            print("function_body_tree", function_body_tree)
            self.analyze(function_body_tree)
            # Pop the function scope after analysis
            self.scope_stack.pop()

        elif tree.data == "respond_stms":
            # Handle return statements
            expression_tree = tree.children[0]
            return_type = self.analyze(expression_tree)
            print(expression_tree)
            print(self.scope_stack[-1])
            print(self.symbol_table[self.scope_stack[-1]])
            # Check if the return type matches the function's return type
            if return_type != self.symbol_table[self.scope_stack[-1]]['type']:
                print(f"Error: Return type '{return_type}' doesn't match the function's return type '{self.scope_stack[-1]}'.")
                return -1
            else:
                return return_type
            
        elif tree.data == "function_call_statement":
            # Extract function identifier and argument values
            function_identifier = tree.children[0].children[0]
            argument_values_tree = tree.children[1]
            print("function call", function_identifier )
            print(argument_values_tree)
            # Check if the function identifier exists
            if function_identifier not in self.symbol_table:
                print(f"Error: Function '{function_identifier}' is not defined.")
                return -1

            # Retrieve function information from symbol table
            function_info = self.symbol_table[function_identifier]
            print(function_info)
            # Check if the function has been defined
            
            # Retrieve function definition tree
            function_param = function_info["paramaters"]

            # Check if the number of arguments matches the number of parameters
            argument_count = len(argument_values_tree.children)
            parameter_count = len(function_param)
            if argument_count != parameter_count:
                print(f"Error: Function '{function_identifier}' expects {parameter_count} arguments, but {argument_count} were provided.")
                return -1

            # Analyze each argument expression and compare with parameter types
            for i in range(argument_count):
                argument_expression_tree = argument_values_tree.children[i]
                parameter_tree = function_param[i]
                parameter_type = parameter_tree.value
                argument_type = self.analyze(argument_expression_tree)
                if argument_type != parameter_type:
                    print(f"Error: Type mismatch in argument {i + 1} of function '{function_identifier}'. Expected type '{parameter_type}', but found '{argument_type}'.")
                    return -1

            # If the function has a return type, return it
            if "type" in function_info:
                return function_info["type"]
            else:
                return None

        elif tree.data == "tuple_statement":
            # Handle tuple declaration statement
            tuple_identifier = tree.children[0].children[0].value
            # Check if the tuple identifier is not already declared in the current scope
            if tuple_identifier in self.symbol_table and self.symbol_table[tuple_identifier]['scope'] == self.scope_stack[-1]:
                print(f"Error: Identifier '{tuple_identifier}' already declared in this scope.")
                return -1
            else:
                # Extract argument values and their types
                argument_values_tree = tree.children[1]
                tuple_elements = []
                for expression_tree in argument_values_tree.children:
                    element_type = self.analyze(expression_tree)
                    if element_type == -1:
                        return -1  # Error occurred, stop further processing
                    tuple_elements.append(element_type)
                # Add the tuple identifier to the symbol table with type 'tuple'
                self.symbol_table[tuple_identifier] = {'type': 'tuple', 'scope': self.scope_stack[-1], 'elements': tuple_elements}
                return "tuple"
        elif tree.data == "array_declaration":
            # Handle array declaration statement
            array_type = tree.children[0].children[0]
            array_identifier = tree.children[1].children[0].value
            array_size = tree.children[2].children[0].children[0].value 
            # Check if the array identifier is not already declared in the current scope
            if array_identifier in self.symbol_table and self.symbol_table[array_identifier]['scope'] == self.scope_stack[-1]:
                print(f"Error: Identifier '{array_identifier}' already declared in this scope.")
                return -1
            else:
                # Check if the array has been initialized with elements
                if len(tree.children) == 4:  # Array initialized with elements
                    # Extract argument values and their types
                    argument_values_tree = tree.children[3].children
                    array_elements = []
                    print(tree.children[3].children)
                    for expression_tree in argument_values_tree:
                        
                        element_type = self.analyze(expression_tree)
                        print("element" , element_type)

                        if element_type != array_type :
                            print(f"Error: type of elements isn't same with array {array_identifier} ") 
                            return -1  # Error occurred, stop further processing
                        array_elements.append(element_type)
                    # Add the array identifier to the symbol table with type 'array' and elements
                    self.symbol_table[array_identifier] = {'type': array_type, 'scope': self.scope_stack[-1], 'size': array_size}
                else:  # Array declaration without initialization
                    array_size_type = self.analyze(tree.children[2])
                    if array_size_type == "int":
                        self.symbol_table[array_identifier] = {'type': array_type, 'scope': self.scope_stack[-1], 'size': array_size}
                    else:
                        print("Error: Array size must be an integer.")
                        return -1
                return array_type

        elif tree.data == "array_operation_stms":
            # Extract identifier, index expression, and value expression
            identifier = tree.children[0].children[0]
            index_expression = tree.children[1]
            value_expression = tree.children[2]

            # Analyze index and value expressions
            index_type = self.analyze(index_expression)
            value_type = self.analyze(value_expression)
            print("array operation", index_type, value_type)
            print(self.symbol_table[identifier]['type'])
            # Check if the index expression evaluates to an integer
            if index_type != "int":
                print(f"Error: Array index must be an integer in statement '{tree}'.")
                return -1
            elif identifier not in self.symbol_table:
                print(f"Error: Array {identifier} hasn't been declared in this scope")
                return -1

            elif self.symbol_table[identifier]['type'] != value_type:
                print(f"Error: Array {identifier} type {self.symbol_table[identifier]['type']} can't take {value_type} type value")
                return -1

        elif tree.data == "string_ops_stms":
            # Extract identifier and operation details
            identifier = tree.children[0].children[0]
            operation_type = tree.children[1].children[1].data

            if operation_type == "concat":
                # For concat operation, ensure the identifier is a string
                if identifier in self.symbol_table and self.symbol_table[identifier]['type'] != "string":
                    print(f"Error: Identifier '{identifier}' must be of type string for concat operation.")
                    return -1
            elif operation_type == "slice":
                # For slice operation, ensure the identifier is a string
                if identifier in self.symbol_table and self.symbol_table[identifier]['type'] != "string":
                    print(f"Error: Identifier '{identifier}' must be of type string for slice operation.")
                    return -1
            else:
                print("Error: Invalid string operation type.")
                return -1

        elif tree.data == "expression":
            # Check the type of expression and return its type
            if tree.children[0].data == "identifier":
                # If it's an identifier, look it up in the symbol table
                print("expression-identifier")
                identifier = tree.children[0].children[0]
                if identifier in self.symbol_table:
                    return self.symbol_table[identifier]['type']
                else:
                    print(f"Error: Identifier '{identifier}' hasn't been declared.")
                    return -1
            elif tree.children[0].data == "integer":
                return "int"
            elif tree.children[0].data == "boolean":
                return "bool"
            elif tree.children[0].data == "string":
                return "string"
            elif tree.children[0].data == "unary_operation":
                # Perform type checking for unary operations
                identifier_tree = tree.children[0].children[0]
                output = self.analyze(identifier_tree)
                operator = tree.children[0].children[1].children[0]
                print("unary_operation",   identifier_tree, operator)

                # Perform type checking for unary operations and return the result type
                if operator == "++" or operator == "--":
                    if output == "int":
                        return "int"
                    else:
                        print("Error: Unary operation can only be performed on integer type.")
                        return -1
                else:
                    print("Error: Invalid unary operator.")
                    return -1
            elif tree.children[0].data == "binary_operation":
                # Perform type checking for binary operations
                operator = tree.children[0].children[1].children[0]
                left_operand_type = self.analyze(tree.children[0].children[0])
                right_operand_type = self.analyze(tree.children[0].children[2])
                print("binary_operation", operator, left_operand_type, right_operand_type)
                # Perform type checking for binary operations and return the result type
                if operator in ["+", "-", "*", "/", "%", "**"]:
                    if left_operand_type == "int" and right_operand_type == "int":
                        return "int"
                    else:
                        print("Error: Binary operation can only be performed on integer types.")
                        return -1
                elif operator in ["and", "or"]:
                    if left_operand_type == "bool" and right_operand_type == "bool":
                        return "bool"
                    else:
                        print("Error: Binary operation can only be performed on boolean types.")
                        return -1
                else:
                    print("Error: Invalid binary operator.")
                    return -1
            elif tree.children[0].data == "compare_operation":
                # Perform type checking for comparison operations
                operator = tree.children[0].children[1].children[0]
                left_operand_type = self.analyze(tree.children[0].children[0])
                right_operand_type = self.analyze(tree.children[0].children[2])
                print("compare_operation", operator, left_operand_type, right_operand_type)
                # Perform type checking for comparison operations and return the result type
                if operator in ["==", "!=", "<=", ">=", ">", "<"]:
                    if left_operand_type == right_operand_type:
                        return "bool"
                    else:
                        print("Error: Comparison operation can only be performed on operands of the same type.")
                        return -1
                else:
                    print("Error: Invalid comparison operator.")
                    return -1
            
            elif tree.children[0].data == "string_ops":
                operation_type = tree.children[0].children[1].data
                print("string", operation_type)
                if operation_type == "concat":
                    # For concat operation, expect two string identifiers
                    string1_identifier = tree.children[0].children[0].children[0]
                    string2_identifier = tree.children[0].children[2].children[0]
                    print(string1_identifier, string2_identifier)
                    # Check if both identifiers exist and are of type string
                    if string1_identifier in self.symbol_table and string2_identifier in self.symbol_table:
                        if self.symbol_table[string1_identifier]['type'] == "string" and self.symbol_table[string2_identifier]['type'] == "string":
                            return "string"
                        else:
                            print("Error: Concat operation expects two string operands.")
                            return -1
                    else:
                        print("Error: Identifier not found or not of type string.")
                        return -1
                elif operation_type == "slice":
                    # For slice operation, expect an integer index and length
                    start_index = self.analyze(tree.children[0].children[2])
                    length = self.analyze(tree.children[0].children[3])
                    string_identifier = tree.children[0].children[0].children[0].value 
                    print("string id", string_identifier)
                    print(start_index, length)
                    # Check if start index and length are integers
                    if string_identifier in self.symbol_table and self.symbol_table[string_identifier]['type'] == "string":
                        if start_index == "int" and length == "int":
                            return "string"
                        
                        else:
                            print("Error: Slice operation expects integer start index and length.")
                            return -1
                    else : 
                        print("Error: Identifier not found or not of type string.")
                        return -1
            elif tree.children[0].data == "tuple_operations":
                # Handle tuple operations
                tuple_identifier = tree.children[0].children[0].children[0]
                print("tuple_identifier")
                # Check if the tuple identifier exists and is of type tuple
                if tuple_identifier in self.symbol_table:
                    if self.symbol_table[tuple_identifier]['type'] == "tuple":
                        return "int"
                    else:
                        print(f"Error: Identifier '{tuple_identifier}' is not of type tuple.")
                        return -1
                else:
                    print(f"Error: Identifier '{tuple_identifier}' not found.")
                    return -1
            else:
                print("Error: Invalid string operation.")
                return -1



        else:
            # Recursively analyze child nodes
            for child in tree.children:
                print("else condition is called")
                self.analyze(child)

# Create a SemanticAnalyzer instance
semantic_analyzer = SemanticAnalyzer()

# Perform semantic analysis
output  = semantic_analyzer.analyze(tree)
print(output)
