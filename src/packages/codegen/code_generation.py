class CodeGenerator:
    def __init__(self):
        self.indent_level = 0
        self.code_lines = []
        self.switch_counter = 0  # Used to generate unique names for switch temp variables
        self.for_counter = 0     # Used to generate unique names for for loop helper variables
        self.symbol_stack = [{}]  # Stack to maintain scopes for variable types

    def indent(self):
        return "    " * self.indent_level

    def current_scope(self):
        return self.symbol_stack[-1]

    def push_scope(self):
        self.symbol_stack.append({})

    def pop_scope(self):
        self.symbol_stack.pop()

    def lookup_variable(self, var_name):
        for scope in reversed(self.symbol_stack):
            if var_name in scope:
                return scope[var_name]
        return None

    def emit_helper_functions(self):
        # Emit a helper to truncate andamhie (float) values to 6 decimals.
        self.code_lines.append("""def truncate_andamhie_acclang_specific(value):
    import math
    return math.trunc(value * 1000000) / 1000000
""")
        # Updated type checking function for our custom types.
        self.code_lines.append("""def check_type_acclang_specific(expected, value):
    if expected == 'anda':
        try:
            return int(value)
        except ValueError:
            try:
                return int(float(value))
            except ValueError:
                raise TypeError("Type error: expected numeric value for type 'anda'")
    elif expected == 'andamhie':
        try:
            f = float(value)
            import math
            return math.trunc(f * 1000000) / 1000000
        except ValueError:
            try:
                f = float(int(value))
                import math
                return math.trunc(f * 1000000) / 1000000
            except ValueError:
                raise TypeError("Type error: expected numeric value for type 'andamhie'")
    elif expected == 'eklabool':
        try:
            return False if int(value) == 0 else True
        except ValueError:
            try:
                return False if float(value) == 0.0 else True
            except ValueError:
                if isinstance(value, str):
                    return True
                else:
                    raise TypeError("Type error: expected numeric or string value for type 'eklabool'")
    elif expected == 'chika':
        if isinstance(value, str):
            return value
        else:
            raise TypeError("Type error: expected string value for type 'chika'")
    else:
        return value
""")
        self.code_lines.append("""def check_array_type_acclang_specific(expected, arr):
    if isinstance(arr, list):
        return [check_array_type_acclang_specific(expected, x) for x in arr]
    else:
        return check_type_acclang_specific(expected, arr)
""")

    def generate(self, node):
        self.emit_helper_functions()
        self.visit(node)
        self.code_lines.append("if __name__ == '__main__':")
        self.code_lines.append("    kween()")
        return "\n".join(self.code_lines) + "\n"

    def visit(self, node):
        # Handle lists (used in array initializers) separately.
        if isinstance(node, list):
            return self.visit_list(node)
        method_name = "visit_" + node.__class__.__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def visit_list(self, lst):
        # Recursively process lists to output a Python list literal.
        elements = []
        for item in lst:
            if isinstance(item, list):
                elements.append(self.visit_list(item))
            else:
                elements.append(self.visit(item))
        return "[" + ", ".join(elements) + "]"

    def generic_visit(self, node):
        raise Exception(f"No visit_{node.__class__.__name__} method")

    # --- Statement Nodes ---

    def visit_ProgramNode(self, node):
        for stmt in node.statements:
            self.visit(stmt)

    def visit_FunctionDeclNode(self, node):
        params = ", ".join([p[0] for p in node.parameters])
        self.code_lines.append(f"def {node.name}({params}):")
        self.indent_level += 1
        self.push_scope()
        for param_name, param_type in node.parameters:
            self.current_scope()[param_name] = param_type
        if node.body is None or len(node.body) == 0:
            self.code_lines.append(self.indent() + "pass")
        else:
            for stmt in node.body:
                self.visit(stmt)
        self.pop_scope()
        self.indent_level -= 1
        self.code_lines.append("")

    def visit_VarDeclNode(self, node):
        if isinstance(node.initializer, list):
            expr_code = self.visit_list(node.initializer)
            code = f"{node.name} = check_array_type_acclang_specific('{node.data_type}', {expr_code})"
        else:
            expr_code = self.visit(node.initializer) if node.initializer is not None else None
            if expr_code is None:
                if node.data_type in ['anda', 'andamhie']:
                    expr_code = "0"
                elif node.data_type == 'eklabool':
                    expr_code = "False"
                elif node.data_type == 'chika':
                    expr_code = '""'
                else:
                    expr_code = "None"
            expr_code = f"check_type_acclang_specific('{node.data_type}', {expr_code})"
            code = f"{node.name} = {expr_code}"
    
        self.code_lines.append(self.indent() + code)
        self.current_scope()[node.name] = node.data_type

    def visit_AssignmentNode(self, node):
        var_type = self.lookup_variable(node.identifier)
        right = self.visit(node.expression)
        if var_type is None:
            self.code_lines.append(self.indent() + f"{node.identifier} {node.operator} {right}")
        else:
            if node.operator == "=":
                self.code_lines.append(self.indent() + f"{node.identifier} = check_type_acclang_specific('{var_type}', {right})")
            else:
                op_map = {"+=": "+", "-=": "-", "*=": "*", "/=": "/", "%=": "%", "**=": "**", "//=": "//"}
                bin_op = op_map.get(node.operator, node.operator)
                self.code_lines.append(self.indent() + f"{node.identifier} = {node.identifier} {bin_op} check_type_acclang_specific('{var_type}', {right})")

    def visit_FunctionCallNode(self, node):
        args = ", ".join([self.visit(arg) for arg in node.arguments])
        return f"{node.name}({args})"

    def visit_ReturnNode(self, node):
        if node.expression is not None:
            expr_code = self.visit(node.expression)
            self.code_lines.append(self.indent() + f"return {expr_code}")
        else:
            self.code_lines.append(self.indent() + "return")

    def visit_PrintNode(self, node):
        expr_code = self.visit(node.expression)
        self.code_lines.append(self.indent() + f"print({expr_code})")

    def visit_IfNode(self, node):
        condition = self.visit(node.condition)
        self.code_lines.append(self.indent() + f"if {condition}:")
        self.indent_level += 1
        self.push_scope()
        for stmt in node.then_block:
            self.visit(stmt)
        self.pop_scope()
        self.indent_level -= 1
        for cond, block in node.else_if_blocks:
            cond_code = self.visit(cond)
            self.code_lines.append(self.indent() + f"elif {cond_code}:")
            self.indent_level += 1
            self.push_scope()
            for stmt in block:
                self.visit(stmt)
            self.pop_scope()
            self.indent_level -= 1
        if node.else_block is not None:
            self.code_lines.append(self.indent() + "else:")
            self.indent_level += 1
            self.push_scope()
            for stmt in node.else_block:
                self.visit(stmt)
            self.pop_scope()
            self.indent_level -= 1

    def visit_WhileNode(self, node):
        condition = self.visit(node.condition)
        self.code_lines.append(self.indent() + f"while {condition}:")
        self.indent_level += 1
        self.push_scope()
        for stmt in node.body:
            self.visit(stmt)
        self.pop_scope()
        self.indent_level -= 1

    def visit_DoWhileNode(self, node):
        self.code_lines.append(self.indent() + "while True:")
        self.indent_level += 1
        self.push_scope()
        for stmt in node.body:
            self.visit(stmt)
        self.pop_scope()
        cond = self.visit(node.condition)
        self.code_lines.append(self.indent() + f"if not ({cond}):")
        self.indent_level += 1
        self.code_lines.append(self.indent() + "break")
        self.indent_level -= 2

    def visit_ForNode(self, node):
        for_index = self.for_counter
        self.for_counter += 1
        start_expr = self.visit(node.start_expr)
        end_expr = self.visit(node.end_expr)
        step_expr = self.visit(node.step_expr) if node.step_expr is not None else "1"
        start_var = f"start_val_{for_index}"
        end_var = f"end_val_{for_index}"
        step_var = f"step_val_{for_index}"
        bound_var = f"end_bound_{for_index}"
        self.code_lines.append(self.indent() + f"{start_var} = {start_expr}")
        self.code_lines.append(self.indent() + f"{end_var} = {end_expr}")
        self.code_lines.append(self.indent() + f"{step_var} = {step_expr}")
        self.code_lines.append(self.indent() + f"if {step_var} > 0:")
        self.indent_level += 1
        self.code_lines.append(self.indent() + f"{bound_var} = {end_var} + 1")
        self.indent_level -= 1
        self.code_lines.append(self.indent() + "else:")
        self.indent_level += 1
        self.code_lines.append(self.indent() + f"{bound_var} = {end_var} - 1")
        self.indent_level -= 1
        self.code_lines.append(self.indent() + f"for {node.loop_var} in range({start_var}, {bound_var}, {step_var}):")
        self.indent_level += 1
        self.push_scope()
        if node.new_declaration and node.var_type:
            self.current_scope()[node.loop_var] = node.var_type
        for stmt in node.body:
            self.visit(stmt)
        self.pop_scope()
        self.indent_level -= 1

    def visit_SwitchNode(self, node):
        temp_var = f"switch_value_{self.switch_counter}"
        self.switch_counter += 1
        expr = self.visit(node.expression)
        self.code_lines.append(self.indent() + f"{temp_var} = {expr}")
        first = True
        for case_expr, stmts in node.cases:
            prefix = "if" if first else "elif"
            case_code = self.visit(case_expr)
            self.code_lines.append(self.indent() + f"{prefix} {temp_var} == {case_code}:")
            self.indent_level += 1
            self.push_scope()
            for stmt in stmts:
                self.visit(stmt)
            self.pop_scope()
            self.indent_level -= 1
            first = False
        if node.default_case is not None:
            self.code_lines.append(self.indent() + "else:")
            self.indent_level += 1
            self.push_scope()
            for stmt in node.default_case:
                self.visit(stmt)
            self.pop_scope()
            self.indent_level -= 1

    def visit_BlockNode(self, node):
        self.push_scope()
        for stmt in node.statements:
            self.visit(stmt)
        self.pop_scope()

    # --- Expression Nodes ---

    def visit_LiteralNode(self, node):
        # For string literals, return as is.
        if node.literal_type == 'chika':
            return f'{node.value}'
        # For numeric literals, let the type conversion (and possible truncation) occur later.
        return str(node.value)

    def visit_IdentifierNode(self, node):
        return node.name

    def visit_BinaryOpNode(self, node):
        # Handle the '+' operator separately to account for potential string concatenation.
        if node.operator == '+':
            left_code = self.visit(node.left)
            right_code = self.visit(node.right)
            left_type = self.infer_type(node.left)
            right_type = self.infer_type(node.right)
            if left_type == 'chika' or right_type == 'chika':
                if left_type == 'chika' and right_type != 'chika':
                    right_code = f"str({right_code})"
                elif right_type == 'chika' and left_type != 'chika':
                    left_code = f"str({left_code})"
                return f"({left_code} + {right_code})"
            else:
                expr = f"({left_code} + {right_code})"
                result_type = self.infer_type(node)
                if result_type == 'andamhie':
                    return f"truncate_andamhie_acclang_specific({expr})"
                return expr
        else:
            left = self.visit(node.left)
            right = self.visit(node.right)
            op = node.operator
            if op == '&&':
                op = 'and'
            elif op == '||':
                op = 'or'
            expr = f"({left} {op} {right})"
            # For arithmetic operators, if the inferred type is andamhie, apply truncation.
            if node.operator in ['-', '*', '/', '%', '**', '//']:
                result_type = self.infer_type(node)
                if result_type == 'andamhie':
                    return f"truncate_andamhie_acclang_specific({expr})"
            return expr

    def visit_UnaryOpNode(self, node):
        operand = self.visit(node.operand)
        op = node.operator
        if op == '!':
            return f"(not {operand})"
        if op == '++':
            return f"({operand} + 1)"
        if op == '--':
            return f"({operand} - 1)"
        return f"({op}{operand})"

    def visit_ArrayAccessNode(self, node):
        array_code = self.visit(node.array)
        for index_expr in node.index_exprs:
            idx = self.visit(index_expr)
            array_code += f"[{idx}]"
        return array_code

    def visit_InputCallNode(self, node):
        return f"input({repr(node.prompt)})"

    # --- Helper method to infer expression types ---

    def infer_type(self, node):
        if hasattr(node, 'literal_type'):
            return node.literal_type
        if hasattr(node, 'name'):
            var_type = self.lookup_variable(node.name)
            if var_type is not None:
                return var_type
        if hasattr(node, 'operator'):
            if node.operator == '+':
                left_type = self.infer_type(node.left)
                right_type = self.infer_type(node.right)
                if left_type == 'chika' or right_type == 'chika':
                    return 'chika'
                if left_type == 'andamhie' or right_type == 'andamhie':
                    return 'andamhie'
                return 'anda'
            elif node.operator in ['-', '*', '/', '%', '**', '//']:
                left_type = self.infer_type(node.left)
                right_type = self.infer_type(node.right)
                if left_type == 'andamhie' or right_type == 'andamhie':
                    return 'andamhie'
                return 'anda'
            elif node.operator in ['&&', '||']:
                return 'eklabool'
        if hasattr(node, 'operator') and hasattr(node, 'operand'):
            if node.operator == '!':
                return 'eklabool'
            return self.infer_type(node.operand)
        return None

def generate_code(ast):
    generator = CodeGenerator()
    return generator.generate(ast)

# Example usage (commented out):
# from ast_generator import ASTGenerator
# tokens = [ ... ]  # Your token stream here.
# ast = ASTGenerator(tokens).generate()
# python_code = generate_code(ast)
# print(python_code)
