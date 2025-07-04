from .ast_generator import UnaryOpNode, IdentifierNode, ArrayAccessNode, LiteralNode, InputCallNode, FunctionCallNode


# code_generation.py

class CodeGenerator:
    def __init__(self):
        self.indent_level = 0
        self.code_lines = []
        self.switch_counter = 0  # Used to generate unique names for switch temp variables
        self.for_counter = 0     # Used to generate unique names for for loop helper variables
        self.symbol_stack = [{}]
        # map function name -> (return_type, is_array)
        self.function_signatures = {}
        self.import_emitted = False

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
                entry = scope[var_name]
                if isinstance(entry, tuple):
                    return entry  # (type, is_array)
                else:
                    return (entry, False)  # backward compatibility
        return None

    def emit_helper_functions(self):
        # Helper to catch use-before-init errors
                # ── forbid arrays in scalar operators ─────────────────────────
        self.code_lines.append("""def _cNoArray_(value, op):
    if isinstance(value, list):
        raise TypeError(f"Runtime error: array value used with operator {op}")
    return value
""")
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
            raise OverflowError("Overflow error: value exceeds maximum for type 'anda'")
        if v < -9999999999:
            raise OverflowError("Overflow error: value exceeds minimum for type 'anda'")
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
            raise OverflowError("Overflow error: value exceeds maximum for type 'andamhie'")
        if f < -9999999999:
            raise OverflowError("Overflow error: value exceeds minimum for type 'andamhie'")
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
        # --- NEW: same-type guard for adele() --------------------------
        self.code_lines.append("""def _cSameElemType_(expected, actual):
    if expected != actual:
        raise TypeError(
            f"Type mismatch in adele(): target list holds {expected} "
            f"but value is list[{actual}]"
        )
""")
        self.code_lines.append("""def _cEnsureArray_(value, name):
    if not isinstance(value, list):
        raise TypeError(f"Runtime error: cannot append to non-array '{name}'")
    return value
""")

    def generate(self, node):
        self.emit_helper_functions()
        self.visit(node)
        self.code_lines.append("if __name__ == '__main__':")
        self.code_lines.append("    try:")
        self.code_lines.append("        _kween()")
        self.code_lines.append("    except Exception as e:")
        self.code_lines.append("        print()")
        self.code_lines.append("        print(e)")
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

    def get_base_identifier_name(self, expr):
        while isinstance(expr, ArrayAccessNode):
            expr = expr.array
        if isinstance(expr, IdentifierNode):
            return expr.name
        return "<unknown>"

    def visit_ProgramNode(self, node):
        self.emit_statements(node.statements)

    def visit_FunctionDeclNode(self, node):
        params = ", ".join(["_"+p[0] for p in node.parameters])
        self.code_lines.append(f"def _{node.name}({params}):")
        self.indent_level += 1
        self.push_scope()
        for param_info in node.parameters:
            if len(param_info) == 2:
                param_name, param_type = param_info
                is_array = False
            else:
                param_name, param_type, is_array = param_info
            self.current_scope()[param_name] = (param_type, is_array)

        # record return signature
        self.function_signatures[node.name] = (node.return_type, getattr(node, 'is_array', False))
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
            update_info = self.lookup_variable(var)
            update_type = update_info[0] if isinstance(update_info, tuple) else update_info
            # prefix: update then assign
            if not getattr(init, 'is_postfix', False):
                if update_type:
                    self.code_lines.append(
                        self.indent() +
                        f"_{var} = _cType_('{update_type}', _{var} {op_symbol} 1)"
                    )
                else:
                    self.code_lines.append(
                        self.indent() + f"_{var} = _{var} {op_symbol} 1"
                    )
                # assign to new var
                self.code_lines.append(
                    self.indent() + f"_{node.name} = _cType_('{node.data_type}', _{var})"
                )
            else:
                # postfix: assign original, then update
                self.code_lines.append(
                    self.indent() + f"_{node.name} = _cType_('{node.data_type}', _{var})"
                )
                if update_type:
                    self.code_lines.append(
                        self.indent() +
                        f"_{var} = _cType_('{update_type}', _{var} {op_symbol} 1)"
                    )
                else:
                    self.code_lines.append(
                        self.indent() + f"_{var} = _{var} {op_symbol} 1"
                    )
            # record the declared type
            self.current_scope()[node.name] = node.data_type
            return

        # Handle initializer from array-returning function call
        from .code_generation import FunctionCallNode
        if isinstance(node.initializer, FunctionCallNode):
            name = node.initializer.name
            sig = self.function_signatures.get(name)
            if sig and sig[1]:  # returns array
                # import copy if needed
                if not self.import_emitted:
                    self.code_lines.insert(0, "import copy")
                    self.import_emitted = True
                call = f"_{name}({', '.join(self.visit(a) for a in node.initializer.arguments)})"
                self.code_lines.append(
                    self.indent() +
                    f"_{node.name} = _cArray_('{node.data_type}', copy.deepcopy({call}))"
                )
                self.current_scope()[node.name] = (node.data_type, True)
                return
        # No initializer: None or empty list
        if init is None:
            code = f"_{node.name} = []" if node.is_array else f"_{node.name} = None"
            self.code_lines.append(self.indent() + code)
            self.current_scope()[node.name] = (node.data_type, node.is_array) if node.is_array else node.data_type
            return

        # 1) Literal list initializer
        if isinstance(init, list):
            expr_code = self.visit_list(init)
            code = f"_{node.name} = _cArray_('{node.data_type}', {expr_code})"
            self.code_lines.append(self.indent() + code)
            self.current_scope()[node.name] = (node.data_type, True)
            return

        # 2) Whole-array variable initializer (e.g., g = grades)
        if isinstance(init, IdentifierNode):
            info = self.lookup_variable(init.name)
            if isinstance(info, tuple) and info[1]:
                # deep-copy the source array
                if not self.import_emitted:
                    self.code_lines.insert(0, "import copy")
                    self.import_emitted = True
                code = (f"_{node.name} = _cArray_('{node.data_type}', "
                        f"copy.deepcopy(_{init.name}))")
                self.code_lines.append(self.indent() + code)
                self.current_scope()[node.name] = (node.data_type, True)
                return

        # 3) Array-element initializer (e.g., g = grades[0])
        if isinstance(init, ArrayAccessNode):
            # check base is an array variable
            base = init.array
            if isinstance(base, IdentifierNode):
                binfo = self.lookup_variable(base.name)
                if isinstance(binfo, tuple) and binfo[1]:
                    # deep-copy that array element
                    if not self.import_emitted:
                        self.code_lines.insert(0, "import copy")
                        self.import_emitted = True
                    src = self.visit(init)  # yields something like "_cNone_(_grades,'grades')[0]"
                    code = (f"_{node.name} = _cArray_('{node.data_type}', "
                            f"copy.deepcopy({src}))")
                    self.code_lines.append(self.indent() + code)
                    self.current_scope()[node.name] = (node.data_type, True)
                    return

        # 4) Scalar or mixed initializer (the old path)
        expr = self.visit(init)
        expr = f"_cType_('{node.data_type}', {expr})"
        code = f"_{node.name} = {expr}"
        self.code_lines.append(self.indent() + code)
        self.current_scope()[node.name] = node.data_type

    def visit_AssignmentNode(self, node):
        # ───────── ARRAY ELEMENT on the LHS ─────────
        if isinstance(node.identifier, ArrayAccessNode):
            lhs_code = self.visit(node.identifier)

            # literal {…} on RHS
            if isinstance(node.expression, list):
                rhs_code  = self.visit_list(node.expression)
                base_name = self.get_base_identifier_name(node.identifier)
                elem_type = self.lookup_variable(base_name)[0]
                rhs_code  = f"_cArray_('{elem_type}', {rhs_code})"
            else:
                rhs_code  = self.visit(node.expression)
                base_name = self.get_base_identifier_name(node.identifier)
                elem_type = self.lookup_variable(base_name)[0]
                rhs_code  = f"_cType_('{elem_type}', {rhs_code})"

            self.code_lines.append(self.indent() + f"{lhs_code} = {rhs_code}")
            return

        if not isinstance(node.identifier, IdentifierNode):
            raise Exception("Unsupported assignment target: " + repr(node.identifier))

        lhs_name     = node.identifier.name
        lhs_info     = self.lookup_variable(lhs_name)
        lhs_type     = lhs_info[0] if isinstance(lhs_info, tuple) else lhs_info
        lhs_is_array = isinstance(lhs_info, tuple) and lhs_info[1]

        rhs_is_array = isinstance(node.expression, list)
        rhs_code     = (self.visit_list(node.expression)
                        if rhs_is_array else self.visit(node.expression))

        # Detect “RHS is an array variable” (IdentifierNode) for clamping
        if (not rhs_is_array) and isinstance(node.expression, IdentifierNode):
            rhs_info     = self.lookup_variable(node.expression.name)
            rhs_is_array = isinstance(rhs_info, tuple) and rhs_info[1]

        if node.operator != "=":
            if lhs_is_array or rhs_is_array:
                self.code_lines.append(
                    self.indent() +
                    f"raise TypeError('Compound operator {node.operator} not valid with arrays')"
                )
                return
            op_map = {"+=":"+", "-=":"-", "*=":"*", "/=":"/", "%=":"%", "**=":"**", "//=":"//"}
            op     = op_map[node.operator]
            if lhs_type:
                rhs_code = f"_cType_('{lhs_type}', {rhs_code})"
                expr     = f"_cType_('{lhs_type}', _{lhs_name} {op} {rhs_code})"
                self.code_lines.append(self.indent() + f"_{lhs_name} = {expr}")
            else:
                self.code_lines.append(self.indent() + f"_{lhs_name} {node.operator} {rhs_code}")
            return

        if lhs_is_array:
            # always clamp the incoming value to an array of the correct element-type
            if lhs_type:
                rhs_code = f"_cArray_('{lhs_type}', {rhs_code})"
            self.code_lines.append(self.indent() + f"_{lhs_name} = {rhs_code}")
        else:
            # scalar LHS: clamp to the declared primitive type when we know it
            if lhs_type:
                rhs_code = f"_cType_('{lhs_type}', {rhs_code})"
            self.code_lines.append(self.indent() + f"_{lhs_name} = {rhs_code}")

    # ──────────────────────────────────────────────────────────────────────────
    #  CodeGenerator : visit_FunctionCallNode
    # ──────────────────────────────────────────────────────────────────────────
    def visit_FunctionCallNode(self, node):
        # ─── built-in len() ────────────────────────────────────────────────
        if node.name == 'len':
            arg_code = self.visit(node.arguments[0])
            return f"_cType_('anda', len({arg_code}))"

        # ─── built-in adele(target_list , value_to_append) ────────────────
        if node.name == 'adele':
            tgt_expr = node.arguments[0]        # e.g. msgs
            src_expr = node.arguments[1]        # e.g. msgs2  OR  msgs2[0]  OR  {…}

            # helper: recover element-type (anda/chika/…) of an array expr
            def array_info(expr):
                if isinstance(expr, IdentifierNode):
                    info = self.lookup_variable(expr.name)
                    if isinstance(info, tuple) and info[1]:      # is_array flag
                        return info[0]
                if isinstance(expr, ArrayAccessNode):
                    return array_info(expr.array)
                return None

            tgt_code  = self.visit(tgt_expr)
            src_code  = self.visit(src_expr)
            tgt_etype = array_info(tgt_expr)

            # ── is the 2nd arg a *whole array variable*? ─────────────────
            src_is_whole_array = (
                isinstance(src_expr, IdentifierNode) and
                isinstance(self.lookup_variable(src_expr.name), tuple) and
                self.lookup_variable(src_expr.name)[1]            # is_array
            )

            # runtime name used in _cEnsureArray_() message
            display_name = self.get_base_identifier_name(tgt_expr)
            array_check  = f"_cEnsureArray_({tgt_code}, '{display_name}')"

            # ── case 1: whole array → deep copy, clamp element-type ───────
            if src_is_whole_array:
                # make sure `copy` is imported once
                if not self.import_emitted:
                    self.code_lines.insert(0, "import copy")
                    self.import_emitted = True

                if tgt_etype:
                    src_code = f"_cArray_('{tgt_etype}', copy.deepcopy({src_code}))"
                else:
                    src_code = f"copy.deepcopy({src_code})"

                return f"{array_check}.append({src_code})"

            # ── case 2: scalar value or { … } literal ─────────────────────
            if tgt_etype:
                if isinstance(src_expr, list):                     # literal list
                    src_code = f"_cArray_('{tgt_etype}', {self.visit_list(src_expr)})"
                else:                                             # scalar / element access
                    src_code = f"_cType_('{tgt_etype}', {src_code})"

            return f"{array_check}.append({src_code})"

        # ─── built-in adelete() ───────────────────────────────────────────
        if node.name == 'adelete':
            if len(node.arguments) != 1:
                return "raise TypeError('adelete() takes exactly 1 argument')"

            target = node.arguments[0]
            if isinstance(target, IdentifierNode):                 # whole list
                return f"del _{target.name}"
            if isinstance(target, ArrayAccessNode):                # element
                return f"del {self.visit(target)}"

            return ("raise TypeError('adelete() argument must be an array "
                    "variable or array element reference')")

        # ─── user-defined functions ───────────────────────────────────────
        args = ", ".join(self.visit(a) for a in node.arguments)
        return f"_{node.name}({args})"


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
        sv = f"_start_val_{idx}"
        ev = f"_end_val_{idx}"
        tv = f"_step_val_{idx}"
        bv = f"_end_bound_{idx}"
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
        self.code_lines.append(self.indent() + f"for _{node.loop_var} in range({sv}, {bv}, {tv}):")
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

    def visit_BreakNode(self, node):
        self.code_lines.append(self.indent() + "break")

    def visit_ContinueNode(self, node):
        self.code_lines.append(self.indent() + "continue")

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
        return f"_cNone_(_{node.name}, '{node.name}')"

    def visit_BinaryOpNode(self, node):
        # first generate raw operand code
        L_raw = self.visit(node.left)
        R_raw = self.visit(node.right)

        # wrap them: arrays are disallowed in operators
        L = f"_cNoArray_({L_raw}, '{node.operator}')"
        R = f"_cNoArray_({R_raw}, '{node.operator}')"

        # handle '+' special-case for chika concatenation
        if node.operator == '+':
            lt = self.infer_type(node.left)
            rt = self.infer_type(node.right)
            if lt == 'chika' or rt == 'chika':
                if lt == 'chika' and rt != 'chika':
                    R = f"str({R})"
                elif rt == 'chika' and lt != 'chika':
                    L = f"str({L})"
                return f"({L} + {R})"

        # map logical symbols
        op_map = {'&&': 'and', '||': 'or'}
        op = op_map.get(node.operator, node.operator)

        expr = f"({L} {op} {R})"

        # numeric post-clamp for maths ops
        if node.operator in ['+', '-', '*', '/', '%', '**', '//']:
            t = self.infer_type(node)
            if t in ['anda', 'andamhie']:
                return f"_cType_('{t}', {expr})"
        return expr

    def visit_UnaryOpNode(self, node):
        val_raw = self.visit(node.operand)
        val     = f"_cNoArray_({val_raw}, '{node.operator}')"
        op      = node.operator

        if op == '!':
            return f"(not {val})"

        if op in ['++', '--']:
            ar = '+' if op == '++' else '-'
            t  = self.infer_type(node.operand)
            expr = f"({val} {ar} 1)"
            return f"_cType_('{t}', {expr})" if t in ['anda', 'andamhie'] else expr

        # plain unary ‘-’
        return f"({op}{val})"

    def visit_ArrayAccessNode(self, node):
        base = self.visit(node.array)
        for idx in node.index_exprs:
            # If base is a string literal, don't wrap it with _cNone_
            if isinstance(node.array, LiteralNode):
                base = f"({base})[{self.visit(idx)}]"
            else:
                base = f"{base}[{self.visit(idx)}]"
        return base

    def visit_InputCallNode(self, node):
        return f"input('{node.prompt}')"

    def infer_type(self, node):
        # — string/number/boolean literals —
        if isinstance(node, LiteralNode):
            return node.literal_type

        # — givenchy(input) always yields a string (chika) —
        if isinstance(node, InputCallNode):
            return 'chika'

        # — identifiers: lookup in your symbol stack, then take only the type portion —
        if hasattr(node, 'name'):
            vt = self.lookup_variable(node.name)    # returns (type,is_array) or None
            if vt:
                return vt[0] if isinstance(vt, tuple) else vt

        # — operators: same logic as before —
        if hasattr(node, 'operator'):
            if node.operator == '+':
                lt = self.infer_type(node.left)
                rt = self.infer_type(node.right)
                # if either side is a string, result is string
                if lt == 'chika' or rt == 'chika':
                    return 'chika'
                # else if either is float, result is float
                if lt == 'andamhie' or rt == 'andamhie':
                    return 'andamhie'
                return 'anda'
            if node.operator in ['-', '*', '/', '%', '**', '//']:
                lt = self.infer_type(node.left)
                rt = self.infer_type(node.right)
                return 'andamhie' if lt == 'andamhie' or rt == 'andamhie' else 'anda'
            if node.operator in ['&&', '||']:
                return 'eklabool'

        # — unary operators —
        if hasattr(node, 'operand'):
            if node.operator == '!':
                return 'eklabool'
            return self.infer_type(node.operand)

        # fall-back
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
