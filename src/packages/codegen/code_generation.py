from .ast_generator import UnaryOpNode, IdentifierNode

# code_generation.py

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
        # Helper to catch use-before-init errors
        self.code_lines.append("""def _cNone_(value, name):
    if value is None:
        raise NameError(f"Runtime error: variable '{name}' used before initialization")
    return value
""")
        # Updated type checking with clamping for anda/andamhie
        self.code_lines.append("""def _cType_(expected, value):
    if expected == 'anda':
        try:
            v = int(value)
        except Exception:
            try:
                v = int(float(value))
            except Exception:
                raise TypeError("Type error: expected numeric value for type 'anda'")
        if v > 9999999999:
            v = 9999999999
        if v < -9999999999:
            v = -9999999999
        return v
    elif expected == 'andamhie':
        try:
            f = float(value)
        except Exception:
            try:
                f = float(int(value))
            except Exception:
                raise TypeError("Type error: expected numeric value for type 'andamhie'")
        import math
        f = math.trunc(f * 1000000) / 1000000
        if f > 9999999999.999999:
            f = 9999999999.999999
        if f < -9999999999:
            f = -9999999999.999999
        return f
    elif expected == 'eklabool':
        try:
            return False if int(value) == 0 else True
        except Exception:
            try:
                return False if float(value) == 0.0 else True
            except Exception:
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
        # Array type checker
        self.code_lines.append("""def _cArray_(expected, arr):
    if isinstance(arr, list):
        return [_cArray_(expected, x) for x in arr]
    else:
        return _cType_(expected, arr)
""")

    def generate(self, node):
        self.emit_helper_functions()
        self.visit(node)
        self.code_lines.append("if __name__ == '__main__':")
        self.code_lines.append("    kween()")
        return "\n".join(self.code_lines) + "\n"

    def visit(self, node):
        if isinstance(node, list):
            return self.visit_list(node)
        method_name = "visit_" + node.__class__.__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def visit_list(self, lst):
        elements = []
        for item in lst:
            if isinstance(item, list):
                elements.append(self.visit_list(item))
            else:
                elements.append(self.visit(item))
        return "[" + ", ".join(elements) + "]"

    def generic_visit(self, node):
        raise Exception(f"No visit_{node.__class__.__name__} method")

    def emit_statement(self, node):
        if node.__class__.__name__ == "FunctionCallNode":
            self.code_lines.append(self.indent() + self.visit(node))
        else:
            self.visit(node)

    def emit_statements(self, statements):
        for stmt in statements:
            self.emit_statement(stmt)

    def visit_ProgramNode(self, node):
        self.emit_statements(node.statements)

    def visit_FunctionDeclNode(self, node):
        params = ", ".join([p[0] for p in node.parameters])
        self.code_lines.append(f"def {node.name}({params}):")
        self.indent_level += 1
        self.push_scope()
        for param_name, param_type in node.parameters:
            self.current_scope()[param_name] = param_type
        if not node.body:
            self.code_lines.append(self.indent() + "pass")
        else:
            self.emit_statements(node.body)
        self.pop_scope()
        self.indent_level -= 1
        self.code_lines.append("")

    def visit_VarDeclNode(self, node):
        # Handle pre-/post-increment/decrement in initializer
        init = node.initializer
        if hasattr(init, 'operator') and init.operator in ['++', '--']:
            op_symbol = '+' if init.operator == '++' else '-'
            # operand may be IdentifierNode or expression
            operand = init.operand
            if isinstance(operand, IdentifierNode):
                var = operand.name
            else:
                var = self.visit(operand)
            # determine type for operand update
            update_type = self.lookup_variable(var)
            # prefix: update then assign
            if not getattr(init, 'is_postfix', False):
                if update_type:
                    self.code_lines.append(
                        self.indent() +
                        f"{var} = _cType_('{update_type}', {var} {op_symbol} 1)"
                    )
                else:
                    self.code_lines.append(
                        self.indent() + f"{var} = {var} {op_symbol} 1"
                    )
                # assign to new var
                self.code_lines.append(
                    self.indent() + f"{node.name} = _cType_('{node.data_type}', {var})"
                )
            else:
                # postfix: assign original, then update
                self.code_lines.append(
                    self.indent() + f"{node.name} = _cType_('{node.data_type}', {var})"
                )
                if update_type:
                    self.code_lines.append(
                        self.indent() +
                        f"{var} = _cType_('{update_type}', {var} {op_symbol} 1)"
                    )
                else:
                    self.code_lines.append(
                        self.indent() + f"{var} = {var} {op_symbol} 1"
                    )
            # record the declared type
            self.current_scope()[node.name] = node.data_type
            return

        # Original variable declaration handling
        if node.initializer is None:
            code = f"{node.name} = None"
        else:
            if isinstance(node.initializer, list):
                expr_code = self.visit_list(node.initializer)
                code = (f"{node.name} = "
                        f"_cArray_('{node.data_type}', {expr_code})")
            else:
                expr = self.visit(node.initializer)
                expr = f"_cType_('{node.data_type}', {expr})"
                code = f"{node.name} = {expr}"
        self.code_lines.append(self.indent() + code)
        self.current_scope()[node.name] = node.data_type

    def visit_AssignmentNode(self, node):
        # Handle pre-/post-increment/decrement in assignment expression
        expr = node.expression
        if node.operator == '=' and hasattr(expr, 'operator') and expr.operator in ['++', '--']:
            op_symbol = '+' if expr.operator == '++' else '-'
            operand = expr.operand
            if isinstance(operand, IdentifierNode):
                var = operand.name
            else:
                var = self.visit(operand)
            update_type = self.lookup_variable(var)
            # prefix
            if not getattr(expr, 'is_postfix', False):
                if update_type:
                    self.code_lines.append(
                        self.indent() +
                        f"{var} = _cType_('{update_type}', {var} {op_symbol} 1)"
                    )
                else:
                    self.code_lines.append(
                        self.indent() + f"{var} = {var} {op_symbol} 1"
                    )
                self.code_lines.append(
                    self.indent() + f"{node.identifier} = _cType_('{update_type}', {var})"
                )
            else:
                # postfix
                self.code_lines.append(
                    self.indent() + f"{node.identifier} = _cType_('{update_type}', {var})"
                )
                if update_type:
                    self.code_lines.append(
                        self.indent() +
                        f"{var} = _cType_('{update_type}', {var} {op_symbol} 1)"
                    )
                else:
                    self.code_lines.append(
                        self.indent() + f"{var} = {var} {op_symbol} 1"
                    )
            return

        var_type = self.lookup_variable(node.identifier)
        right = self.visit(node.expression)
        if var_type is None or node.operator == "=":
            if var_type:
                self.code_lines.append(
                    self.indent() +
                    f"{node.identifier} = _cType_('{var_type}', {right})"
                )
            else:
                self.code_lines.append(self.indent() + f"{node.identifier} {node.operator} {right}")
        else:
            op_map = {"+=": "+", "-=": "-", "*=": "*", "/=": "/", "%=": "%", "**=": "**", "//=": "//"}
            bin_op = op_map.get(node.operator, node.operator)
            full = (
                f"_cType_("
                f"'{var_type}', {node.identifier} {bin_op} _cType_('{var_type}', {right})"
                f")"
            )
            self.code_lines.append(self.indent() + f"{node.identifier} = {full}")

    def visit_FunctionCallNode(self, node):
        args = ", ".join(self.visit(arg) for arg in node.arguments)
        return f"{node.name}({args})"

    def visit_ReturnNode(self, node):
        if node.expression is not None:
            self.code_lines.append(self.indent() + f"return {self.visit(node.expression)}")
        else:
            self.code_lines.append(self.indent() + "return")

    def visit_PrintNode(self, node):
        # Wrap the expression use with check_none
        expr = self.visit(node.expression)
        self.code_lines.append(self.indent() + f"print({expr}, end='')")

    def visit_IfNode(self, node):
        self.code_lines.append(self.indent() + f"if {self.visit(node.condition)}:")
        self.indent_level += 1
        self.push_scope()
        self.emit_statements(node.then_block)
        self.pop_scope()
        self.indent_level -= 1
        for cond, blk in node.else_if_blocks:
            self.code_lines.append(self.indent() + f"elif {self.visit(cond)}:")
            self.indent_level += 1
            self.push_scope()
            self.emit_statements(blk)
            self.pop_scope()
            self.indent_level -= 1
        if node.else_block is not None:
            self.code_lines.append(self.indent() + "else:")
            self.indent_level += 1
            self.push_scope()
            self.emit_statements(node.else_block)
            self.pop_scope()
            self.indent_level -= 1

    def visit_WhileNode(self, node):
        self.code_lines.append(self.indent() + f"while {self.visit(node.condition)}:")
        self.indent_level += 1
        self.push_scope()
        self.emit_statements(node.body)
        self.pop_scope()
        self.indent_level -= 1

    def visit_DoWhileNode(self, node):
        self.code_lines.append(self.indent() + "while True:")
        self.indent_level += 1
        self.push_scope()
        self.emit_statements(node.body)
        self.pop_scope()
        cond = self.visit(node.condition)
        self.code_lines.append(self.indent() + f"if not ({cond}):")
        self.indent_level += 1
        self.code_lines.append(self.indent() + "break")
        self.indent_level -= 2

    def visit_ForNode(self, node):
        idx = self.for_counter
        self.for_counter += 1
        s = self.visit(node.start_expr)
        e = self.visit(node.end_expr)
        st = self.visit(node.step_expr) if node.step_expr is not None else "1"
        sv = f"start_val_{idx}"
        ev = f"end_val_{idx}"
        tv = f"step_val_{idx}"
        bv = f"end_bound_{idx}"
        self.code_lines.append(self.indent() + f"{sv} = {s}")
        self.code_lines.append(self.indent() + f"{ev} = {e}")
        self.code_lines.append(self.indent() + f"{tv} = {st}")
        self.code_lines.append(self.indent() + f"if {tv} > 0:")
        self.indent_level += 1
        self.code_lines.append(self.indent() + f"{bv} = {ev} + 1")
        self.indent_level -= 1
        self.code_lines.append(self.indent() + "else:")
        self.indent_level += 1
        self.code_lines.append(self.indent() + f"{bv} = {ev} - 1")
        self.indent_level -= 1
        self.code_lines.append(self.indent() + f"for {node.loop_var} in range({sv}, {bv}, {tv}):")
        self.indent_level += 1
        self.push_scope()
        if node.new_declaration and node.var_type:
            self.current_scope()[node.loop_var] = node.var_type
        self.emit_statements(node.body)
        self.pop_scope()
        self.indent_level -= 1

    def visit_SwitchNode(self, node):
        expr = self.visit(node.expression)
        first = True
        for case_expr, stmts in node.cases:
            prefix = "if" if first else "elif"
            self.code_lines.append(self.indent() + f"{prefix} {expr} == {self.visit(case_expr)}:")
            self.indent_level += 1
            self.push_scope()
            self.emit_statements(stmts)
            self.pop_scope()
            self.indent_level -= 1
            first = False
        if node.default_case is not None:
            self.code_lines.append(self.indent() + "else:")
            self.indent_level += 1
            self.push_scope()
            self.emit_statements(node.default_case)
            self.pop_scope()
            self.indent_level -= 1

    def visit_BlockNode(self, node):
        self.push_scope()
        self.emit_statements(node.statements)
        self.pop_scope()

    def visit_LiteralNode(self, node):
        if node.literal_type == 'chika':
            return f"{node.value}"
        return str(node.value)

    def visit_IdentifierNode(self, node):
        # Wrap every use in a runtime check
        return f"_cNone_({node.name}, '{node.name}')"

    def visit_BinaryOpNode(self, node):
        if node.operator == '+':
            L = self.visit(node.left)
            R = self.visit(node.right)
            lt = self.infer_type(node.left)
            rt = self.infer_type(node.right)
            if lt == 'chika' or rt == 'chika':
                if lt == 'chika' and rt != 'chika':
                    R = f"str({R})"
                elif rt == 'chika' and lt != 'chika':
                    L = f"str({L})"
                return f"({L} + {R})"
            expr = f"({L} + {R})"
            t = self.infer_type(node)
            if t in ['anda', 'andamhie']:
                return f"_cType_('{t}', {expr})"
            return expr
        else:
            L = self.visit(node.left)
            R = self.visit(node.right)
            op = node.operator
            if op == '&&':
                op = 'and'
            elif op == '||':
                op = 'or'
            expr = f"({L} {op} {R})"
            if node.operator in ['-', '*', '/', '%', '**', '//']:
                t = self.infer_type(node)
                if t in ['anda', 'andamhie']:
                    return f"_cType_('{t}', {expr})"
            return expr

    def visit_UnaryOpNode(self, node):
        val = self.visit(node.operand)
        op = node.operator
        if op == '!':
            return f"(not {val})"
        if op in ['++', '--']:
            ar = '+' if op == '++' else '-'
            expr = f"({val} {ar} 1)"
            t = self.infer_type(node.operand)
            if t in ['anda', 'andamhie']:
                return f"_cType_('{t}', {expr})"
            return expr
        return f"({op}{val})"

    def visit_ArrayAccessNode(self, node):
        code = self.visit(node.array)
        for idx in node.index_exprs:
            code += f"[{self.visit(idx)}]"
        return code

    def visit_InputCallNode(self, node):
        return f"input('{node.prompt}')"

    def infer_type(self, node):
        if hasattr(node, 'literal_type'):
            return node.literal_type
        if hasattr(node, 'name'):
            vt = self.lookup_variable(node.name)
            if vt:
                return vt
        if hasattr(node, 'operator'):
            if node.operator == '+':
                lt = self.infer_type(node.left)
                rt = self.infer_type(node.right)
                if lt == 'chika' or rt == 'chika':
                    return 'chika'
                if lt == 'andamhie' or rt == 'andamhie':
                    return 'andamhie'
                return 'anda'
            if node.operator in ['-', '*', '/', '%', '**', '//']:
                lt = self.infer_type(node.left)
                rt = self.infer_type(node.right)
                if lt == 'andamhie' or rt == 'andamhie':
                    return 'andamhie'
                return 'anda'
            if node.operator in ['&&', '||']:
                return 'eklabool'
        if hasattr(node, 'operand'):
            if node.operator == '!':
                return 'eklabool'
            return self.infer_type(node.operand)
        return None

    def visit_UnaryOpStatementNode(self, node):
        val = self.visit(node.operand)
        op = node.operator
        ar = '+' if op == '++' else '-'
        t = self.infer_type(node.operand)
        expr = f"{val} {ar} 1"
        if t in ['anda', 'andamhie']:
            expr = f"_cType_('{t}', {expr})"
        self.code_lines.append(self.indent() + f"{val.split('(')[-1].split(',')[0]} = {expr}")

def generate_code(ast):
    generator = CodeGenerator()
    return generator.generate(ast)
