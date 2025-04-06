class CodeGenerator:
    def __init__(self):
        self.indent_level = 0
        self.code_lines = []
        self.switch_counter = 0  # Used to generate unique names for switch temp variables

    def indent(self):
        return "    " * self.indent_level

    def generate(self, node):
        self.visit(node)
        return "\n".join(self.code_lines) + "\nif __name__ == '__main__':\n    kween()"

    def visit(self, node):
        method_name = "visit_" + node.__class__.__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        raise Exception(f"No visit_{node.__class__.__name__} method")

    # --- Statement Nodes ---

    def visit_ProgramNode(self, node):
        for stmt in node.statements:
            self.visit(stmt)

    def visit_FunctionDeclNode(self, node):
        # Create a Python function definition.
        params = ", ".join([p[0] for p in node.parameters])
        self.code_lines.append(f"def {node.name}({params}):")
        self.indent_level += 1
        if node.body is None or len(node.body) == 0:
            self.code_lines.append(self.indent() + "pass")
        else:
            for stmt in node.body:
                self.visit(stmt)
        self.indent_level -= 1
        self.code_lines.append("")  # Blank line after function

    def visit_VarDeclNode(self, node):
        # In Python, variables are dynamically typed.
        # But for 'anda' and 'andamhie', we enforce conversion.
        expr_code = self.visit(node.initializer) if node.initializer is not None else None
        if expr_code is None:
            # If no initializer, assign a default value.
            if node.data_type in ['anda', 'andamhie']:
                expr_code = "0"
            elif node.data_type == 'eklabool':
                expr_code = "False"
            elif node.data_type == 'chika':
                expr_code = '""'
            else:
                expr_code = "None"
        if node.data_type == 'anda':
            code = f"{node.name} = int({expr_code})"
        elif node.data_type == 'andamhie':
            code = f"{node.name} = float({expr_code})"
        else:
            code = f"{node.name} = {expr_code}"
        self.code_lines.append(self.indent() + code)

    def visit_AssignmentNode(self, node):
        left = node.identifier
        right = self.visit(node.expression)
        # For augmented assignment, use the same operator.
        self.code_lines.append(self.indent() + f"{left} {node.operator} {right}")

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
        for stmt in node.then_block:
            self.visit(stmt)
        self.indent_level -= 1
        for cond, block in node.else_if_blocks:
            cond_code = self.visit(cond)
            self.code_lines.append(self.indent() + f"elif {cond_code}:")
            self.indent_level += 1
            for stmt in block:
                self.visit(stmt)
            self.indent_level -= 1
        if node.else_block is not None:
            self.code_lines.append(self.indent() + "else:")
            self.indent_level += 1
            for stmt in node.else_block:
                self.visit(stmt)
            self.indent_level -= 1

    def visit_WhileNode(self, node):
        condition = self.visit(node.condition)
        self.code_lines.append(self.indent() + f"while {condition}:")
        self.indent_level += 1
        for stmt in node.body:
            self.visit(stmt)
        self.indent_level -= 1

    def visit_DoWhileNode(self, node):
        self.code_lines.append(self.indent() + "while True:")
        self.indent_level += 1
        for stmt in node.body:
            self.visit(stmt)
        cond = self.visit(node.condition)
        self.code_lines.append(self.indent() + f"if not ({cond}):")
        self.indent_level += 1
        self.code_lines.append(self.indent() + "break")
        self.indent_level -= 2

    def visit_ForNode(self, node):
        start = self.visit(node.start_expr)
        end = self.visit(node.end_expr)
        step = self.visit(node.step_expr) if node.step_expr is not None else "1"
        # Assuming "to" is inclusive; hence, end+1 in range.
        self.code_lines.append(self.indent() + f"for {node.loop_var} in range({start}, ({end})+1, {step}):")
        self.indent_level += 1
        for stmt in node.body:
            self.visit(stmt)
        self.indent_level -= 1

    def visit_SwitchNode(self, node):
        # Generate a unique temporary variable name.
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
            for stmt in stmts:
                self.visit(stmt)
            self.indent_level -= 1
            first = False
        if node.default_case is not None:
            self.code_lines.append(self.indent() + "else:")
            self.indent_level += 1
            for stmt in node.default_case:
                self.visit(stmt)
            self.indent_level -= 1

    def visit_BlockNode(self, node):
        for stmt in node.statements:
            self.visit(stmt)

    # --- Expression Nodes ---

    def visit_LiteralNode(self, node):
        # For string literals, add quotes.
        if node.literal_type == 'chika':
            return f'{node.value}'
        return str(node.value)

    def visit_IdentifierNode(self, node):
        return node.name

    def visit_BinaryOpNode(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)
        op = node.operator
        if op == '&&':
            op = 'and'
        elif op == '||':
            op = 'or'
        return f"({left} {op} {right})"

    def visit_UnaryOpNode(self, node):
        operand = self.visit(node.operand)
        op = node.operator
        # Handle logical not
        if op == '!':
            return f"(not {operand})"
        # Handle increment/decrement operators:
        # Here we simply translate prefix ++/-- to (x + 1) or (x - 1) for simplicity.
        if op == '++':
            return f"({operand} + 1)"
        if op == '--':
            return f"({operand} - 1)"
        # For postfix, assume similar treatment.
        return f"({op}{operand})"

    def visit_ArrayAccessNode(self, node):
        array_code = self.visit(node.array)
        # For each index expression, add indexing.
        for index_expr in node.index_exprs:
            idx = self.visit(index_expr)
            array_code += f"[{idx}]"
        return array_code

    def visit_InputCallNode(self, node):
        # Transpile to Python's input() function.
        return f"input({repr(node.prompt)})"


# Helper function to generate code from an AST
def generate_code(ast):
    generator = CodeGenerator()
    return generator.generate(ast)


# Example usage (commented out):
# from ast_generator import ASTGenerator
# tokens = [ ... ]  # Your token stream here.
# ast = ASTGenerator(tokens).generate()
# python_code = generate_code(ast)
# print(python_code)
