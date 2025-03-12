from .error_handler import SemanticError

class SemanticAnalyzer:
    def __init__(self, token_stream):
        self.symbol_table = {
            "variables": {},
            "functions": {}
        }
        self.current_function = None  # None means global scope.
        # Filter out whitespace and newline tokens.
        self._token_stream = [t for t in token_stream if t[1] not in ['whitespace', 'newline']]
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
            arg_token = self.current_token()
            arg_type = None

            # Determine argument type
            if arg_token[1] == 'id':
                var_name = arg_token[0]
                # Check local variables/parameters first
                if var_name in self.symbol_table["functions"][self.current_function]["locals"]:
                    arg_type = self.symbol_table["functions"][self.current_function]["locals"][var_name]["data_type"]
                else:
                    # Check parameters of the current function
                    params = self.symbol_table["functions"][self.current_function]["parameters"]
                    param_match = [p for p in params if p[0] == var_name]
                    if param_match:
                        arg_type = param_match[0][1]
                    else:
                        # Check global variables
                        if var_name in self.symbol_table["variables"]:
                            arg_type = self.symbol_table["variables"][var_name]["data_type"]
                        else:
                            raise SemanticError(f"Undeclared variable '{var_name}' used in call to '{func_name}'")
            elif arg_token[1].endswith('_literal'):
                arg_type = arg_token[1].split('_')[0]  # e.g., 'anda_literal' → 'anda'
            elif arg_token[1] in ['korik', 'eme']:
                arg_type = 'eklabool'
            else:
                raise SemanticError(f"Invalid argument '{arg_token[0]}' in call to '{func_name}'")

            args.append(arg_type)
            self.advance()

            # Skip commas
            if self.current_token() and self.current_token()[1] == ',':
                self.advance()

        # Validate closing parenthesis
        if not self.current_token() or self.current_token()[1] != ')':
            raise SemanticError(f"Missing ')' in call to '{func_name}'")
        self.advance()  # Move past ')'

        # Skip semicolon if present
        if self.current_token() and self.current_token()[1] == ';':
            self.advance()

        # Validate argument count
        if len(args) != len(expected_params):
            raise SemanticError(f"Function '{func_name}' expects {len(expected_params)} arguments, got {len(args)}")

        # Validate argument types
        for i, (arg_type, param) in enumerate(zip(args, expected_params)):
            param_type = param[1]
            if arg_type != param_type:
                raise SemanticError(f"Argument {i+1} of '{func_name}' expects type '{param_type}', got '{arg_type}'")

    def finalize_functions(self):
        for func_name, func_entry in self.symbol_table["functions"].items():
            if not func_entry.get("defined", False):
                raise SemanticError(f"Function '{func_name}' declared but not defined")

    def process_initializer(self, var_type):
        if not self.current_token():
            raise SemanticError("Expected literal for initialization")
        tok = self.current_token()
        if tok[1] in ['korik', 'eme']:
            if var_type not in ['anda', 'andamhie', 'eklabool']:
                raise SemanticError(f"Type '{var_type}' cannot be initialized with a boolean literal")
            value = tok[0]  # Keep as "korik" or "eme"
            self.advance()
            return value
        elif tok[1].endswith('_literal'):
            value = tok[0]
            self.advance()
            return value
        else:
            raise SemanticError("Expected literal for initialization")

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
        Recursively processes an array initializer list without enforcing that
        the number of elements exactly matches the declared dimensions.
        It collects elements until the matching closing brace is encountered.
        This method does not validate the initializer's shape against 'dimensions'
        at compile time.
        """
        if not self.current_token() or self.current_token()[1] != '{':
            raise SemanticError("Expected '{' to start array initializer")
        self.advance()  # Skip the opening '{'
        init_list = []
        # Loop until a closing brace is encountered.
        while self.current_token() and self.current_token()[1] != '}':
            # If a nested initializer list is encountered, recurse.
            if self.current_token()[1] == '{':
                element = self.process_array_initializer(dimensions, var_type, dim_index + 1)
            else:
                # Otherwise, expect a scalar literal.
                tok = self.current_token()
                if tok[1] in ['korik', 'eme']:
                    if var_type not in ['anda', 'andamhie', 'eklabool']:
                        raise SemanticError(f"Type '{var_type}' cannot be initialized with a boolean literal")
                    element = tok[0]  # Keep as "korik" or "eme"
                    self.advance()
                elif tok[1].endswith('_literal'):
                    element = tok[0]
                    self.advance()
                else:
                    raise SemanticError("Expected literal in array initializer")
            init_list.append(element)
            # If a comma is present, skip it.
            if self.current_token() and self.current_token()[1] == ',':
                self.advance()
            else:
                continue
        if not self.current_token() or self.current_token()[1] != '}':
            raise SemanticError("Expected '}' at end of array initializer")
        self.advance()  # Skip the closing '}'
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
        self.advance()  # Skip semicolon

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
        # Process an assignment statement: identifier '=' literal ';'
        ident = self.current_token()[0]
        self.advance()  # Skip the identifier
        if not self.current_token() or self.current_token()[1] != '=':
            raise SemanticError("Expected '=' in assignment statement")
        self.advance()  # Skip '='
        if not self.current_token() or not (self.current_token()[1].endswith('_literal') or self.current_token()[1] in ['korik','eme']):
            raise SemanticError("Expected literal in assignment statement")
        self.advance()  # Skip literal
        if not self.current_token() or self.current_token()[1] != ';':
            raise SemanticError("Expected ';' at end of assignment statement")
        self.advance()  # Skip ';'
        
        # Now check if the identifier was declared.
        declared = False
        entry = None
        if self.current_function is not None:
            # Check local variables first.
            if ident in self.symbol_table["functions"][self.current_function]["locals"]:
                declared = True
                entry = self.symbol_table["functions"][self.current_function]["locals"][ident]
            # Then check if it is declared as a parameter.
            elif any(param[0] == ident for param in self.symbol_table["functions"][self.current_function]["parameters"]):
                raise SemanticError(f"Assignment to immutable parameter '{ident}' is not allowed")
            # Finally check global variables.
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
        
        # Check if the variable is constant.
        if entry["naur_flag"]:
            raise SemanticError(f"Assignment to constant variable '{ident}' is not allowed")

    def function_declaration(self, return_type, func_name):
        # If the function was already declared (e.g. as a prototype)
        if func_name in self.symbol_table["functions"]:
            existing = self.symbol_table["functions"][func_name]
            if existing.get("defined", False):
                raise SemanticError(f"Redefinition of function '{func_name}'")
            
            # Check if return types match between prototype and definition
            if existing["return_type"] != return_type:
                raise SemanticError(
                    f"Return type mismatch for function '{func_name}' between prototype '{existing['return_type']}' and definition '{return_type}'"
                )
            
            func_entry = existing
        else:
            # Initialize with 'parameters' set to None so we can distinguish a new declaration.
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

        # ***** Parameter Consistency Check *****
        if func_entry["parameters"] is not None:
            # A previous declaration (prototype) exists – compare the parameter lists.
            if func_entry["parameters"] != parameters:
                raise SemanticError(
                    f"Parameter list mismatch for function '{func_name}' between prototype and definition"
                )
        else:
            # No prior declaration; save the current parameter list.
            func_entry["parameters"] = parameters

        # Process function prototype versus definition.
        if not self.current_token():
            raise SemanticError("Unexpected end of input after function parameters")
        if self.current_token()[1] == ';':
            if func_entry["defined"] is True:
                raise SemanticError(f"Function '{func_name}' already defined")
            func_entry["defined"] = False
            self.advance()  # Skip ';'
        elif self.current_token()[1] == '{':
            self.advance()  # Skip '{'
            self.current_function = func_name
            func_entry["defined"] = True
            brace_depth = 1  # To track nested scopes within the function body

            # Process tokens inside the function body.
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