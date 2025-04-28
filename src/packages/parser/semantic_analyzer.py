# semantic_analyzer.py

from .error_handler import SemanticError

class SemanticAnalyzer:
    def __init__(self, token_stream):
        self.symbol_table = {
            "variables": {},
            "functions": {}
        }
        self.current_function = None  # None means global scope.
        # Filter out whitespace, newline, and comment tokens.
        self._token_stream = [t for t in token_stream if t[0][1] not in ['whitespace', 'newline', 'comment']]
        self.token_index = 0
        # Stack for block scopes (for conditionals, loops, and other nested blocks)
        self.block_scopes = []
        self.log = ''
        self.allow_unindexed_array_usage = False

    def current_token(self):
        if 0 <= self.token_index < len(self._token_stream):
            return self._token_stream[self.token_index][0]
        return None

    def next_token(self):
        next_index = self.token_index + 1
        if next_index < len(self._token_stream):
            return self._token_stream[next_index][0]
        return None

    def advance(self):
        self.token_index += 1

    def analyze(self):
        try:
            while self.current_token():
                token = self.current_token()
                if token[1] in ['naur', 'anda', 'andamhie', 'chika', 'eklabool', 'shimenet']:
                    self.handle_declaration()
                elif token[1] == 'pak':
                    self.process_conditional_statement()
                elif token[1] == 'serve':
                    self.process_serve_statement()
                elif token[1] == 'adele':
                    self.process_adele_statement()
                elif token[1] == 'adelete':
                    self.process_adelete_statement()
                elif token[1] == 'push':
                    self.process_push_statement()
                elif token[1] == 'keri':
                    # Distinguish between while and do-while loops.
                    if self.next_token() and self.next_token()[1] == 'lang':
                        self.process_do_while_loop()
                    else:
                        self.process_while_loop()
                elif token[1] == 'versa':
                    self.process_switch_statement()
                elif token[1] == 'forda':
                    self.process_forda_loop()
                elif token[1] == 'id' and self.next_token() and self.next_token()[1] == '(':
                    self.process_function_call()
                elif token[1] == 'id' and self.next_token() and self.next_token()[1] in ['=', '+=', '-=', '*=', '/=', '%=', '**=', '//=']:
                    self.process_assignment_statement()
                else:
                    self.advance()
            self.finalize_functions()
            return True
        except SemanticError as e:
            print("Semantic error: " + str(e))
            return False

    def process_push_statement(self):
        if self.current_function is None:
            error_token = self._token_stream[self.token_index]
            self.log += str(SemanticError(
                "Return statement 'push' is only allowed inside function bodies",
                error_token[1][0]
            )) + '\n'

        func_entry = self.symbol_table["functions"][self.current_function]
        declared_return_type = func_entry["return_type"]
        self.advance()  # Skip 'push'

        # ─── Allow bare-array usage just for this return expression ───
        orig_allow = self.allow_unindexed_array_usage
        self.allow_unindexed_array_usage = True

        # Capture position for error messages
        push_token_pos = (
            self._token_stream[self.token_index][1][0]
            if self.token_index < len(self._token_stream) else -1
        )

        # If there's an expression (not just a bare ';')
        if self.current_token() and self.current_token()[1] != ';':
            expr_type = self.evaluate_expression()

            # Restore normal rules immediately after parsing expression
            self.allow_unindexed_array_usage = orig_allow

            if not self.current_token() or self.current_token()[1] != ';':
                self.log += str(SemanticError(
                    "Missing semicolon after return expression",
                    push_token_pos
                )) + '\n'
            self.advance()

            # type‐check return‐value compatibility
            if declared_return_type == 'shimenet':
                self.log += str(SemanticError(
                    "Function with return type 'shimenet' must not return a value",
                    push_token_pos
                )) + '\n'

            func_entry["has_return"] = True

            # your existing return‐type checks here...
            # e.g. numeric vs boolean vs string compatibility

        else:
            # no expression → push without value
            self.allow_unindexed_array_usage = orig_allow

            if declared_return_type != 'shimenet':
                self.log += str(SemanticError(
                    f"Function '{self.current_function}' with return type '{declared_return_type}' must return a value",
                    push_token_pos
                )) + '\n'
            if not self.current_token() or self.current_token()[1] != ';':
                self.log += str(SemanticError(
                    "Missing semicolon after 'push'",
                    push_token_pos
                )) + '\n'
            self.advance()
            func_entry["has_return"] = True

    def finalize_functions(self):
        for func_name, func_entry in self.symbol_table["functions"].items():
            if not func_entry.get("defined", False):
                self.log += str(SemanticError(f"Function '{func_name}' declared but not defined")) + '\n'

    def process_initializer(self, var_type):
        # Evaluate the full expression.
        value_type = self.evaluate_expression()
        # If the expression is a givenchy call, bypass type checking.
        if value_type == "givenchy":
            return value_type
        # Check compatibility based on your rules.
        if var_type in ['anda', 'andamhie']:
            if value_type not in ['anda', 'andamhie', 'eklabool']:
                self.log += str(SemanticError(f"Variable of type '{var_type}' cannot be assigned a value of type '{value_type}'", self._token_stream[self.token_index][1][0])) + '\n'
        elif var_type == 'eklabool':
            if value_type not in ['eklabool', 'anda', 'andamhie', 'chika']:
                self.log += str(SemanticError(f"Variable of type 'eklabool' cannot be assigned a value of type '{value_type}'", self._token_stream[self.token_index][1][0])) + '\n'
        elif var_type == 'chika':
            if value_type != 'chika':
                self.log += str(SemanticError(f"Variable of type 'chika' cannot be assigned a value of type '{value_type}'", self._token_stream[self.token_index][1][0])) + '\n'
        return value_type

    def process_array_dimensions(self):
        """
        Revised to parse an expression inside [ ] for each dimension
        rather than expecting a simple integer literal.
        The dimension's type can be anything except 'chika'.
        """
        dims = []
        while self.current_token() and self.current_token()[1] == '[':
            self.advance()  # Skip '['

            # Require literal size
            token = self.current_token()
            if token[1] != 'anda_literal':
                self.log += str(SemanticError("Array size must be an anda literal", self._token_stream[self.token_index][1][0])) + '\n'
                self.advance()
                continue

            size = int(token[0])
            if size <= 0:
                self.log += str(SemanticError("Array size must be greater than 0", self._token_stream[self.token_index][1][0])) + '\n'
            dims.append(size)
            self.advance()  # Skip the literal

            if not self.current_token() or self.current_token()[1] != ']':
                self.log += str(SemanticError("Expected ']' after array dimension size", self._token_stream[self.token_index][1][0])) + '\n'
            self.advance()  # Skip ']'

            if len(dims) > 3:
                self.log += str(SemanticError("Arrays cannot have more than 3 dimensions", self._token_stream[self.token_index][1][0])) + '\n'
        return dims

    def process_array_initializer(self, dimensions, var_type, dim_index=0):
        """
        Recursively processes an array initializer list.
        Validates that the number of elements matches the declared dimensions at each level
        and that the dimensions are correct.
        """
        if not self.current_token() or self.current_token()[1] != '{':
            self.log += str(SemanticError("Expected '{' to start array initializer", self._token_stream[self.token_index][1][0])) + '\n'
        self.advance()  # Skip '{'

        init_list = []
        count_elements = 0

        while self.current_token() and self.current_token()[1] != '}':
            # Check if we expect more dimensions
            is_nested = self.current_token()[1] == '{'
            
            # Verify dimension depth is correct
            if is_nested:
                if dim_index + 1 >= len(dimensions):
                    self.log += str(SemanticError("Initializer has too many nested levels", self._token_stream[self.token_index][1][0])) + '\n'
                    # Skip this nested initializer to continue parsing
                    nested_braces = 1
                    self.advance()  # Skip '{'
                    while nested_braces > 0 and self.current_token():
                        if self.current_token()[1] == '{':
                            nested_braces += 1
                        elif self.current_token()[1] == '}':
                            nested_braces -= 1
                        self.advance()
                    continue
                element = self.process_array_initializer(dimensions, var_type, dim_index + 1)
            else:
                # If we're not at the deepest level but found a non-array element
                if dim_index < len(dimensions) - 1:
                    self.log += str(SemanticError(f"Expected nested array at dimension {dim_index+1}, but got a scalar value", 
                                            self._token_stream[self.token_index][1][0])) + '\n'
                element_type = self.evaluate_expression()

                # Type validation
                if var_type in ['anda', 'andamhie']:
                    if element_type not in ['anda', 'andamhie', 'eklabool']:
                        self.log += str(SemanticError(f"Array of type '{var_type}' cannot have element of type '{element_type}'", 
                                                self._token_stream[self.token_index][1][0])) + '\n'
                elif var_type == 'eklabool':
                    if element_type not in ['eklabool', 'anda', 'andamhie']:
                        self.log += str(SemanticError(f"Array of type 'eklabool' cannot have element of type '{element_type}'", 
                                                self._token_stream[self.token_index][1][0])) + '\n'
                elif var_type == 'chika':
                    if element_type != 'chika':
                        self.log += str(SemanticError(f"Array of type 'chika' cannot have element of type '{element_type}'", 
                                                self._token_stream[self.token_index][1][0])) + '\n'
                element = element_type

            init_list.append(element)
            count_elements += 1

            if self.current_token() and self.current_token()[1] == ',':
                self.advance()

        # Check if element count matches the declared size for this dimension
        if dim_index < len(dimensions):
            expected_size = dimensions[dim_index]
            if expected_size != count_elements:
                self.log += str(SemanticError(
                    f"Array initializer at dimension {dim_index+1} expects {expected_size} elements, but got {count_elements}",
                    self._token_stream[self.token_index][1][0]
                )) + '\n'

        if not self.current_token() or self.current_token()[1] != '}':
            self.log += str(SemanticError("Expected '}' at end of array initializer", self._token_stream[self.token_index][1][0])) + '\n'
        self.advance()  # Skip '}'
        return init_list

    def handle_declaration(self):
        is_constant = False
        token = self.current_token()
        if token[1] == 'naur':
            is_constant = True
            self.advance()
            token = self.current_token()
        if token[1] == 'shimenet':
            if is_constant:
                self.log += str(SemanticError("Constant declaration cannot be a function declaration", self._token_stream[self.token_index][1][0])) + '\n'
            if self.current_function is not None:
                self.log += str(SemanticError("Nested function declarations are not allowed", self._token_stream[self.token_index][1][0])) + '\n'
            self.advance()  # Skip 'shimenet'
            if self.current_token() and self.current_token()[1] == 'kween':
                func_name = "kween"
                self.advance()
            elif self.current_token() and self.current_token()[1] == 'id':
                func_name = self.current_token()[0]
                self.advance()
            else:
                self.log += str(SemanticError("Expected function name after 'shimenet'", self._token_stream[self.token_index][1][0])) + '\n'
            self.function_declaration('shimenet', func_name)
            return
        if token[1] not in ['anda', 'andamhie', 'chika', 'eklabool']:
            self.log += str(SemanticError("Expected a type token after 'naur'" if is_constant else "Expected a type token", self._token_stream[self.token_index][1][0])) + '\n'
        data_type = token[1]
        self.advance()  # Skip type token
        if not self.current_token() or self.current_token()[1] != 'id':
            self.log += str(SemanticError("Expected identifier after type declaration", self._token_stream[self.token_index][1][0])) + '\n'
        var_name = self.current_token()[0]
        self.advance()  # Skip identifier
        # Check if this is a function declaration (if '(' follows immediately).
        if self.current_token() and self.current_token()[1] == '(':
            if var_name == "kween" and data_type != "shimenet":
                self.log += str(SemanticError("Function 'kween' must have return type 'shimenet'", self._token_stream[self.token_index][1][0])) + '\n'
            self.function_declaration(data_type, var_name)
            return
        # Otherwise, it's a variable declaration.
        self.process_variable_declaration(data_type, var_name, is_constant)
        while self.current_token() and self.current_token()[1] == ',':
            self.advance()  # Skip comma
            if not self.current_token() or self.current_token()[1] != 'id':
                self.log += str(SemanticError("Expected identifier after comma in declaration", self._token_stream[self.token_index][1][0])) + '\n'
            var_name = self.current_token()[0]
            self.advance()  # Skip identifier
            self.process_variable_declaration(data_type, var_name, is_constant)
        if not self.current_token() or self.current_token()[1] != ';':
            self.log += str(SemanticError("Missing semicolon at end of declaration", self._token_stream[self.token_index][1][0])) + '\n'
        self.advance()  # Skip ';'

    def process_variable_declaration(self, data_type, var_name, is_constant):
        is_array = False
        initializer_value = None            # stored in the symbol-table entry

        if self.current_token() and self.current_token()[1] == '[':
            is_array = True
            self.advance()
            if not self.current_token() or self.current_token()[1] != ']':
                self.log += str(SemanticError(
                    "Expected ']' after '[' in array declaration",
                    self._token_stream[self.token_index][1][0])) + '\n'
            else:
                self.advance()              # skip ']'
        if self.current_token() and self.current_token()[1] == '=':
            self.advance()

            if self.current_token() and self.current_token()[1] == '{':
                if is_array:
                    initializer_value = self.process_array_initializer_dynamic(data_type)
                else:
                    initializer_value = self.evaluate_expression()

            else:
                saved_flag = self.allow_unindexed_array_usage
                if is_array:
                    # allow a naked array name like  chika words2[] = words;
                    self.allow_unindexed_array_usage = True

                rhs_type, rhs_name = self.evaluate_expression_with_name()

                self.allow_unindexed_array_usage = saved_flag
                initializer_value = rhs_type      # we just keep the type info

                # shape compatibility checks
                if is_array and not self._is_array_type(rhs_type):
                    self.log += str(SemanticError(
                        f"Array variable '{var_name}' must be initialised with an array value",
                        self._token_stream[self.token_index][1][0])) + '\n'
                if (not is_array) and self._is_array_type(rhs_type):
                    self.log += str(SemanticError(
                        f"Scalar variable '{var_name}' cannot be initialised with an array value",
                        self._token_stream[self.token_index][1][0])) + '\n'

        if is_constant and initializer_value is None:
            self.log += str(SemanticError(
                "Constant variable declaration must be assigned an initializer",
                self._token_stream[self.token_index][1][0])) + '\n'

        self.register_variable(data_type, var_name, is_constant,
                            initializer_value, is_array)

    def process_array_initializer_dynamic(self, var_type=None, dim_index=0):
        if not self.current_token() or self.current_token()[1] != '{':
            self.log += str(SemanticError("Expected '{' to start array initializer", self._token_stream[self.token_index][1][0])) + '\n'
            return []

        self.advance()  # skip '{'
        elements = []
        count_elements = 0

        while self.current_token() and self.current_token()[1] != '}':
            if self.current_token()[1] == '{':
                sub_array = self.process_array_initializer_dynamic(var_type, dim_index + 1)
                elements.append(sub_array)
            else:
                element_type = self.evaluate_expression()
                # Now validate type matching
                if var_type:
                    if var_type in ['anda', 'andamhie']:
                        if element_type not in ['anda', 'andamhie', 'eklabool']:
                            self.log += str(SemanticError(
                                f"Array of type '{var_type}' cannot have element of type '{element_type}'",
                                self._token_stream[self.token_index][1][0]
                            )) + '\n'
                    elif var_type == 'eklabool':
                        if element_type not in ['eklabool', 'anda', 'andamhie']:
                            self.log += str(SemanticError(
                                f"Array of type 'eklabool' cannot have element of type '{element_type}'",
                                self._token_stream[self.token_index][1][0]
                            )) + '\n'
                    elif var_type == 'chika':
                        if element_type != 'chika':
                            self.log += str(SemanticError(
                                f"Array of type 'chika' cannot have element of type '{element_type}'",
                                self._token_stream[self.token_index][1][0]
                            )) + '\n'
                elements.append(element_type)

            count_elements += 1

            if self.current_token() and self.current_token()[1] == ',':
                self.advance()

        if not self.current_token() or self.current_token()[1] != '}':
            self.log += str(SemanticError("Expected '}' at end of array initializer", self._token_stream[self.token_index][1][0])) + '\n'
        else:
            self.advance()  # skip '}'

        return elements

    def register_variable(self, var_type, var_name, is_constant, initializer_value, is_array=False):
        entry = {
            "data_type": var_type,
            "value": initializer_value,
            "naur_flag": is_constant,
            "is_array": is_array
        }
        if is_array and initializer_value is not None:
            if isinstance(initializer_value, list):
                entry["dimensions"] = self.calculate_array_shape(initializer_value)
            else:
                entry["dimensions"] = []  # Empty array case
        elif is_array:
            entry["dimensions"] = []  # No initializer case

        if self.block_scopes:
            if self.variable_exists_in_enclosing_scopes(var_name):
                self.log += str(SemanticError(f"Redeclaration of variable '{var_name}' in block scope is not allowed", self._token_stream[self.token_index][1][0])) + '\n'
            self.block_scopes[-1][var_name] = entry
        else:
            if self.current_function is None:
                if var_name in self.symbol_table["variables"]:
                    self.log += str(SemanticError(f"Redeclaration of global variable '{var_name}'", self._token_stream[self.token_index][1][0])) + '\n'
                self.symbol_table["variables"][var_name] = entry
            else:
                if any(param[0] == var_name for param in self.symbol_table["functions"][self.current_function]["parameters"]):
                    self.log += str(SemanticError(f"Local variable '{var_name}' conflicts with a parameter in function '{self.current_function}'", self._token_stream[self.token_index][1][0])) + '\n'
                if var_name in self.symbol_table["functions"][self.current_function]["locals"]:
                    self.log += str(SemanticError(f"Redeclaration of local variable '{var_name}' in function '{self.current_function}'", self._token_stream[self.token_index][1][0])) + '\n'
                self.symbol_table["functions"][self.current_function]["locals"][var_name] = entry

    def calculate_array_shape(self, initializer):
        if not isinstance(initializer, list):
            return []
        dims = [len(initializer)]
        if len(initializer) > 0 and isinstance(initializer[0], list):
            dims += self.calculate_array_shape(initializer[0])
        return dims

    def variable_exists_in_enclosing_scopes(self, var_name):
        # Check any active block scopes.
        for scope in self.block_scopes:
            if var_name in scope:
                return True
        # Check function parameters and locals if in a function.
        if self.current_function is not None:
            for param in self.symbol_table["functions"][self.current_function]["parameters"]:
                if param[0] == var_name:
                    return True
            if var_name in self.symbol_table["functions"][self.current_function]["locals"]:
                return True
            # Finally, check global variables
            if var_name in self.symbol_table["variables"]:
                return True
        else:
            if var_name in self.symbol_table["variables"]:
                return True
        return False

    # ──────────────────────────────────────────────────────────
    # Small utility: look up a variable entry in any accessible
    # scope (block → locals → params → globals). Returns None
    # if the name is unknown in every scope.
    # ──────────────────────────────────────────────────────────
    def lookup_variable(self, name):
        if self.current_function:
            # innermost block-scopes first
            for scope in reversed(self.block_scopes):
                if name in scope:
                    return scope[name]
            # then locals
            if name in self.symbol_table["functions"][self.current_function]["locals"]:
                return self.symbol_table["functions"][self.current_function]["locals"][name]
            # then parameters
            for p_name, p_type, p_is_arr in self.symbol_table["functions"][self.current_function]["parameters"]:
                if p_name == name:
                    return {"data_type": p_type, "is_array": p_is_arr}
        # finally globals
        return self.symbol_table["variables"].get(name)


    # ──────────────────────────────────────────────────────────
    #  assignment :  id [ '[' expr ']' ] assignment_op rhs_expr ';'
    # ──────────────────────────────────────────────────────────
    def process_assignment_statement(self):
        lhs_name = self.current_token()[0]   # variable being written
        self.advance()                       # skip identifier

        # ---------- optional single-dimension indexing ----------
        is_indexed = False
        if self.current_token() and self.current_token()[1] == '[':
            is_indexed = True
            self.advance()
            index_t = self.evaluate_expression()
            if index_t not in ['anda', 'andamhie']:
                self.log += str(SemanticError("Array index must be numeric", 
                                              self._token_stream[self.token_index][1][0])) + '\n'
            if not self.current_token() or self.current_token()[1] != ']':
                self.log += str(SemanticError("Expected ']' after array index", 
                                              self._token_stream[self.token_index][1][0])) + '\n'
            self.advance()

        # ---------- assignment operator ----------
        if not self.current_token():
            self.log += str(SemanticError("Expected assignment operator after identifier", 
                                          self._token_stream[self.token_index-1][1][0])) + '\n'
            return
        op_tok = self.current_token();  op = op_tok[1]
        if op not in ['=', '+=', '-=', '*=', '/=', '%=', '**=', '//=']:
            self.log += str(SemanticError("Expected an assignment operator", 
                                          self._token_stream[self.token_index][1][0])) + '\n'
        self.advance()

        # ---------- look-up LHS variable ----------
        lhs_entry = self.lookup_variable(lhs_name)
        if not lhs_entry:
            self.log += str(SemanticError(f"Assignment to undeclared variable '{lhs_name}'", 
                                          op_tok[1][0])) + '\n'
            lhs_entry = {"data_type": 'anda', "is_array": False, "naur_flag": False}  # recovery

        if lhs_entry.get("naur_flag"):
            self.log += str(SemanticError(f"Assignment to constant variable '{lhs_name}' is not allowed", 
                                          op_tok[1][0])) + '\n'

        lhs_is_array = lhs_entry.get("is_array", False)

        # ---------- RHS parsing ----------
        # If we’re assigning **to an array variable**, briefly allow bare
        # array names on the RHS so parse_primary won’t complain.
        saved_allow = self.allow_unindexed_array_usage
        if lhs_is_array:
            self.allow_unindexed_array_usage = True

        rhs_is_array = False
        if self.current_token() and self.current_token()[1] == '{':
            # array literal
            rhs_is_array = True
            rhs_type = self.process_array_initializer_dynamic(var_type=lhs_entry["data_type"])
        else:
            rhs_type, rhs_name = self.evaluate_expression_with_name()
            # check if the expression was a bare identifier that denotes
            # an array variable
            var_ent = self.lookup_variable(rhs_name)
            if var_ent and var_ent.get("is_array", False):
                rhs_is_array = True

        # restore the flag
        self.allow_unindexed_array_usage = saved_allow

        # ---------- expect ';' ----------
        if not self.current_token() or self.current_token()[1] != ';':
            self.log += str(SemanticError("Expected ';' at end of assignment statement", 
                                          self._token_stream[self.token_index][1][0])) + '\n'
        self.advance()

        # ---------- type / shape checks ----------
        if is_indexed:
            # assigning **into** a single element
            if rhs_is_array:
                self.log += str(SemanticError(f"Cannot assign an array value to a single element '{lhs_name}[…]'", 
                                              self._token_stream[self.token_index-1][1][0])) + '\n'
        else:
            if lhs_is_array != rhs_is_array:
                if lhs_is_array:
                    self.log += str(SemanticError(f"Array variable '{lhs_name}' must be assigned an array, not a scalar value", 
                                                  self._token_stream[self.token_index-1][1][0])) + '\n'
                else:
                    self.log += str(SemanticError(f"Scalar variable '{lhs_name}' cannot be assigned an array value", 
                                                  self._token_stream[self.token_index-1][1][0])) + '\n'
            else:
                # scalar-to-scalar, or array-to-array → keep your previous
                # primitive-type compatibility rules
                if not lhs_is_array:
                    lt = lhs_entry["data_type"]; rt = rhs_type
                    if lt in ['anda', 'andamhie']:
                        if rt not in ['anda', 'andamhie', 'eklabool', 'givenchy']:
                            self.log += str(SemanticError(f"Variable '{lhs_name}' of type '{lt}' cannot be assigned a value of type '{rt}'",
                                                          self._token_stream[self.token_index-1][1][0])) + '\n'
                    elif lt == 'eklabool':
                        if rt not in ['anda', 'andamhie', 'eklabool', 'chika', 'givenchy']:
                            self.log += str(SemanticError(f"Variable '{lhs_name}' of type '{lt}' cannot be assigned a value of type '{rt}'",
                                                          self._token_stream[self.token_index-1][1][0])) + '\n'
                    elif lt == 'chika':
                        if rt not in ['chika', 'givenchy']:
                            self.log += str(SemanticError(f"Variable '{lhs_name}' of type '{lt}' must be assigned a 'chika'", 
                                                          self._token_stream[self.token_index-1][1][0])) + '\n'

    def evaluate_expression_with_name(self):
        """Evaluates an expression and also tries to capture the base variable name if it exists."""
        saved_index = self.token_index
        name = None
        if self.current_token() and self.current_token()[1] == 'id':
            name = self.current_token()[0]  # Save the name
        expr_type = self.evaluate_expression()
        if name is None:
            # If it's not a simple ID, return something unique to avoid wrong lookups
            name = f"<nonvar@{saved_index}>"
        return expr_type, name

    def process_adele_statement(self):
        """Built-in adele(arr, value): append `value` to array `arr`."""
        # record position for error messages
        pos = self._token_stream[self.token_index][1][0]

        # skip the 'adele' identifier
        self.advance()
        if not self.current_token() or self.current_token()[1] != '(':
            self.log += str(SemanticError("Expected '(' after 'adele'", pos)) + '\n'
        self.advance()

        # ─── first argument: must be an array variable ───
        saved_flag = self.allow_unindexed_array_usage
        self.allow_unindexed_array_usage = True
        arg_type, arg_name = self.evaluate_expression_with_name()
        self.allow_unindexed_array_usage = saved_flag

        entry = self.lookup_variable(arg_name)
        if not entry:
            self.log += str(SemanticError(f"Argument '{arg_name}' to 'adele' is not declared", pos)) + '\n'
        elif not entry.get("is_array", False):
            self.log += str(SemanticError(f"Argument '{arg_name}' to 'adele' must be an array", pos)) + '\n'

        # expect comma
        if not self.current_token() or self.current_token()[1] != ',':
            self.log += str(SemanticError("Expected ',' after first argument in 'adele'", pos)) + '\n'
        else:
            self.advance()

        # ─── second argument: any expression ───
        saved_flag = self.allow_unindexed_array_usage
        self.allow_unindexed_array_usage = True
        self.evaluate_expression()
        self.allow_unindexed_array_usage = saved_flag

        # closing ')'
        if not self.current_token() or self.current_token()[1] != ')':
            self.log += str(SemanticError("Missing ')' in 'adele' call", pos)) + '\n'
        else:
            self.advance()

        # semicolon
        if not self.current_token() or self.current_token()[1] != ';':
            self.log += str(SemanticError("Missing ';' after 'adele' call", pos)) + '\n'
        else:
            self.advance()


    def process_adelete_statement(self):
        # current token is 'adelete'
        pos = self._token_stream[self.token_index][1][0]
        self.advance()  # skip 'adelete'
        if not self.current_token() or self.current_token()[1] != '(':
            self.log += str(SemanticError("Expected '(' after 'adelete'", pos)) + '\n'
        self.advance()  # skip '('

        # temporarily allow bare-array usage
        saved_flag = self.allow_unindexed_array_usage
        self.allow_unindexed_array_usage = True

        # parse argument, capturing its name
        arg_type, arg_name = self.evaluate_expression_with_name()

        # restore normal rules
        self.allow_unindexed_array_usage = saved_flag

        # semantic check: must be a declared array
        entry = self.lookup_variable(arg_name)
        if not entry:
            self.log += str(SemanticError(f"Argument '{arg_name}' to 'adelete' is not declared", pos)) + '\n'
        elif not entry.get("is_array", False):
            self.log += str(SemanticError(f"Argument '{arg_name}' to 'adelete' must be an array", pos)) + '\n'

        if not self.current_token() or self.current_token()[1] != ')':
            self.log += str(SemanticError("Missing ')' in 'adelete' call", pos)) + '\n'
        else:
            self.advance()

        if not self.current_token() or self.current_token()[1] != ';':
            self.log += str(SemanticError("Missing ';' after 'adelete' call", pos)) + '\n'
        else:
            self.advance()

    def process_function_call(self):
        """
        Processes a standalone function call statement.
        It checks that the function is declared, validates the arguments against the function's parameter list,
        and ensures the statement is properly terminated with a semicolon.
        """
        # Current token is the function identifier.
        func_name = self.current_token()[0]
        self.advance()  # Skip the function identifier

        # Expect '(' after the function name.
        if not self.current_token() or self.current_token()[1] != '(':
            self.log += str(SemanticError("Expected '(' after function name in function call", self._token_stream[self.token_index][1][0])) + '\n'
        self.advance()  # Skip '('

        # Check that the function is declared.
        if func_name not in self.symbol_table["functions"]:
            self.log += str(SemanticError(f"Function '{func_name}' is not declared", self._token_stream[self.token_index][1][0])) + '\n'
            # Use a dummy function entry to allow further processing.
            func_entry = {"parameters": [], "return_type": "anda"}
        else:
            func_entry = self.symbol_table["functions"][func_name]

        expected_params = func_entry["parameters"]

        arg_info_list = []  # Will store (arg_name, arg_type)
        # Process arguments (if any).  Allow array variables un-indexed here:
        while self.current_token() and self.current_token()[1] != ')':
            original_flag = self.allow_unindexed_array_usage
            self.allow_unindexed_array_usage = True

            arg_type, arg_name = self.evaluate_expression_with_name()
            arg_info_list.append((arg_name, arg_type))

            self.allow_unindexed_array_usage = original_flag

            if self.current_token() and self.current_token()[1] == ',':
                self.advance()

        if not self.current_token() or self.current_token()[1] != ')':
            self.log += str(SemanticError(f"Missing ')' in function call to '{func_name}'", self._token_stream[self.token_index][1][0])) + '\n'
        self.advance()  # Skip ')'

        if len(arg_info_list) != len(expected_params):
            self.log += str(SemanticError(f"Function '{func_name}' expects {len(expected_params)} arguments, got {len(arg_info_list)}", self._token_stream[self.token_index][1][0])) + '\n'
        # ---------- argument-by-argument checks ----------
        for i, (arg_info, param) in enumerate(zip(arg_info_list, expected_params)):
            arg_name, arg_type = arg_info
            param_name, param_type, param_is_array = param

            # ---- work out whether the actual argument is an array ----
            is_argument_array = False
            var_entry = self.lookup_variable(arg_name)
            if var_entry and var_entry.get("is_array", False):
                is_argument_array = True

            # ---- 1. shape (array vs scalar) compatibility ----
            if is_argument_array != param_is_array:
                self.log += str(SemanticError(
                    f"Argument {i+1} '{param_name}' of function '{func_name}' expects "
                    f"{'an array' if param_is_array else 'a scalar'}, but got "
                    f"{'an array' if is_argument_array else 'a scalar'}",
                    self._token_stream[self.token_index][1][0]
                )) + '\n'
                # shape mismatch → skip further checks on this argument
                continue

            # ---- 2. primitive/base-type compatibility ----
            #      (only needed when shapes already match)
            #      For arrays we compare the *element* type, i.e. strip the 'array_' prefix first.
            base_arg_type = arg_type[len("array_"):] if isinstance(arg_type, str) and arg_type.startswith("array_") else arg_type

            if param_type in ['anda', 'andamhie']:
                if base_arg_type not in ['anda', 'andamhie', 'eklabool']:
                    self.log += str(SemanticError(
                        f"Argument {i+1} of '{func_name}' expects a numeric type, got '{base_arg_type}'",
                        self._token_stream[self.token_index][1][0])) + '\n'

            elif param_type == 'eklabool':
                if base_arg_type not in ['eklabool', 'anda', 'andamhie', 'chika']:
                    self.log += str(SemanticError(
                        f"Argument {i+1} of '{func_name}' expects a boolean type, got '{base_arg_type}'",
                        self._token_stream[self.token_index][1][0])) + '\n'

            elif param_type == 'chika':
                if base_arg_type != 'chika':
                    self.log += str(SemanticError(
                        f"Argument {i+1} of '{func_name}' expects type 'chika', got '{base_arg_type}'",
                        self._token_stream[self.token_index][1][0])) + '\n'

            # ➡️ Now additionally check array vs scalar compatibility
            # --- lookup if the argument is an array in symbol table ---
            is_argument_array = False
            var_entry = None
            if self.current_function:
                for scope in reversed(self.block_scopes):
                    if arg_name in scope:
                        var_entry = scope[arg_name]
                        break
                if not var_entry:
                    if arg_name in self.symbol_table["functions"][self.current_function]["locals"]:
                        var_entry = self.symbol_table["functions"][self.current_function]["locals"][arg_name]
                    else:
                        for param_in_func in self.symbol_table["functions"][self.current_function]["parameters"]:
                            if param_in_func[0] == arg_name:
                                var_entry = {"data_type": param_in_func[1], "is_array": param_in_func[2]}
                                break
                if not var_entry and arg_name in self.symbol_table["variables"]:
                    var_entry = self.symbol_table["variables"][arg_name]
            else:
                if arg_name in self.symbol_table["variables"]:
                    var_entry = self.symbol_table["variables"][arg_name]


            if var_entry and var_entry.get("is_array", False):
                is_argument_array = True

            # --- compare with expected parameter ---
            if is_argument_array != param_is_array:
                self.log += str(SemanticError(
                    f"Argument {i+1} '{param_name}' of function '{func_name}' expects "
                    f"{'an array' if param_is_array else 'a scalar'}, but got "
                    f"{'an array' if is_argument_array else 'a scalar'}",
                    self._token_stream[self.token_index][1][0]
                )) + '\n'

        # Expect semicolon to end the function call statement.
        if not self.current_token() or self.current_token()[1] != ';':
            self.log += str(SemanticError("Expected ';' after function call", self._token_stream[self.token_index][1][0])) + '\n'
        self.advance()  # Skip ';'

    def function_declaration(self, return_type, func_name):
        # Check for previous declarations or definitions.
        if func_name in self.symbol_table["functions"]:
            existing = self.symbol_table["functions"][func_name]
            if existing["return_type"] != return_type:
                self.log += str(SemanticError(
                    f"Return type mismatch for function '{func_name}' between previous declaration '{existing['return_type']}' and current declaration '{return_type}'", self._token_stream[self.token_index][1][0]
                ))
            func_entry = existing
        else:
            func_entry = {
                "return_type": return_type,
                "parameters": None,
                "locals": {},
                "defined": None
            }
            self.symbol_table["functions"][func_name] = func_entry

        if not self.current_token() or self.current_token()[1] != '(':
            self.log += str(SemanticError("Expected '(' after function name", self._token_stream[self.token_index][1][0])) + '\n'
        self.advance()  # Skip '('

        parameters = []
        while self.current_token() and self.current_token()[1] != ')':
            if self.current_token()[1] in ['anda', 'andamhie', 'chika', 'eklabool']:
                param_type = self.current_token()[1]
                self.advance()  # Skip parameter type
                if not self.current_token() or self.current_token()[1] != 'id':
                    self.log += str(SemanticError("Expected parameter name in function declaration", self._token_stream[self.token_index][1][0])) + '\n'
                param_name = self.current_token()[0]
                # Check if parameter is an array (by seeing if next token is '[' ']')
                self.advance()  # Skip parameter name
                is_array_param = False
                if self.current_token() and self.current_token()[1] == '[':
                    self.advance()
                    if not self.current_token() or self.current_token()[1] != ']':
                        self.log += str(SemanticError("Expected ']' after '[' in parameter array declaration", self._token_stream[self.token_index][1][0])) + '\n'
                    else:
                        self.advance()  # Skip ']'
                    is_array_param = True

                parameters.append((param_name, param_type, is_array_param))
                if self.current_token() and self.current_token()[1] == ',':
                    self.advance()  # Skip comma
                elif self.current_token() and self.current_token()[1] != ')':
                    self.log += str(SemanticError("Expected ',' or ')' in parameter list", self._token_stream[self.token_index][1][0])) + '\n'
            else:
                self.log += str(SemanticError("Unexpected token in parameter list", self._token_stream[self.token_index][1][0])) + '\n'
        if not self.current_token() or self.current_token()[1] != ')':
            self.log += str(SemanticError("Missing closing parenthesis in function declaration", self._token_stream[self.token_index][1][0])) + '\n'
        self.advance()  # Skip ')'

        if not self.current_token():
            self.log += str(SemanticError("Unexpected end of input after function parameters", self._token_stream[self.token_index][1][0])) + '\n'
        
        is_prototype = self.current_token()[1] == ';'
        
        if func_entry["parameters"] is not None:
            if is_prototype and not func_entry["defined"]:
                self.log += str(SemanticError(f"Redeclaration of function prototype '{func_name}'", self._token_stream[self.token_index][1][0])) + '\n'
            if func_entry["defined"] is True and not is_prototype:
                self.log += str(SemanticError(f"Redefinition of function '{func_name}'", self._token_stream[self.token_index][1][0])) + '\n'
            if func_entry["parameters"] != parameters:
                self.log += str(SemanticError(
                    f"Parameter list mismatch for function '{func_name}' between previous declaration and current declaration", self._token_stream[self.token_index][1][0]
                ))
        else:
            func_entry["parameters"] = parameters

        if is_prototype:
            if func_entry["defined"] is True:
                self.log += str(SemanticError(f"Function '{func_name}' already defined, cannot declare as prototype", self._token_stream[self.token_index][1][0])) + '\n'
            func_entry["defined"] = False
            self.advance()  # Skip ';'
        elif self.current_token() and self.current_token()[1] == '{':
            self.advance()  # Skip '{'
            self.current_function = func_name
            func_entry["defined"] = True
            func_entry["has_return"] = False
            # Process function body statements until the matching '}'
            self.process_statements('}')
            if not self.current_token() or self.current_token()[1] != '}':
                self.log += str(SemanticError("Expected '}' at end of function body", self._token_stream[self.token_index][1][0])) + '\n'
            index = self.token_index if self.token_index < len(self._token_stream) else -1
            self.advance()  # Skip '}'
            if func_entry["return_type"] != "shimenet" and not func_entry.get("has_return", False):
                self.log += str(SemanticError(f"Function '{func_name}' with return type '{func_entry['return_type']}' must return a value", self._token_stream[index][1][0])) + '\n'
            self.current_function = None
        else:
            self.log += str(SemanticError("Expected ';' or '{' after function parameter list", self._token_stream[self.token_index][1][0])) + '\n'

    # --- Methods for block scoping and conditionals ---

    def enter_block_scope(self):
        self.block_scopes.append({})

    def exit_block_scope(self):
        self.block_scopes.pop()

    def process_statements(self, terminator):
        """
        Processes statements until a token with value equal to terminator is encountered.
        If terminator is None, processes until end of token stream.
        """
        while self.current_token() and (terminator is None or self.current_token()[1] != terminator):
            token = self.current_token()
            if token[1] == '{':
                self.process_block()
            elif token[1] in ['naur', 'anda', 'andamhie', 'chika', 'eklabool', 'shimenet']:
                self.handle_declaration()
            elif token[1] == 'pak':
                self.process_conditional_statement()
            elif token[1] == 'serve':
                self.process_serve_statement()
            elif token[1] == 'adele':
                self.process_adele_statement()
            elif token[1] == 'adelete':
                self.process_adelete_statement()
            elif token[1] == 'push':
                self.process_push_statement()
            elif token[1] == 'keri':
                if self.next_token() and self.next_token()[1] == 'lang':
                    self.process_do_while_loop()
                else:
                    self.process_while_loop()
            elif token[1] == 'versa':
                self.process_switch_statement()
            elif token[1] == 'forda':
                self.process_forda_loop()
            elif token[1] == 'id' and self.next_token() and self.next_token()[1] == '(':
                self.process_function_call()
            elif token[1] == 'id' and self.next_token() and self.next_token()[1] in ['=', '+=', '-=', '*=', '/=', '%=', '**=', '//=']:
                self.process_assignment_statement()
            else:
                self.advance()

    def process_block(self):
        """
        Processes a block delimited by '{' and '}'.
        Pushes a new block scope, processes the statements in the block, and pops the scope.
        """
        if not self.current_token() or self.current_token()[1] != '{':
            self.log += str(SemanticError("Expected '{' to start block", self._token_stream[self.token_index][1][0])) + '\n'
        self.advance()  # Skip '{'
        self.enter_block_scope()
        self.process_statements('}')
        if not self.current_token() or self.current_token()[1] != '}':
            self.log += str(SemanticError("Expected '}' to end block", self._token_stream[self.token_index][1][0])) + '\n'
        self.advance()  # Skip '}'
        self.exit_block_scope()

    def process_conditional_statement(self):
        """
        Processes a conditional statement with support for:
            - if (pak)
            - else if (ganern pak)
            - else (ganern)
        Each block inside the conditional gets its own scope.
        The condition expression is evaluated (without enforcing a specific type).
        """
        # Process the initial if clause.
        if not self.current_token() or self.current_token()[1] != 'pak':
            self.log += str(SemanticError("Expected 'pak' for if statement", self._token_stream[self.token_index][1][0])) + '\n'
        self.advance()  # Skip 'pak'
        if not self.current_token() or self.current_token()[1] != '(':
            self.log += str(SemanticError("Expected '(' after 'pak'", self._token_stream[self.token_index][1][0])) + '\n'
        self.advance()  # Skip '('
        self.evaluate_expression()  # Evaluate condition (any type allowed)
        if not self.current_token() or self.current_token()[1] != ')':
            self.log += str(SemanticError("Expected ')' after condition in 'pak'", self._token_stream[self.token_index][1][0])) + '\n'
        self.advance()  # Skip ')'
        self.process_block()  # Process the if block

        # Process optional else if and else clauses.
        while self.current_token() and self.current_token()[1] == 'ganern':
            self.advance()  # Skip 'ganern'
            if self.current_token() and self.current_token()[1] == 'pak':
                # Else if branch.
                self.advance()  # Skip 'pak'
                if not self.current_token() or self.current_token()[1] != '(':
                    self.log += str(SemanticError("Expected '(' after 'ganern pak'", self._token_stream[self.token_index][1][0])) + '\n'
                self.advance()  # Skip '('
                self.evaluate_expression()  # Evaluate condition
                if not self.current_token() or self.current_token()[1] != ')':
                    self.log += str(SemanticError("Expected ')' after condition in 'ganern pak'", self._token_stream[self.token_index][1][0])) + '\n'
                self.advance()  # Skip ')'
                self.process_block()  # Process the else-if block.
            else:
                # Else branch (no condition).
                self.process_block()  # Process the else block.
                break

    # --- New methods for loop constructs ---

    def process_while_loop(self):
        """
        Processes a while loop in the form:
            keri ( condition ) { ... }
        The condition expression can be of any type. A new block scope is created for the loop body.
        """
        # Current token is 'keri'
        self.advance()  # Skip 'keri'
        if not self.current_token() or self.current_token()[1] != '(':
            self.log += str(SemanticError("Expected '(' after 'keri' for while loop condition", self._token_stream[self.token_index][1][0])) + '\n'
        self.advance()  # Skip '('
        # Evaluate the condition (any type is allowed)
        self.evaluate_expression()
        if not self.current_token() or self.current_token()[1] != ')':
            self.log += str(SemanticError("Expected ')' after while loop condition", self._token_stream[self.token_index][1][0])) + '\n'
        self.advance()  # Skip ')'
        if not self.current_token() or self.current_token()[1] != '{':
            self.log += str(SemanticError("Expected '{' to start while loop block", self._token_stream[self.token_index][1][0])) + '\n'
        self.process_block()  # The block creates its own scope

    def process_do_while_loop(self):
        """
        Processes a do-while loop in the form:
            keri lang { ... } keri ( condition )
        Here, 'keri lang' together represent the 'do' keyword. The loop body is processed first,
        and then the condition is evaluated.
        """
        # Current token is 'keri' and the next token should be 'lang'
        self.advance()  # Skip 'keri'
        if not self.current_token() or self.current_token()[1] != 'lang':
            self.log += str(SemanticError("Expected 'lang' after 'keri' for do-while loop", self._token_stream[self.token_index][1][0])) + '\n'
        self.advance()  # Skip 'lang'
        if not self.current_token() or self.current_token()[1] != '{':
            self.log += str(SemanticError("Expected '{' to start do-while loop block", self._token_stream[self.token_index][1][0])) + '\n'
        self.process_block()  # Process the loop body block with its own scope
        if not self.current_token() or self.current_token()[1] != 'keri':
            self.log += str(SemanticError("Expected 'keri' after do-while loop block for loop condition", self._token_stream[self.token_index][1][0])) + '\n'
        self.advance()  # Skip 'keri'
        if not self.current_token() or self.current_token()[1] != '(':
            self.log += str(SemanticError("Expected '(' after 'keri' in do-while loop condition", self._token_stream[self.token_index][1][0])) + '\n'
        self.advance()  # Skip '('
        self.evaluate_expression()  # Evaluate loop condition
        if not self.current_token() or self.current_token()[1] != ')':
            self.log += str(SemanticError("Expected ')' after do-while loop condition", self._token_stream[self.token_index][1][0])) + '\n'
        self.advance()  # Skip ')'

    def process_switch_statement(self):
        """
        Processes a switch statement using:
            versa ( expression ) { case_clauses }
        where:
            - 'versa' is the switch keyword,
            - each case clause begins with 'betsung' followed by an expression and ':'.
            - the default clause is 'ditech' followed by ':'.
        Each case clause is processed in its own block scope.
        """
        # Current token is 'versa'
        self.advance()  # Skip 'versa'
        if not self.current_token() or self.current_token()[1] != '(':
            self.log += str(SemanticError("Expected '(' after 'versa'", self._token_stream[self.token_index][1][0])) + '\n'
        self.advance()  # Skip '('
        switch_expr_type = self.evaluate_expression()
        if not self.current_token() or self.current_token()[1] != ')':
            self.log += str(SemanticError("Expected ')' after switch expression", self._token_stream[self.token_index][1][0])) + '\n'
        self.advance()  # Skip ')'
        if not self.current_token() or self.current_token()[1] != '{':
            self.log += str(SemanticError("Expected '{' to start switch block", self._token_stream[self.token_index][1][0])) + '\n'
        self.advance()  # Skip '{'
        # Enter a new block scope for the entire switch statement.
        self.enter_block_scope()
        default_found = False
        while self.current_token() and self.current_token()[1] != '}':
            token = self.current_token()
            if token[1] == 'betsung':
                self.advance()  # Skip 'betsung'
                # Evaluate the case label expression.
                case_expr_type = self.evaluate_expression()
                if not self.is_type_compatible(switch_expr_type, case_expr_type):
                    self.log += str(SemanticError(f"Case label type '{case_expr_type}' is not compatible with switch expression type '{switch_expr_type}'", self._token_stream[self.token_index][1][0])) + '\n'
                if not self.current_token() or self.current_token()[1] != ':':
                    self.log += str(SemanticError("Expected ':' after case label", self._token_stream[self.token_index][1][0])) + '\n'
                self.advance()  # Skip ':'
                # Process statements for this case in a new block scope.
                self.enter_block_scope()
                while self.current_token() and self.current_token()[1] not in ['betsung', 'ditech', '}']:
                    token_inner = self.current_token()
                    if token_inner[1] == '{':
                        self.process_block()
                    elif token_inner[1] in ['naur', 'anda', 'andamhie', 'chika', 'eklabool', 'shimenet']:
                        self.handle_declaration()
                    elif token_inner[1] == 'pak':
                        self.process_conditional_statement()
                    elif token_inner[1] == 'serve':
                        self.process_serve_statement()
                    elif token_inner[1] == 'push':
                        self.process_push_statement()
                    elif token_inner[1] == 'keri':
                        if self.next_token() and self.next_token()[1] == 'lang':
                            self.process_do_while_loop()
                        else:
                            self.process_while_loop()
                    elif token_inner[1] == 'versa':
                        self.process_switch_statement()
                    elif token_inner[1] == 'forda':
                        self.process_forda_loop()
                    elif token_inner[1] == 'id' and self.next_token() and self.next_token()[1] == '(':
                        self.process_function_call()
                    elif token_inner[1] == 'id' and self.next_token() and self.next_token()[1] in ['=', '+=', '-=', '*=', '/=', '%=', '**=', '//=']:
                        self.process_assignment_statement()
                    else:
                        self.advance()
                self.exit_block_scope()  # End of this case clause.
            elif token[1] == 'ditech':
                if default_found:
                    self.log += str(SemanticError("Multiple default clauses in switch statement", self._token_stream[self.token_index][1][0])) + '\n'
                default_found = True
                self.advance()  # Skip 'ditech'
                if not self.current_token() or self.current_token()[1] != ':':
                    self.log += str(SemanticError("Expected ':' after default clause", self._token_stream[self.token_index][1][0])) + '\n'
                self.advance()  # Skip ':'
                # Process default clause statements in a new block scope.
                self.enter_block_scope()
                while self.current_token() and self.current_token()[1] not in ['betsung', '}']:
                    token_inner = self.current_token()
                    if token_inner[1] == '{':
                        self.process_block()
                    elif token_inner[1] in ['naur', 'anda', 'andamhie', 'chika', 'eklabool', 'shimenet']:
                        self.handle_declaration()
                    elif token_inner[1] == 'pak':
                        self.process_conditional_statement()
                    elif token_inner[1] == 'serve':
                        self.process_serve_statement()
                    elif token_inner[1] == 'push':
                        self.process_push_statement()
                    elif token_inner[1] == 'keri':
                        if self.next_token() and self.next_token()[1] == 'lang':
                            self.process_do_while_loop()
                        else:
                            self.process_while_loop()
                    elif token_inner[1] == 'versa':
                        self.process_switch_statement()
                    elif token_inner[1] == 'forda':
                        self.process_forda_loop()
                    elif token_inner[1] == 'id' and self.next_token() and self.next_token()[1] == '(':
                        self.process_function_call()
                    elif token_inner[1] == 'id' and self.next_token() and self.next_token()[1] in ['=', '+=', '-=', '*=', '/=', '%=', '**=', '//=']:
                        self.process_assignment_statement()
                    else:
                        self.advance()
                self.exit_block_scope()  # End of default clause.
            else:
                self.log += str(SemanticError("Expected 'betsung' or 'ditech' in switch block", self._token_stream[self.token_index][1][0])) + '\n'
        if not self.current_token() or self.current_token()[1] != '}':
            self.log += str(SemanticError("Expected '}' to close switch block", self._token_stream[self.token_index][1][0])) + '\n'
        self.advance()  # Skip '}'
        self.exit_block_scope()  # Exit the switch block scope.

    def is_type_compatible(self, switch_type, case_type):
        """
        Checks if the case label type is compatible with the switch expression type.
        For numeric types (anda and andamhie), we allow either numeric or eklabool.
        For chika, must match exactly.
        For eklabool, accept eklabool, anda, or andamhie.
        """
        if switch_type == case_type:
            return True
        if switch_type in ['anda', 'andamhie', 'eklabool'] and case_type in ['anda', 'andamhie', 'eklabool']:
            return True
        return False

    # --- New method for for loop construct ---
    def process_forda_loop(self):
        """
        Processes a for loop in the form:
            forda ( [<type>]? <id> from <start_expr> to <end_expr> [step <step_expr>] ) { ... }
        The loop header may optionally declare a new loop variable. In that case, the variable
        must not already be declared in an enclosing scope. Otherwise, the variable must already exist.
        The expressions for 'from', 'to', and (optionally) 'step' must be numeric (i.e. evaluate to 'anda' or 'andamhie' or 'eklabool').
        A new block scope is created for the loop body.
        """
        self.advance()  # Skip 'forda'
        if not self.current_token() or self.current_token()[1] != '(':
            self.log += str(SemanticError("Expected '(' after 'forda'", self._token_stream[self.token_index][1][0])) + '\n'
        self.advance()  # Skip '('

        # Determine if there is a new declaration in the loop header.
        new_declaration = False
        declared_type = None
        loop_var_name = None
        loop_var_type = None

        if self.current_token() and self.current_token()[1] in ['anda', 'andamhie', 'chika', 'eklabool']:
            # Ensure only numeric types are used for loop variables (per the original design).
            declared_type = self.current_token()[1]
            if declared_type not in ['anda', 'andamhie']:
                self.log += str(SemanticError(f"For loop iteration variable must be numeric, got type '{declared_type}'", self._token_stream[self.token_index][1][0])) + '\n'
            new_declaration = True
            self.advance()  # Skip type token
            if not self.current_token() or self.current_token()[1] != 'id':
                self.log += str(SemanticError("Expected identifier for for loop variable declaration", self._token_stream[self.token_index][1][0])) + '\n'
            loop_var_name = self.current_token()[0]
            loop_var_type = declared_type  # Store type for later validation
            self.advance()  # Skip identifier
        else:
            # Otherwise, expect an identifier.
            if not self.current_token() or self.current_token()[1] != 'id':
                self.log += str(SemanticError("Expected identifier for for loop variable", self._token_stream[self.token_index][1][0])) + '\n'
            loop_var_name = self.current_token()[0]
            self.advance()  # Skip identifier

            # Validate that the existing variable is already declared and is numeric.
            var_entry = None
            if self.current_function:
                for scope in reversed(self.block_scopes):
                    if loop_var_name in scope:
                        var_entry = scope[loop_var_name]
                        break
                if not var_entry:
                    if loop_var_name in self.symbol_table["functions"][self.current_function]["locals"]:
                        var_entry = self.symbol_table["functions"][self.current_function]["locals"][loop_var_name]
                    elif any(param[0] == loop_var_name for param in self.symbol_table["functions"][self.current_function]["parameters"]):
                        self.log += str(SemanticError(f"Loop variable '{loop_var_name}' cannot be a function parameter", self._token_stream[self.token_index][1][0])) + '\n'
                    elif loop_var_name in self.symbol_table["variables"]:
                        var_entry = self.symbol_table["variables"][loop_var_name]
            else:
                if loop_var_name in self.symbol_table["variables"]:
                    var_entry = self.symbol_table["variables"][loop_var_name]

            if not var_entry:
                self.log += str(SemanticError(f"For loop variable '{loop_var_name}' is not declared", self._token_stream[self.token_index][1][0])) + '\n'

            loop_var_type = var_entry["data_type"]

            if loop_var_type not in ['anda', 'andamhie']:
                self.log += str(SemanticError(f"For loop variable '{loop_var_name}' must be numeric, but it is '{loop_var_type}'", self._token_stream[self.token_index][1][0])) + '\n'

        # Expect 'from'
        if not self.current_token() or self.current_token()[1] != 'from':
            self.log += str(SemanticError("Expected 'from' in for loop header", self._token_stream[self.token_index][1][0])) + '\n'
        self.advance()  # Skip 'from'

        # Evaluate start expression.
        start_expr_type = self.evaluate_expression()
        if start_expr_type not in ['anda', 'andamhie', 'eklabool']:
            self.log += str(SemanticError("For loop 'from' expression must be numeric or boolean", self._token_stream[self.token_index][1][0])) + '\n'

        # Expect 'to'
        if not self.current_token() or self.current_token()[1] != 'to':
            self.log += str(SemanticError("Expected 'to' in for loop header", self._token_stream[self.token_index][1][0])) + '\n'
        self.advance()  # Skip 'to'

        # Evaluate end expression.
        end_expr_type = self.evaluate_expression()
        if end_expr_type not in ['anda', 'andamhie', 'eklabool']:
            self.log += str(SemanticError("For loop 'to' expression must be numeric or boolean", self._token_stream[self.token_index][1][0])) + '\n'

        # Optionally handle 'step'
        if self.current_token() and self.current_token()[1] == 'step':
            self.advance()  # Skip 'step'
            step_expr_type = self.evaluate_expression()
            if step_expr_type not in ['anda', 'andamhie', 'eklabool']:
                self.log += str(SemanticError("For loop 'step' expression must be numeric or boolean", self._token_stream[self.token_index][1][0])) + '\n'

        if not self.current_token() or self.current_token()[1] != ')':
            self.log += str(SemanticError("Expected ')' after for loop header", self._token_stream[self.token_index][1][0])) + '\n'
        self.advance()  # Skip ')'

        # Enter a new block scope for the for loop header.
        self.enter_block_scope()

        if new_declaration:
            # Check that the loop variable is not already declared in any enclosing scope.
            if self.variable_exists_in_enclosing_scopes(loop_var_name):
                self.log += str(SemanticError(f"Redeclaration of variable '{loop_var_name}' in for loop header is not allowed", self._token_stream[self.token_index][1][0])) + '\n'
            # Register the new loop variable in the current (for loop header) block scope.
            entry = {
                "data_type": declared_type,
                "value": None,
                "naur_flag": False,
                "is_array": False
            }
            self.block_scopes[-1][loop_var_name] = entry

        # Process the loop body.
        if not self.current_token() or self.current_token()[1] != '{':
            self.log += str(SemanticError("Expected '{' to start for loop block", self._token_stream[self.token_index][1][0])) + '\n'
        self.process_block()

        # Exit the for loop header's scope.
        self.exit_block_scope()

    # --- Expression Type Checking Methods ---
    def evaluate_expression(self):
        """
        Entry point for expression type-checking.
        Returns one of: 'anda', 'andamhie', 'chika', 'eklabool', or 'givenchy'.
        """
        return self.parse_logical_or()

    def parse_logical_or(self):
        left_type = self.parse_logical_and()
        while self.current_token() and self.current_token()[1] == '||':
            self.advance()  # Skip '||'
            right_type = self.parse_logical_and()
            if self._is_array_type(left_type) or self._is_array_type(right_type):
                pos = self._token_stream[self.token_index][1][0] if self.token_index < len(self._token_stream) else -1
                self.log += str(SemanticError(
                    "Array variables cannot participate in expressions",
                    pos)) + '\n'
                left_type = 'anda'
                continue
            for t in (left_type, right_type):
                if t not in ['anda', 'andamhie', 'eklabool', 'chika', 'givenchy']:
                    self.log += str(SemanticError(f"Invalid operand type '{t}' for logical operator '||'", self._token_stream[self.token_index][1][0])) + '\n'
            left_type = 'eklabool'
        return left_type

    def parse_logical_and(self):
        left_type = self.parse_equality()
        while self.current_token() and self.current_token()[1] == '&&':
            self.advance()  # Skip '&&'
            right_type = self.parse_equality()
            if self._is_array_type(left_type) or self._is_array_type(right_type):
                pos = self._token_stream[self.token_index][1][0] if self.token_index < len(self._token_stream) else -1
                self.log += str(SemanticError(
                    "Array variables cannot participate in expressions",
                    pos)) + '\n'
                left_type = 'anda'
                continue
            for t in (left_type, right_type):
                if t not in ['anda', 'andamhie', 'eklabool', 'chika', 'givenchy']:
                    self.log += str(SemanticError(f"Invalid operand type '{t}' for logical operator '&&'", self._token_stream[self.token_index][1][0])) + '\n'
            left_type = 'eklabool'
        return left_type

    def parse_equality(self):
        left_type = self.parse_relational()
        while self.current_token() and self.current_token()[1] in ['==', '!=']:
            op = self.current_token()[1]
            self.advance()
            right_type = self.parse_relational()
            if self._is_array_type(left_type) or self._is_array_type(right_type):
                pos = self._token_stream[self.token_index][1][0] if self.token_index < len(self._token_stream) else -1
                self.log += str(SemanticError(
                    "Array variables cannot participate in expressions",
                    pos)) + '\n'
                left_type = 'anda'
                continue
            if left_type not in ['anda', 'andamhie', 'eklabool', 'chika', 'givenchy'] or right_type not in ['anda', 'andamhie', 'eklabool', 'chika', 'givenchy']:
                self.log += str(SemanticError("Invalid types for equality operator", self._token_stream[self.token_index][1][0])) + '\n'
            left_type = 'eklabool'
        return left_type

    def parse_relational(self):
        left_type = self.parse_additive()
        while self.current_token() and self.current_token()[1] in ['<', '<=', '>', '>=']:
            op = self.current_token()[1]
            self.advance()
            right_type = self.parse_additive()
            if self._is_array_type(left_type) or self._is_array_type(right_type):
                pos = self._token_stream[self.token_index][1][0] if self.token_index < len(self._token_stream) else -1
                self.log += str(SemanticError(
                    "Array variables cannot participate in expressions",
                    pos)) + '\n'
                left_type = 'anda'
                continue
            if left_type not in ['anda', 'andamhie', 'eklabool', 'givenchy'] or right_type not in ['anda', 'andamhie', 'eklabool', 'givenchy']:
                self.log += str(SemanticError("Invalid types for relational operator", self._token_stream[self.token_index][1][0])) + '\n'
            left_type = 'eklabool'
        return left_type

    def parse_additive(self):
        """
        Handles + and -.
        - If op is '+', and at least one side is 'chika', the result is 'chika'.
        - Otherwise both must be numeric/boolean: anda, andamhie, eklabool, or givenchy.
        """
        left_type = self.parse_multiplicative()
        while self.current_token() and self.current_token()[1] in ['+', '-']:
            op = self.current_token()[1]
            self.advance()  # consume '+' or '-'

            # Save the allow-flag so we restore it after parsing RHS
            saved_allow = self.allow_unindexed_array_usage

            # Parse the right side
            right_type = self.parse_multiplicative()

            if self._is_array_type(left_type) or self._is_array_type(right_type):
                pos = self._token_stream[self.token_index][1][0] if self.token_index < len(self._token_stream) else -1
                self.log += str(SemanticError(
                    "Array variables cannot participate in expressions",
                    pos)) + '\n'
                left_type = 'anda'
                continue

            # Restore the original allow-flag
            self.allow_unindexed_array_usage = saved_allow

            if op == '+':
                # Flexible concatenation: If either side is chika, result is chika
                if left_type == 'chika' or right_type == 'chika':
                    result_type = 'chika'
                else:
                    # Normal numeric addition/subtraction rules
                    if left_type not in ['anda', 'andamhie', 'eklabool', 'givenchy'] \
                    or right_type not in ['anda', 'andamhie', 'eklabool', 'givenchy']:
                        pos = self._token_stream[self.token_index][1][0] if self.token_index < len(self._token_stream) else -1
                        self.log += str(SemanticError("Invalid types for arithmetic addition", pos)) + '\n'
                        result_type = 'invalid'
                    else:
                        result_type = 'andamhie'
            elif op == '-':
                # Subtraction: must be purely numeric/boolean
                if left_type not in ['anda', 'andamhie', 'eklabool', 'givenchy'] \
                or right_type not in ['anda', 'andamhie', 'eklabool', 'givenchy']:
                    pos = self._token_stream[self.token_index][1][0] if self.token_index < len(self._token_stream) else -1
                    self.log += str(SemanticError("Invalid types for arithmetic subtraction", pos)) + '\n'
                    result_type = 'invalid'
                else:
                    result_type = 'andamhie'

            left_type = result_type

        return left_type

    def parse_multiplicative(self):
        left_type = self.parse_unary()
        while self.current_token() and self.current_token()[1] in ['*', '/', '%', '**', '//']:
            op = self.current_token()[1]
            self.advance()
            right_type = self.parse_unary()
            if self._is_array_type(left_type) or self._is_array_type(right_type):
                pos = self._token_stream[self.token_index][1][0] if self.token_index < len(self._token_stream) else -1
                self.log += str(SemanticError(
                    "Array variables cannot participate in expressions",
                    pos)) + '\n'
                left_type = 'anda'
                continue
            if left_type not in ['anda', 'andamhie', 'eklabool', 'givenchy'] or right_type not in ['anda', 'andamhie', 'eklabool', 'givenchy']:
                self.log += str(SemanticError("Invalid types for arithmetic multiplicative operation", self._token_stream[self.token_index][1][0])) + '\n'
            left_type = 'andamhie'
        return left_type

    def parse_unary(self):
        token = self.current_token()
        if token and token[1] in ['!', '-', '++', '--']:
            op = token[1]
            self.advance()
            if op in ['++', '--']:
                operand_token = self.current_token()
                if not operand_token or operand_token[1] != 'id':
                    self.log += str(SemanticError(f"Operator '{op}' must be applied to an identifier", self._token_stream[self.token_index][1][0])) + '\n'
                var_name = operand_token[0]
                var_entry = None
                if self.current_function:
                    # Check in block scopes first.
                    for scope in reversed(self.block_scopes):
                        if var_name in scope:
                            var_entry = scope[var_name]
                            break
                    if not var_entry:
                        if var_name in self.symbol_table["functions"][self.current_function]["locals"]:
                            var_entry = self.symbol_table["functions"][self.current_function]["locals"][var_name]
                        elif any(param[0] == var_name for param in self.symbol_table["functions"][self.current_function]["parameters"]):
                            self.log += str(SemanticError(f"Operator '{op}' cannot be applied to immutable parameter '{var_name}'", self._token_stream[self.token_index][1][0])) + '\n'
                else:
                    if var_name in self.symbol_table["variables"]:
                        var_entry = self.symbol_table["variables"][var_name]
                if not var_entry:
                    self.log += str(SemanticError(f"Undefined variable '{var_name}' for operator '{op}'", self._token_stream[self.token_index][1][0])) + '\n'
                if var_entry and var_entry["naur_flag"]:
                    self.log += str(SemanticError(f"Operator '{op}' cannot be applied to constant variable '{var_name}'", self._token_stream[self.token_index][1][0])) + '\n'
                self.advance()  # Consume identifier.
                return var_entry["data_type"] if var_entry else 'anda'
            elif op == '-':
                operand_type = self.parse_unary()
                if operand_type not in ['anda', 'andamhie', 'eklabool', 'givenchy']:
                    self.log += str(SemanticError("Unary minus can only be applied to numeric or boolean types", self._token_stream[self.token_index][1][0])) + '\n'
                return 'andamhie'
            elif op == '!':
                operand_type = self.parse_unary()
                if operand_type not in ['anda', 'andamhie', 'eklabool', 'chika', 'givenchy']:
                    self.log += str(SemanticError("Logical not can only be applied to numeric, boolean, or string types", self._token_stream[self.token_index][1][0])) + '\n'
                return 'eklabool'
        else:
            return self.parse_primary()

    def parse_primary(self):
        token = self.current_token()
        if not token:
            pos = (self._token_stream[self.token_index][1][0]
                   if self.token_index < len(self._token_stream) else -1)
            self.log += str(SemanticError("Unexpected end of expression", pos)) + '\n'
            return 'anda'

        # ─── built-in givenchy(...) ───
        if token[1] == 'givenchy':
            self.advance()  # skip 'givenchy'
            if not self.current_token() or self.current_token()[1] != '(':
                pos = self._token_stream[self.token_index][1][0]
                self.log += str(SemanticError("Expected '(' after 'givenchy'", pos)) + '\n'
            self.advance()  # skip '('
            if not self.current_token() or self.current_token()[1] != 'chika_literal':
                pos = self._token_stream[self.token_index][1][0]
                self.log += str(SemanticError("Expected string literal for 'givenchy'", pos)) + '\n'
            self.advance()  # skip literal
            if not self.current_token() or self.current_token()[1] != ')':
                pos = self._token_stream[self.token_index][1][0]
                self.log += str(SemanticError("Expected ')' after 'givenchy' argument", pos)) + '\n'
            self.advance()  # skip ')'
            return "givenchy"

        # --- built-in len(...) with up to 3-dimension support ---
        if token[1] == 'id' and token[0] == 'len' and self.next_token() and self.next_token()[1] == '(':
            pos = self._token_stream[self.token_index][1][0]
            self.advance()  # skip 'len'
            self.advance()  # skip '('

            # must start with an identifier or a string literal
            if not self.current_token() or self.current_token()[1] not in ['id', 'chika_literal']:
                self.log += str(SemanticError("len() argument must be an array or a string literal", pos)) + '\n'
                # recover to closing ')'
                while self.current_token() and self.current_token()[1] != ')':
                    self.advance()
                if self.current_token():
                    self.advance()
                return 'anda'

            is_literal = self.current_token()[1] == 'chika_literal'
            name = self.current_token()[0]
            entry = self.lookup_variable(name) if not is_literal else None
            self.advance()  # skip identifier or literal

            if not is_literal and entry:
                if not entry.get("is_array", False) and entry.get("data_type") != "chika":
                    self.log += str(SemanticError(
                        "len() argument must be an array or a chika",
                        pos)) + '\n'

            # collect up to three [literal] indexes
            indexes = []
            while self.current_token() and self.current_token()[1] == '[':
                self.advance()  # skip '['
                idx_tok = self.current_token()
                if not idx_tok or idx_tok[1] != 'anda_literal':
                    self.log += str(SemanticError("len() index must be a numeric literal", pos)) + '\n'
                    # skip until ']' or ')'
                    while self.current_token() and self.current_token()[1] not in [']', ')']:
                        self.advance()
                    if not self.current_token() or self.current_token()[1] != ']':
                        self.log += str(SemanticError("Missing ']' in len() argument", pos)) + '\n'
                    break
                idx = int(idx_tok[0])
                indexes.append(idx)
                self.advance()  # skip literal
                if not self.current_token() or self.current_token()[1] != ']':
                    self.log += str(SemanticError("Missing ']' in len() argument", pos)) + '\n'
                    break
                self.advance()  # skip ']'

            # expect closing ')'
            if not self.current_token() or self.current_token()[1] != ')':
                self.log += str(SemanticError("Missing ')' after len()", pos)) + '\n'
            else:
                self.advance()

            if not is_literal:
                # compile-time initializer validation
                init_val = entry.get("value") if entry else None
                for idx in indexes:
                    if isinstance(init_val, list) and 0 <= idx < len(init_val):
                        if not isinstance(init_val[idx], list):
                            self.log += str(SemanticError(
                                f"len() argument at index {idx} is not an array",
                                pos)) + '\n'
                        init_val = init_val[idx]
                    else:
                        break

            return 'anda'

        # ─── literals: anda_literal, chika_literal, etc. ───
        if token[1].endswith('_literal'):
            lit_type = token[1].split('_')[0]
            self.advance()
            # allow string-indexing: "abc"[i]
            if lit_type == 'chika' and self.current_token() and self.current_token()[1] == '[':
                self.advance()
                idx_t = self.evaluate_expression()
                if idx_t not in ['anda', 'andamhie']:
                    p = self._token_stream[self.token_index][1][0]
                    self.log += str(SemanticError("String index must be numeric", p)) + '\n'
                if not self.current_token() or self.current_token()[1] != ']':
                    p = self._token_stream[self.token_index][1][0]
                    self.log += str(SemanticError("Missing ']' after string index", p)) + '\n'
                self.advance()
                return 'chika'
            return lit_type

        # ─── boolean literals ───
        if token[1] in ['korik', 'eme']:
            self.advance()
            return 'eklabool'

        # ─── identifier: variable, array access, or inline function call ───
        if token[1] == 'id':
            var_name = token[0]
            self.advance()

            # inline function-call
            if self.current_token() and self.current_token()[1] == '(':
                return self._parse_inline_function_call(var_name)

            # array indexing
            idx_count = 0
            while self.current_token() and self.current_token()[1] == '[':
                idx_count += 1
                self.advance()
                t = self.evaluate_expression()
                if t not in ['anda', 'andamhie']:
                    p = self._token_stream[self.token_index][1][0]
                    self.log += str(SemanticError("Array index must be numeric", p)) + '\n'
                if not self.current_token() or self.current_token()[1] != ']':
                    p = self._token_stream[self.token_index][1][0]
                    self.log += str(SemanticError("Missing ']' in array access", p)) + '\n'
                self.advance()

            entry = self.lookup_variable(var_name)
            if not entry:
                p = self._token_stream[self.token_index][1][0]
                self.log += str(SemanticError(f"Undeclared variable '{var_name}'", p)) + '\n'
                return 'anda'

            base   = entry["data_type"]
            is_arr = entry.get("is_array", False)
            dims   = entry.get("dimensions", [])

            if is_arr:
                if idx_count == 0:
                    if not self.allow_unindexed_array_usage:
                        p = self._token_stream[self.token_index][1][0]
                        self.log += str(SemanticError(
                            f"Array '{var_name}' cannot be used directly in expressions; index it",
                            p)) + '\n'
                    return f"array_{base}"
                else:
                    if idx_count < len(dims):
                        return f"array_{base}"
                    else:
                        return base
            # scalar
            while self.current_token() and self.current_token()[1] in ['++', '--']:
                self.advance()
            return base

        # ─── parenthesized subexpression ───
        if token[1] == '(':
            self.advance()
            t = self.evaluate_expression()
            if not self.current_token() or self.current_token()[1] != ')':
                p = self._token_stream[self.token_index][1][0]
                self.log += str(SemanticError("Missing ')' in expression", p)) + '\n'
            else:
                self.advance()
            return t

        # anything else is unexpected
        p = self._token_stream[self.token_index][1][0]
        self.log += str(SemanticError(f"Unexpected token '{token[0]}' in expression", p)) + '\n'
        return 'anda'

    def process_serve_statement(self):
        """Process and validate the 'serve' statement (print statement)."""
        if self.current_token()[1] != 'serve':
            self.log += str(SemanticError("Expected 'serve' statement", self._token_stream[self.token_index][1][0])) + '\n'

        self.advance()

        self.allow_unindexed_array_usage = True
        
        if not self.current_token() or self.current_token()[1] != '(':
            self.log += str(SemanticError("Expected '(' after 'serve' statement", self._token_stream[self.token_index][1][0])) + '\n'
        
        self.advance() 
        
        expr_type = self.evaluate_expression()
        
        if expr_type == "chika":
            if self.current_token() and self.current_token()[1] not in [')', ';', '+']:
                self.log += str(SemanticError("Invalid operation: 'chika' type only supports '+' for concatenation", self._token_stream[self.token_index][1][0])) + '\n'
        
        if self.current_token() and self.current_token()[1] == ',':
            self.log += str(SemanticError("Multiple arguments in 'serve' statement are not allowed", self._token_stream[self.token_index][1][0])) + '\n'
        
        if not self.current_token() or self.current_token()[1] != ')':
            self.log += str(SemanticError("Expected ')' at the end of 'serve' statement", self._token_stream[self.token_index][1][0])) + '\n'
        
        self.advance()  
        if not self.current_token() or self.current_token()[1] != ';':
            self.log += str(SemanticError("Expected ';' at the end of 'serve' statement", self._token_stream[self.token_index][1][0])) + '\n'
        
        self.advance()
        self.allow_unindexed_array_usage = False

    def _is_array_type(self, t):
        return isinstance(t, str) and t.startswith("array_")