import astclasses

class WATGenerator:
    def __init__(self):
        self.module_name = "js"  # Assuming JavaScript module for external functions

    def generate_wat(self, ast):
        wat_code = "(module\n"
        # Import log function for preach statements
        wat_code += f'  (import "{self.module_name}" "log" (func $log (param i32)))\n'
        wat_code += self.generate_code(ast)
        wat_code += ")\n"
        return wat_code

    def generate_code(self, node):
        if isinstance(node, astclasses.Program):
            return self.handle_program(node)
        return ""

    def handle_program(self, program_node):
        return "\n".join(self.generate_code(stmt) for stmt in program_node.statements)

    def handle_variable_declaration(self, var_decl):
        # Assuming simplified local variable handling (integers only)
        var_name = var_decl.assignment_expression.left.value
        var_value = var_decl.assignment_expression.right.value
        return f"(local ${var_name} i32)\n(set_local ${var_name} (i32.const {var_value}))"

    def handle_conditional_statement(self, if_stmt):
        condition_code = self.generate_code_for_expression(if_stmt.condition)
        then_code = "\n".join(self.generate_code(stmt) for stmt in if_stmt.true_branch.statements)
        else_code = "\n".join(self.generate_code(stmt) for stmt in if_stmt.false_branch.statements)
        return f"(if {condition_code}\n  (then\n{then_code}  )\n  (else\n{else_code}  ))"

    def generate_code_for_expression(self, expr):
        if isinstance(expr, astclasses.BinaryExpression):
            left_code = f"local.get ${expr.left.value}"
            right_code = f"i32.const {expr.right.value}"
            op_code = {
                '>': 'i32.gt_s',
                '<': 'i32.lt_s',
                '==': 'i32.eq',
                '!=': 'i32.ne',
                '+': 'i32.add',
                '-': 'i32.sub',
                '*': 'i32.mul',
                '/': 'i32.div_s',
                '%': 'i32.rem_s'
            }[expr.operator]
            return f"({op_code} {left_code} {right_code})"
        return ""

    def handle_preach_statement(self, preach_stmt):
        # Assuming we map messages to integer indexes
        message_index = {
            "x is positive": 1,
            "x is not positive": 2
        }[preach_stmt.expression.value]
        return f"(call $log (i32.const {message_index}))"

if __name__ == "__main__":
    # Example usage
    generator = WATGenerator()
    # Construct an AST node manually for demonstration purposes
    ast = astclasses.Program([
        astclasses.VariableDeclaration(
            declaration_specifier=None,
            assignment_expression=astclasses.BinaryExpression(
                left=astclasses.Identifier(value='x'),
                operator='=',
                right=astclasses.IntegerLiteral(value=10)
            )
        ),
        astclasses.IfStatement(
            condition=astclasses.BinaryExpression(
                left=astclasses.Identifier(value='x'),
                operator='>',
                right=astclasses.IntegerLiteral(value=6)
            ),
            true_branch=[astclasses.PreachStatement(expression=astclasses.StringLiteral(value="x is positive"))],
            false_branch=[astclasses.PreachStatement(expression=astclasses.StringLiteral(value="x is not positive"))]
        )
    ])
    print(generator.generate_wat(ast))


# -------------------------------------------------------------------------------
# import astclasses
# # print(dir(astclasses))  # This will print all names defined in the module

# class WATGenerator:
#     def generate_wat(self, ast):
#         # Start with module declaration
#         wat_code = "(module\n"
#         wat_code += self.generate_code(ast)
#         wat_code += ")\n"
#         return wat_code

#     def generate_code(self, node):
#         if isinstance(node, astclasses.Program):
#             return self.handle_program(node)
#         elif isinstance(node, astclasses.FunctionDefinition):
#             return self.handle_function(node)
#         elif isinstance(node, astclasses.VariableDeclaration):
#             return self.handle_variable_declaration(node)
#         elif isinstance(node, astclasses.BinaryExpression) and node.operator == '=':
#             return self.handle_assignment(node)
#         elif isinstance(node, astclasses.IfStatement):
#             return self.handle_conditional_statement(node)
#         elif isinstance(node, astclasses.JumpStatement):  # Update this line
#             return self.handle_jump_statement(node)  # Ensure there is a method that correctly handles this
#         # Continue with other conditions
#         return ""





#     def handle_program(self, program_node):
#         # Combine code for all elements in the program
#         return "\n".join(self.generate_code(stmt) for stmt in program_node.statements)

#     def handle_function(self, function_node):
#         # Start function definition
#         params = " ".join(f"(param ${param.name} i32)" for param in function_node.parameters)
#         locals_ = " ".join(f"(local ${var_decl.assignment_expression.left.value} i32)" 
#                             for stmt in function_node.body.statements 
#                             if isinstance(stmt, astclasses.VariableDeclaration))
#         body_code = "\n".join(self.generate_code(stmt) for stmt in function_node.body.statements
#                             if not isinstance(stmt, astclasses.VariableDeclaration))
#         code = f"(func ${function_node.name} {params}\n{locals_}\n{body_code}\n)\n"
#         return code


#     def handle_variable_declaration(self, var_decl):
#         # Assuming var_decl has attributes 'identifier' and 'type_specifier' appropriately
#         var_name = var_decl.assignment_expression.left.value
#         var_type = var_decl.declaration_specifier.type_specifier.type_keyword  # This maps to 'i32', 'f32', etc.
#         wasm_type = 'i32'  # Simplified mapping, assuming all variables are 'i32' for this example
        
#         # Declare local variable
#         declaration = f"(local ${var_name} {wasm_type})\n"
        
#         # Assume we can also handle the assignment part right after declaration
#         # This needs the assignment expression to be compiled into WAT, which is a separate task
#         value_code = self.generate_code_for_expression(var_decl.assignment_expression.right)
#         assignment = f"(set_local ${var_name} {value_code})\n"
        
#         # return declaration + assignment
#         return ""



#     def handle_assignment(self, node):
#         left_code = self.generate_code(node.left)  # Assuming `node.left` holds the variable being assigned to
#         right_code = self.generate_code(node.right)  # The expression/value being assigned
#         return f"(set_local ${left_code} {right_code})\n"  # Adjust based on how variables are referenced in WAT

#     def handle_conditional_statement(self, if_stmt):
#         condition_code = self.generate_code_for_expression(if_stmt.condition)
#         then_code = "\n".join(self.generate_code(stmt) for stmt in if_stmt.true_branch.statements)
#         else_code = "\n".join(self.generate_code(stmt) for stmt in if_stmt.false_branch.statements) if if_stmt.false_branch else ""
#         return f"(if {condition_code}\n(then\n{then_code}\n)\n(else\n{else_code}\n)\n)"


#     def handle_return_statement(self, return_stmt):
#         # Handle a return statement, assuming it returns an integer for simplicity
#         return_value_code = self.generate_code(return_stmt.expression)
#         return f"(return {return_value_code})\n"

#     def handle_jump_statement(self, jump_stmt):
#         # This method needs to correctly generate WAT code for the return operation
#         # Assuming `jump_stmt` has attributes to determine its type (like 'return')
#         if jump_stmt.operation == 'return':
#             return_code = self.generate_code(jump_stmt.value)  # Assuming 'value' holds the expression to return
#             return f"(return {return_code})\n"

#     # Example for handling expressions and literals
#     def generate_code_for_expression(self, expr):
#         if isinstance(expr, astclasses.Identifier):
#             return f"(local.get ${expr.value})"
#         elif isinstance(expr, astclasses.IntegerLiteral):
#             return f"(i32.const {expr.value})"
#         elif isinstance(expr, astclasses.BinaryExpression):
#             left_code = self.generate_code_for_expression(expr.left)
#             right_code = self.generate_code_for_expression(expr.right)
#             operator = {
#                 '>': 'i32.gt_s',
#                 '<': 'i32.lt_s',
#                 '==': 'i32.eq',
#                 '!=': 'i32.ne',
#                 '+': 'i32.add',
#                 '-': 'i32.sub',
#                 '*': 'i32.mul',
#                 '/': 'i32.div_s',  # Ensure division by zero is handled elsewhere
#                 '%': 'i32.rem_s'
#             }.get(expr.operator, '')
#             return f"({operator} {left_code} {right_code})"
#         # Add additional expression types as necessary

#     def handle_preach_statement(self, preach_stmt):
#         message = preach_stmt.expression  # Assuming this expression results in a string or number
#         message_code = self.generate_code_for_expression(message)
#         return f"(call $log {message_code})"
    
# # Example implementation might require adjustments based on the actual structure of astclasses and the specifics of WAT.
