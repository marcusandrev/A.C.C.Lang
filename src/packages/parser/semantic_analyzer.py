from .error_handler import SemanticError

class SemanticAnalyzer:
    def __init__(self, token_stream):
        self.symbol_table = {
            "variables": {},
            "functions": {}
        }
        self.current_function = None  # None means global scope.
        # Filter out whitespace, newline, and comment tokens.
        self._token_stream = [t for t in token_stream if t[1] not in ['whitespace', 'newline', 'comment']]
        self.token_index = 0

    def current_token(self):
        if 0 <= self.token_index < len(self._token_stream):
            return self._token_stream[self.token_index]
        return None

    def next_token(self):
        next_index = self.token_index + 1
        if next_index < len(self._token_stream):
            return self._token_stream[next_index]
        return None

    def advance(self):
        self.token_index += 1

    def analyze(self):
        try:
            while self.current_token():
                token = self.current_token()
                if token[1] in ['naur', 'anda', 'andamhie', 'chika', 'eklabool', 'shimenet']:
                    self.handle_declaration()
                # Detect function calls: identifier followed by '('
                elif token[1] == 'id' and self.next_token() and self.next_token()[1] == '(':
                    self.process_function_call()
                # Process assignment statements: identifier '=' expression ';'
                elif token[1] == 'id' and self.next_token() and self.next_token()[1] == '=':
                    self.process_assignment_statement()
                else:
                    self.advance()
            self.finalize_functions()
            return True
        except SemanticError as e:
            print(e)
            return False

    def process_function_call(self):
        # Ensure call is inside a function
        if self.current_function is None:
            raise SemanticError("Function calls are only allowed inside function bodies")

        func_name = self.current_token()[0]
        self.advance()  # Move past function name

        # Check if function exists
        if func_name not in self.symbol_table["functions"]:
            raise SemanticError(f"Function '{func_name}' is not declared")
        func_entry = self.symbol_table["functions"][func_name]
        expected_params = func_entry["parameters"]

        self.advance()  # Move past '('
        args = []
        while self.current_token() and self.current_token()[1] != ')':
            # Now evaluate full expressions for arguments
            arg_type = self.evaluate_expression()
            args.append(arg_type)
            # Skip commas if present
            if self.current_token() and self.current_token()[1] == ',':
                self.advance()

        # Validate closing parenthesis
        if not self.current_token() or self.current_token()[1] != ')':
            raise SemanticError(f"Missing ')' in call to '{func_name}'")
        self.advance()  # Skip ')'

        # Skip semicolon if present
        if self.current_token() and self.current_token()[1] == ';':
            self.advance()

        # Validate argument count
        if len(args) != len(expected_params):
            raise SemanticError(f"Function '{func_name}' expects {len(expected_params)} arguments, got {len(args)}")

        # Validate argument types (with implicit conversion)
        for i, (arg_type, param) in enumerate(zip(args, expected_params)):
            param_type = param[1]
            if param_type in ['anda', 'andamhie']:
                if arg_type not in ['anda', 'andamhie', 'eklabool']:
                    raise SemanticError(f"Argument {i+1} of '{func_name}' expects a numeric type, got '{arg_type}'")
            elif param_type == 'eklabool':
                if arg_type not in ['eklabool', 'anda', 'andamhie']:
                    raise SemanticError(f"Argument {i+1} of '{func_name}' expects a boolean type, got '{arg_type}'")
            elif param_type == 'chika':
                # Implicit conversion allowed.
                pass

    def finalize_functions(self):
        for func_name, func_entry in self.symbol_table["functions"].items():
            if not func_entry.get("defined", False):
                raise SemanticError(f"Function '{func_name}' declared but not defined")

    def process_initializer(self, var_type):
        # Evaluate the full expression
        value_type = self.evaluate_expression()
        # Check compatibility based on your rules.
        if var_type in ['anda', 'andamhie']:
            if value_type not in ['anda', 'andamhie', 'eklabool']:
                raise SemanticError(f"Variable of type '{var_type}' cannot be assigned a value of type '{value_type}'")
        elif var_type == 'eklabool':
            if value_type not in ['eklabool', 'anda', 'andamhie']:
                raise SemanticError(f"Variable of type 'eklabool' cannot be assigned a value of type '{value_type}'")
        # For chika, implicit conversion is allowed.
        return value_type

    def process_array_dimensions(self):
        dims = []
        while self.current_token() and self.current_token()[1] == '[':
            self.advance()  # Skip '['
            if not self.current_token() or not self.current_token()[1].endswith('_literal'):
                raise SemanticError("Expected literal for array dimension size")
            dim_str = self.current_token()[0]
            try:
                dim = int(dim_str)
            except ValueError:
                raise SemanticError("Array dimension must be an integer")
            dims.append(dim)
            self.advance()  # Skip literal
            if not self.current_token() or self.current_token()[1] != ']':
                raise SemanticError("Expected ']' after array dimension size")
            self.advance()  # Skip ']'
            if len(dims) > 3:
                raise SemanticError("Arrays cannot have more than 3 dimensions")
        return dims

    def process_array_initializer(self, dimensions, var_type, dim_index=0):
        """
        Recursively processes an array initializer list.
        It collects elements until the matching closing brace is encountered.
        This method does not enforce that the number of elements exactly matches the declared dimensions.
        """
        if not self.current_token() or self.current_token()[1] != '{':
            raise SemanticError("Expected '{' to start array initializer")
        self.advance()  # Skip '{'
        init_list = []
        while self.current_token() and self.current_token()[1] != '}':
            # If a nested initializer list is encountered, recurse.
            if self.current_token()[1] == '{':
                element = self.process_array_initializer(dimensions, var_type, dim_index + 1)
            else:
                # Evaluate full expression for each element.
                element_type = self.evaluate_expression()
                if var_type in ['anda', 'andamhie']:
                    if element_type not in ['anda', 'andamhie', 'eklabool']:
                        raise SemanticError(f"Array of type '{var_type}' cannot have element of type '{element_type}'")
                elif var_type == 'eklabool':
                    if element_type not in ['eklabool', 'anda', 'andamhie']:
                        raise SemanticError(f"Array of type 'eklabool' cannot have element of type '{element_type}'")
                # For chika, implicit conversion is allowed.
                element = element_type
            init_list.append(element)
            if self.current_token() and self.current_token()[1] == ',':
                self.advance()
        if not self.current_token() or self.current_token()[1] != '}':
            raise SemanticError("Expected '}' at end of array initializer")
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
                raise SemanticError("Constant declaration cannot be a function declaration")
            if self.current_function is not None:
                raise SemanticError("Nested function declarations are not allowed")
            self.advance()  # Skip 'shimenet'
            if self.current_token() and self.current_token()[1] == 'kween':
                func_name = "kween"
                self.advance()
            elif self.current_token() and self.current_token()[1] == 'id':
                func_name = self.current_token()[0]
                self.advance()
            else:
                raise SemanticError("Expected function name after 'shimenet'")
            self.function_declaration('shimenet', func_name)
            return
        if token[1] not in ['anda', 'andamhie', 'chika', 'eklabool']:
            raise SemanticError("Expected a type token after 'naur'" if is_constant else "Expected a type token")
        data_type = token[1]
        self.advance()  # Skip type token
        if not self.current_token() or self.current_token()[1] != 'id':
            raise SemanticError("Expected identifier after type declaration")
        var_name = self.current_token()[0]
        self.advance()  # Skip identifier
        # Check if this is a function declaration (if '(' follows immediately).
        if self.current_token() and self.current_token()[1] == '(':
            if var_name == "kween" and data_type != "shimenet":
                raise SemanticError("Function 'kween' must have return type 'shimenet'")
            self.function_declaration(data_type, var_name)
            return
        # Otherwise, it's a variable declaration.
        self.process_variable_declaration(data_type, var_name, is_constant)
        while self.current_token() and self.current_token()[1] == ',':
            self.advance()  # Skip comma
            if not self.current_token() or self.current_token()[1] != 'id':
                raise SemanticError("Expected identifier after comma in declaration")
            var_name = self.current_token()[0]
            self.advance()  # Skip identifier
            self.process_variable_declaration(data_type, var_name, is_constant)
        if not self.current_token() or self.current_token()[1] != ';':
            raise SemanticError("Missing semicolon at end of declaration")
        self.advance()  # Skip ';'

    def process_variable_declaration(self, data_type, var_name, is_constant):
        is_array = False
        dimensions = None
        initializer_value = None
        if self.current_token() and self.current_token()[1] == '[':
            is_array = True
            dimensions = self.process_array_dimensions()
            if self.current_token() and self.current_token()[1] == '=':
                self.advance()  # Skip '='
                initializer_value = self.process_array_initializer(dimensions, data_type)
        else:
            if self.current_token() and self.current_token()[1] == '=':
                self.advance()  # Skip '='
                initializer_value = self.process_initializer(data_type)
        self.register_variable(data_type, var_name, is_constant, initializer_value, is_array, dimensions)

    def register_variable(self, var_type, var_name, is_constant, initializer_value, is_array=False, dimensions=None):
        if is_array:
            entry = {
                "data_type": var_type,
                "value": initializer_value,
                "naur_flag": is_constant,
                "is_array": True,
                "dimensions": dimensions
            }
        else:
            entry = {
                "data_type": var_type,
                "value": initializer_value,
                "naur_flag": is_constant,
                "is_array": False
            }
        if self.current_function is None:
            if var_name in self.symbol_table["variables"]:
                raise SemanticError(f"Redeclaration of global variable '{var_name}'")
            self.symbol_table["variables"][var_name] = entry
        else:
            params = self.symbol_table["functions"][self.current_function]["parameters"]
            if any(param[0] == var_name for param in params):
                raise SemanticError(f"Local variable '{var_name}' conflicts with a parameter in function '{self.current_function}'")
            if var_name in self.symbol_table["functions"][self.current_function]["locals"]:
                raise SemanticError(f"Redeclaration of local variable '{var_name}' in function '{self.current_function}'")
            self.symbol_table["functions"][self.current_function]["locals"][var_name] = entry

    def process_assignment_statement(self):
        # Process an assignment statement: identifier '=' expression ';'
        ident = self.current_token()[0]
        self.advance()  # Skip identifier
        if not self.current_token() or self.current_token()[1] != '=':
            raise SemanticError("Expected '=' in assignment statement")
        self.advance()  # Skip '='
        expr_type = self.evaluate_expression()
        if not self.current_token() or self.current_token()[1] != ';':
            raise SemanticError("Expected ';' at end of assignment statement")
        self.advance()  # Skip ';'
        
        # Check if the identifier was declared.
        declared = False
        entry = None
        if self.current_function is not None:
            if ident in self.symbol_table["functions"][self.current_function]["locals"]:
                declared = True
                entry = self.symbol_table["functions"][self.current_function]["locals"][ident]
            elif any(param[0] == ident for param in self.symbol_table["functions"][self.current_function]["parameters"]):
                raise SemanticError(f"Assignment to immutable parameter '{ident}' is not allowed")
            elif ident in self.symbol_table["variables"]:
                declared = True
                entry = self.symbol_table["variables"][ident]
        else:
            if ident in self.symbol_table["variables"]:
                declared = True
                entry = self.symbol_table["variables"][ident]
        if not declared:
            if self.current_function is not None:
                raise SemanticError(f"Assignment to undeclared variable '{ident}' in function '{self.current_function}'")
            else:
                raise SemanticError(f"Assignment to undeclared global variable '{ident}'")
        
        if entry["naur_flag"]:
            raise SemanticError(f"Assignment to constant variable '{ident}' is not allowed")
        
        # Check type compatibility for assignments.
        var_type = entry["data_type"]
        if var_type in ['anda', 'andamhie']:
            if expr_type not in ['anda', 'andamhie', 'eklabool']:
                raise SemanticError(f"Variable '{ident}' of type '{var_type}' cannot be assigned a value of type '{expr_type}'")
        elif var_type == 'eklabool':
            if expr_type not in ['eklabool', 'anda', 'andamhie']:
                raise SemanticError(f"Variable '{ident}' of type 'eklabool' cannot be assigned a value of type '{expr_type}'")
        # For chika, implicit conversion is allowed.

    def function_declaration(self, return_type, func_name):
        # Check for previous declarations or definitions.
        if func_name in self.symbol_table["functions"]:
            existing = self.symbol_table["functions"][func_name]
            if existing["return_type"] != return_type:
                raise SemanticError(
                    f"Return type mismatch for function '{func_name}' between previous declaration '{existing['return_type']}' and current declaration '{return_type}'"
                )
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
            raise SemanticError("Expected '(' after function name")
        self.advance()  # Skip '('

        parameters = []
        while self.current_token() and self.current_token()[1] != ')':
            if self.current_token()[1] in ['anda', 'andamhie', 'chika', 'eklabool']:
                param_type = self.current_token()[1]
                self.advance()  # Skip parameter type
                if not self.current_token() or self.current_token()[1] != 'id':
                    raise SemanticError("Expected parameter name in function declaration")
                param_name = self.current_token()[0]
                parameters.append((param_name, param_type))
                self.advance()  # Skip parameter name
                if self.current_token() and self.current_token()[1] == ',':
                    self.advance()  # Skip comma
                elif self.current_token() and self.current_token()[1] != ')':
                    raise SemanticError("Expected ',' or ')' in parameter list")
            else:
                raise SemanticError("Unexpected token in parameter list")
        if not self.current_token() or self.current_token()[1] != ')':
            raise SemanticError("Missing closing parenthesis in function declaration")
        self.advance()  # Skip ')'

        if not self.current_token():
            raise SemanticError("Unexpected end of input after function parameters")
        
        is_prototype = self.current_token()[1] == ';'
        
        if func_entry["parameters"] is not None:
            if is_prototype and not func_entry["defined"]:
                raise SemanticError(f"Redeclaration of function prototype '{func_name}'")
            if func_entry["defined"] is True and not is_prototype:
                raise SemanticError(f"Redefinition of function '{func_name}'")
            if func_entry["parameters"] != parameters:
                raise SemanticError(
                    f"Parameter list mismatch for function '{func_name}' between previous declaration and current declaration"
                )
        else:
            func_entry["parameters"] = parameters

        if is_prototype:
            if func_entry["defined"] is True:
                raise SemanticError(f"Function '{func_name}' already defined, cannot declare as prototype")
            func_entry["defined"] = False
            self.advance()  # Skip ';'
        elif self.current_token()[1] == '{':
            self.advance()  # Skip '{'
            self.current_function = func_name
            func_entry["defined"] = True
            brace_depth = 1
            while self.current_token() and brace_depth > 0:
                token = self.current_token()
                if token[1] == '{':
                    brace_depth += 1
                    self.advance()
                elif token[1] == '}':
                    brace_depth -= 1
                    self.advance()
                elif token[1] in ['naur', 'anda', 'andamhie', 'chika', 'eklabool', 'shimenet']:
                    self.handle_declaration()
                elif token[1] == 'id':
                    if self.next_token() and self.next_token()[1] == '(':
                        self.process_function_call()
                    elif self.next_token() and self.next_token()[1] == '=':
                        self.process_assignment_statement()
                    else:
                        self.advance()
                else:
                    self.advance()
            if brace_depth != 0:
                raise SemanticError("Unmatched '{' in function body")
            self.current_function = None
        else:
            raise SemanticError("Expected ';' or '{' after function parameter list")

    # --- Expression Type Checking Methods ---

    def evaluate_expression(self):
        """
        Entry point for expression type-checking.
        Returns one of: 'anda', 'andamhie', 'chika', 'eklabool'.
        """
        return self.parse_logical_or()

    def parse_logical_or(self):
        left_type = self.parse_logical_and()
        while self.current_token() and self.current_token()[1] == '||':
            self.advance()  # Skip '||'
            right_type = self.parse_logical_and()
            for t in (left_type, right_type):
                if t not in ['anda', 'andamhie', 'eklabool', 'chika']:
                    raise SemanticError(f"Invalid operand type '{t}' for logical operator '||'")
            left_type = 'eklabool'
        return left_type

    def parse_logical_and(self):
        left_type = self.parse_equality()
        while self.current_token() and self.current_token()[1] == '&&':
            self.advance()  # Skip '&&'
            right_type = self.parse_equality()
            for t in (left_type, right_type):
                if t not in ['anda', 'andamhie', 'eklabool', 'chika']:
                    raise SemanticError(f"Invalid operand type '{t}' for logical operator '&&'")
            left_type = 'eklabool'
        return left_type

    def parse_equality(self):
        left_type = self.parse_relational()
        while self.current_token() and self.current_token()[1] in ['==', '!=']:
            op = self.current_token()[1]
            self.advance()
            right_type = self.parse_relational()
            if left_type not in ['anda', 'andamhie', 'eklabool', 'chika'] or right_type not in ['anda', 'andamhie', 'eklabool', 'chika']:
                raise SemanticError("Invalid types for equality operator")
            left_type = 'eklabool'
        return left_type

    def parse_relational(self):
        left_type = self.parse_additive()
        while self.current_token() and self.current_token()[1] in ['<', '<=', '>', '>=']:
            op = self.current_token()[1]
            self.advance()
            right_type = self.parse_additive()
            if left_type not in ['anda', 'andamhie', 'eklabool'] or right_type not in ['anda', 'andamhie', 'eklabool']:
                raise SemanticError("Invalid types for relational operator")
            left_type = 'eklabool'
        return left_type

    def parse_additive(self):
        left_type = self.parse_multiplicative()
        while self.current_token() and self.current_token()[1] in ['+', '-']:
            op = self.current_token()[1]
            self.advance()
            right_type = self.parse_multiplicative()
            if op == '+' and ('chika' in [left_type, right_type]):
                left_type = 'chika'
            else:
                if left_type not in ['anda', 'andamhie', 'eklabool'] or right_type not in ['anda', 'andamhie', 'eklabool']:
                    raise SemanticError("Invalid types for arithmetic addition/subtraction")
                left_type = 'andamhie'
        return left_type

    def parse_multiplicative(self):
        left_type = self.parse_unary()
        while self.current_token() and self.current_token()[1] in ['*', '/', '%', '**', '//']:
            op = self.current_token()[1]
            self.advance()
            right_type = self.parse_unary()
            if left_type not in ['anda', 'andamhie', 'eklabool'] or right_type not in ['anda', 'andamhie', 'eklabool']:
                raise SemanticError("Invalid types for arithmetic multiplicative operation")
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
                    raise SemanticError(f"Operator '{op}' must be applied to an identifier")
                var_name = operand_token[0]
                var_entry = None
                if self.current_function:
                    if var_name in self.symbol_table["functions"][self.current_function]["locals"]:
                        var_entry = self.symbol_table["functions"][self.current_function]["locals"][var_name]
                    elif any(param[0] == var_name for param in self.symbol_table["functions"][self.current_function]["parameters"]):
                        raise SemanticError(f"Operator '{op}' cannot be applied to immutable parameter '{var_name}'")
                else:
                    if var_name in self.symbol_table["variables"]:
                        var_entry = self.symbol_table["variables"][var_name]
                if not var_entry:
                    raise SemanticError(f"Undefined variable '{var_name}' for operator '{op}'")
                if var_entry["naur_flag"]:
                    raise SemanticError(f"Operator '{op}' cannot be applied to constant variable '{var_name}'")
                self.advance()  # Consume identifier.
                return var_entry["data_type"]
            elif op == '-':
                operand_type = self.parse_unary()
                if operand_type not in ['anda', 'andamhie', 'eklabool']:
                    raise SemanticError("Unary minus can only be applied to numeric or boolean types")
                return 'andamhie'
            elif op == '!':
                operand_type = self.parse_unary()
                if operand_type not in ['anda', 'andamhie', 'eklabool', 'chika']:
                    raise SemanticError("Logical not can only be applied to numeric, boolean, or string types")
                return 'eklabool'
        else:
            return self.parse_primary()

    def parse_primary(self):
        token = self.current_token()
        if not token:
            raise SemanticError("Unexpected end of expression")
        if token[1].endswith('_literal'):
            lit_type = token[1].split('_')[0]
            self.advance()
            return lit_type
        elif token[1] in ['korik', 'eme']:
            self.advance()
            return 'eklabool'
        elif token[1] == 'id':
            var_name = token[0]
            self.advance()
            # Check if it's a function call
            if self.current_token() and self.current_token()[1] == '(':
                if var_name not in self.symbol_table["functions"]:
                    raise SemanticError(f"Function '{var_name}' is not declared")
                func_entry = self.symbol_table["functions"][var_name]
                expected_params = func_entry["parameters"]
                self.advance()  # Skip '('
                arg_types = []
                while self.current_token() and self.current_token()[1] != ')':
                    arg_type = self.evaluate_expression()
                    arg_types.append(arg_type)
                    if self.current_token() and self.current_token()[1] == ',':
                        self.advance()  # Skip comma
                if not self.current_token() or self.current_token()[1] != ')':
                    raise SemanticError(f"Missing ')' in function call to '{var_name}'")
                self.advance()  # Skip ')'
                if len(arg_types) != len(expected_params):
                    raise SemanticError(f"Function '{var_name}' expects {len(expected_params)} arguments, got {len(arg_types)}")
                for i, (arg_type, param) in enumerate(zip(arg_types, expected_params)):
                    param_type = param[1]
                    if param_type in ['anda', 'andamhie']:
                        if arg_type not in ['anda', 'andamhie', 'eklabool']:
                            raise SemanticError(f"Argument {i+1} of '{var_name}' expects a numeric type, got '{arg_type}'")
                    elif param_type == 'eklabool':
                        if arg_type not in ['eklabool', 'anda', 'andamhie']:
                            raise SemanticError(f"Argument {i+1} of '{var_name}' expects a boolean type, got '{arg_type}'")
                    elif param_type == 'chika':
                        # Implicit conversion allowed.
                        pass
                return func_entry["return_type"]
            # Process array access if present.
            while self.current_token() and self.current_token()[1] == '[':
                self.advance()  # Skip '['
                index_type = self.evaluate_expression()
                if index_type not in ['anda', 'andamhie', 'eklabool']:
                    raise SemanticError("Array index must be numeric")
                if not self.current_token() or self.current_token()[1] != ']':
                    raise SemanticError("Missing ']' in array access")
                self.advance()  # Skip ']'
            # Lookup variable: check local scope, then parameters, then global scope.
            var_entry = None
            if self.current_function:
                if var_name in self.symbol_table["functions"][self.current_function]["locals"]:
                    var_entry = self.symbol_table["functions"][self.current_function]["locals"][var_name]
                else:
                    for param in self.symbol_table["functions"][self.current_function]["parameters"]:
                        if param[0] == var_name:
                            var_entry = {"data_type": param[1]}
                            break
                    # NEW: Check global variables if not found locally.
                    if not var_entry and var_name in self.symbol_table["variables"]:
                        var_entry = self.symbol_table["variables"][var_name]
            else:
                if var_name in self.symbol_table["variables"]:
                    var_entry = self.symbol_table["variables"][var_name]
            if not var_entry:
                raise SemanticError(f"Undeclared variable '{var_name}'")
            return var_entry["data_type"]
        elif token[1] == '(':
            self.advance()  # Skip '('
            expr_type = self.evaluate_expression()
            if not self.current_token() or self.current_token()[1] != ')':
                raise SemanticError("Missing ')' in expression")
            self.advance()  # Skip ')'
            return expr_type
        else:
            raise SemanticError(f"Unexpected token '{token[0]}' in expression")