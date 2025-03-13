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
        self._token_stream = [t for t in token_stream if t[1] not in ['whitespace', 'newline', 'comment']]
        self.token_index = 0
        # Stack for block scopes (for conditionals, loops, and other nested blocks)
        self.block_scopes = []

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
                elif token[1] == 'pak':
                    self.process_conditional_statement()
                elif token[1] == 'serve':
                    self.process_serve_statement()
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
        # Check that push is inside a function body.
        if self.current_function is None:
            raise SemanticError("Return statement 'push' is only allowed inside function bodies")
        
        # Get the current function's entry to know its return type.
        func_entry = self.symbol_table["functions"][self.current_function]
        declared_return_type = func_entry["return_type"]
        self.advance()  # Skip 'push'
        
        # Check if there is an expression following push.
        if self.current_token() and self.current_token()[1] != ';':
            # Evaluate the expression for the returned value.
            expr_type = self.evaluate_expression()
            if not self.current_token() or self.current_token()[1] != ';':
                raise SemanticError("Missing semicolon after return expression")
            self.advance()  # Skip ';'
            
            # For void functions, push must not return a value.
            if declared_return_type == 'shimenet':
                raise SemanticError("Function with return type 'shimenet' must not return a value")
            
            # Mark that a valid return statement has been encountered.
            func_entry["has_return"] = True

            # Type compatibility checks similar to function call argument validation.
            if declared_return_type in ['anda', 'andamhie']:
                if expr_type not in ['anda', 'andamhie', 'eklabool']:
                    raise SemanticError(f"Return value type '{expr_type}' is not compatible with function return type '{declared_return_type}'")
            elif declared_return_type == 'eklabool':
                if expr_type not in ['eklabool', 'anda', 'andamhie']:
                    raise SemanticError(f"Return value type '{expr_type}' is not compatible with function return type 'eklabool'")
            elif declared_return_type == 'chika':
                if expr_type != 'chika':
                    raise SemanticError(f"Return value type '{expr_type}' is not compatible with function return type 'chika'")
        else:
            # No expression after push.
            if declared_return_type != 'shimenet':
                raise SemanticError(f"Function '{self.current_function}' with return type '{declared_return_type}' must return a value")
            if not self.current_token() or self.current_token()[1] != ';':
                raise SemanticError("Missing semicolon after 'push'")
            self.advance()  # Skip ';'
            # Mark that a (void) return has been encountered.
            func_entry["has_return"] = True

    def finalize_functions(self):
        for func_name, func_entry in self.symbol_table["functions"].items():
            if not func_entry.get("defined", False):
                raise SemanticError(f"Function '{func_name}' declared but not defined")

    def process_initializer(self, var_type):
        # Evaluate the full expression.
        value_type = self.evaluate_expression()
        # If the expression is a givenchy call, bypass type checking.
        if value_type == "givenchy":
            return value_type
        # Check compatibility based on your rules.
        if var_type in ['anda', 'andamhie']:
            if value_type not in ['anda', 'andamhie', 'eklabool']:
                raise SemanticError(f"Variable of type '{var_type}' cannot be assigned a value of type '{value_type}'")
        elif var_type == 'eklabool':
            if value_type not in ['eklabool', 'anda', 'andamhie', 'chika']:
                raise SemanticError(f"Variable of type 'eklabool' cannot be assigned a value of type '{value_type}'")
        elif var_type == 'chika':
            if value_type != 'chika':
                raise SemanticError(f"Variable of type 'chika' cannot be assigned a value of type '{value_type}'")
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
                elif var_type == 'chika':
                    if element_type != 'chika':
                        raise SemanticError(f"Array of type 'chika' cannot have element of type '{element_type}'")
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
        # New check: constants must be initialized.
        if is_constant and initializer_value is None:
            raise SemanticError("Constant variable declaration must be assigned an initializer")
        self.register_variable(data_type, var_name, is_constant, initializer_value, is_array, dimensions)

    def register_variable(self, var_type, var_name, is_constant, initializer_value, is_array=False, dimensions=None):
        entry = {
            "data_type": var_type,
            "value": initializer_value,
            "naur_flag": is_constant,
            "is_array": is_array
        }
        if is_array:
            entry["dimensions"] = dimensions

        # If inside a block (e.g. a conditional or loop block), check the entire chain of enclosing scopes.
        if self.block_scopes:
            if self.variable_exists_in_enclosing_scopes(var_name):
                raise SemanticError(f"Redeclaration of variable '{var_name}' in block scope is not allowed")
            self.block_scopes[-1][var_name] = entry
        else:
            if self.current_function is None:
                if var_name in self.symbol_table["variables"]:
                    raise SemanticError(f"Redeclaration of global variable '{var_name}'")
                self.symbol_table["variables"][var_name] = entry
            else:
                if any(param[0] == var_name for param in self.symbol_table["functions"][self.current_function]["parameters"]):
                    raise SemanticError(f"Local variable '{var_name}' conflicts with a parameter in function '{self.current_function}'")
                if var_name in self.symbol_table["functions"][self.current_function]["locals"]:
                    raise SemanticError(f"Redeclaration of local variable '{var_name}' in function '{self.current_function}'")
                self.symbol_table["functions"][self.current_function]["locals"][var_name] = entry

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
        else:
            if var_name in self.symbol_table["variables"]:
                return True
        return False

    def process_assignment_statement(self):
        # Process an assignment statement: identifier assignment_operator expression ';'
        ident = self.current_token()[0]
        self.advance()  # Skip identifier

        # Check for the assignment operator (plain or augmented)
        if not self.current_token():
            raise SemanticError("Expected assignment operator after identifier")
        op_token = self.current_token()
        op = op_token[1]
        if op not in ['=', '+=', '-=', '*=', '/=', '%=', '**=', '//=']:
            raise SemanticError("Expected an assignment operator")
        self.advance()  # Skip assignment operator

        # Evaluate the right-hand side expression.
        expr_type = self.evaluate_expression()
        
        # If the expression is a givenchy call, bypass type checking.
        if expr_type == "givenchy":
            if not self.current_token() or self.current_token()[1] != ';':
                raise SemanticError("Expected ';' after assignment")
            self.advance()  # Skip ';'
            return

        if not self.current_token() or self.current_token()[1] != ';':
            raise SemanticError("Expected ';' at end of assignment statement")
        self.advance()  # Skip ';'

        # Check if the identifier was declared.
        declared = False
        entry = None
        if self.current_function is not None:
            # Look in the active block scopes (if any) first.
            for scope in reversed(self.block_scopes):
                if ident in scope:
                    declared = True
                    entry = scope[ident]
                    break
            if not declared:
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

        # Check type compatibility.
        var_type = entry["data_type"]

        if op == '=':
            # For simple assignment, use the standard type rules.
            if var_type in ['anda', 'andamhie']:
                if expr_type not in ['anda', 'andamhie', 'eklabool']:
                    raise SemanticError(f"Variable '{ident}' of type '{var_type}' cannot be assigned a value of type '{expr_type}'")
            elif var_type == 'eklabool':
                if expr_type not in ['eklabool', 'anda', 'andamhie', 'chika']:
                    raise SemanticError(f"Variable '{ident}' of type 'eklabool' cannot be assigned a value of type '{expr_type}'")
            elif var_type == 'chika':
                if expr_type != 'chika':
                    raise SemanticError(f"Variable '{ident}' of type 'chika' cannot be assigned a value of type '{expr_type}'")
        else:
            # For augmented assignments:
            if op == '+=' and var_type == 'chika':
                # For string concatenation, both sides must be of type 'chika'.
                if expr_type != 'chika':
                    raise SemanticError(f"Operator '+=' expects type 'chika' for concatenation, got '{expr_type}'")
            else:
                # For all augmented assignment operators (and += on non-chika types), only numeric/boolean types are allowed.
                if var_type not in ['anda', 'andamhie', 'eklabool']:
                    raise SemanticError(f"Operator '{op}' cannot be applied to type '{var_type}'")
                if expr_type not in ['anda', 'andamhie', 'eklabool']:
                    raise SemanticError(f"Operator '{op}' expects a numeric or boolean type for assignment, got '{expr_type}'")

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
        elif self.current_token() and self.current_token()[1] == '{':
            self.advance()  # Skip '{'
            self.current_function = func_name
            func_entry["defined"] = True
            func_entry["has_return"] = False
            # Process function body statements until the matching '}'
            self.process_statements('}')
            if not self.current_token() or self.current_token()[1] != '}':
                raise SemanticError("Expected '}' at end of function body")
            self.advance()  # Skip '}'
            if func_entry["return_type"] != "shimenet" and not func_entry.get("has_return", False):
                raise SemanticError(f"Function '{func_name}' with return type '{func_entry['return_type']}' must return a value")
            self.current_function = None
        else:
            raise SemanticError("Expected ';' or '{' after function parameter list")

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
            raise SemanticError("Expected '{' to start block")
        self.advance()  # Skip '{'
        self.enter_block_scope()
        self.process_statements('}')
        if not self.current_token() or self.current_token()[1] != '}':
            raise SemanticError("Expected '}' to end block")
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
            raise SemanticError("Expected 'pak' for if statement")
        self.advance()  # Skip 'pak'
        if not self.current_token() or self.current_token()[1] != '(':
            raise SemanticError("Expected '(' after 'pak'")
        self.advance()  # Skip '('
        self.evaluate_expression()  # Evaluate condition (any type allowed)
        if not self.current_token() or self.current_token()[1] != ')':
            raise SemanticError("Expected ')' after condition in 'pak'")
        self.advance()  # Skip ')'
        self.process_block()  # Process the if block

        # Process optional else if and else clauses.
        while self.current_token() and self.current_token()[1] == 'ganern':
            self.advance()  # Skip 'ganern'
            if self.current_token() and self.current_token()[1] == 'pak':
                # Else if branch.
                self.advance()  # Skip 'pak'
                if not self.current_token() or self.current_token()[1] != '(':
                    raise SemanticError("Expected '(' after 'ganern pak'")
                self.advance()  # Skip '('
                self.evaluate_expression()  # Evaluate condition
                if not self.current_token() or self.current_token()[1] != ')':
                    raise SemanticError("Expected ')' after condition in 'ganern pak'")
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
            raise SemanticError("Expected '(' after 'keri' for while loop condition")
        self.advance()  # Skip '('
        # Evaluate the condition (any type is allowed)
        self.evaluate_expression()
        if not self.current_token() or self.current_token()[1] != ')':
            raise SemanticError("Expected ')' after while loop condition")
        self.advance()  # Skip ')'
        if not self.current_token() or self.current_token()[1] != '{':
            raise SemanticError("Expected '{' to start while loop block")
        self.process_block()  # The block creates its own scope

    def process_do_while_loop(self):
        """
        Processes a do-while loop in the form:
            keri lang { ... } keri ( condition )
        Here, 'keri lang' together represent the 'do' keyword. The loop body is processed first (in its own block scope)
        and then the condition is evaluated.
        """
        # Current token is 'keri' and the next token should be 'lang'
        self.advance()  # Skip 'keri'
        if not self.current_token() or self.current_token()[1] != 'lang':
            raise SemanticError("Expected 'lang' after 'keri' for do-while loop")
        self.advance()  # Skip 'lang'
        if not self.current_token() or self.current_token()[1] != '{':
            raise SemanticError("Expected '{' to start do-while loop block")
        self.process_block()  # Process the loop body block with its own scope
        if not self.current_token() or self.current_token()[1] != 'keri':
            raise SemanticError("Expected 'keri' after do-while loop block for loop condition")
        self.advance()  # Skip 'keri'
        if not self.current_token() or self.current_token()[1] != '(':
            raise SemanticError("Expected '(' after 'keri' in do-while loop condition")
        self.advance()  # Skip '('
        self.evaluate_expression()  # Evaluate loop condition
        if not self.current_token() or self.current_token()[1] != ')':
            raise SemanticError("Expected ')' after do-while loop condition")
        self.advance()  # Skip ')'

    def process_switch_statement(self):
        """
        Processes a switch statement using:
            versa ( expression ) { case_clauses }
        where:
            - 'versa' is the switch keyword,
            - each case clause begins with 'betsung' followed by an expression and ':'.
            - the default clause is 'ditech' followed by ':'.
        Each case clause is processed in its own block scope. The type of the case expression must be compatible with the switch expression.
        """
        # Current token is 'versa'
        self.advance()  # Skip 'versa'
        if not self.current_token() or self.current_token()[1] != '(':
            raise SemanticError("Expected '(' after 'versa'")
        self.advance()  # Skip '('
        switch_expr_type = self.evaluate_expression()
        if not self.current_token() or self.current_token()[1] != ')':
            raise SemanticError("Expected ')' after switch expression")
        self.advance()  # Skip ')'
        if not self.current_token() or self.current_token()[1] != '{':
            raise SemanticError("Expected '{' to start switch block")
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
                    raise SemanticError(f"Case label type '{case_expr_type}' is not compatible with switch expression type '{switch_expr_type}'")
                if not self.current_token() or self.current_token()[1] != ':':
                    raise SemanticError("Expected ':' after case label")
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
                    raise SemanticError("Multiple default clauses in switch statement")
                default_found = True
                self.advance()  # Skip 'ditech'
                if not self.current_token() or self.current_token()[1] != ':':
                    raise SemanticError("Expected ':' after default clause")
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
                raise SemanticError("Expected 'betsung' or 'ditech' in switch block")
        if not self.current_token() or self.current_token()[1] != '}':
            raise SemanticError("Expected '}' to close switch block")
        self.advance()  # Skip '}'
        self.exit_block_scope()  # Exit the switch block scope.

    def is_type_compatible(self, switch_type, case_type):
        """
        Checks if the case label type is compatible with the switch expression type.
        For numeric types (anda and andamhie), we allow either.
        For other types, they must match exactly.
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
        The expressions for 'from', 'to', and (optionally) 'step' must be numeric (i.e. evaluate to 'anda' or 'andamhie').
        A new block scope is created for the loop header.
        """
        self.advance()  # Skip 'forda'
        if not self.current_token() or self.current_token()[1] != '(':
            raise SemanticError("Expected '(' after 'forda'")
        self.advance()  # Skip '('

        # Determine if there is a new declaration in the loop header.
        new_declaration = False
        declared_type = None
        loop_var_name = None
        loop_var_type = None

        if self.current_token() and self.current_token()[1] in ['anda', 'andamhie', 'chika', 'eklabool']:
            # Ensure only numeric types are used for loop variables.
            declared_type = self.current_token()[1]
            if declared_type not in ['anda', 'andamhie']:
                raise SemanticError(f"For loop iteration variable must be numeric, got type '{declared_type}'")
            new_declaration = True
            self.advance()  # Skip type token
            if not self.current_token() or self.current_token()[1] != 'id':
                raise SemanticError("Expected identifier for for loop variable declaration")
            loop_var_name = self.current_token()[0]
            loop_var_type = declared_type  # Store type for later validation
            self.advance()  # Skip identifier
        else:
            # Otherwise, expect an identifier.
            if not self.current_token() or self.current_token()[1] != 'id':
                raise SemanticError("Expected identifier for for loop variable")
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
                        raise SemanticError(f"Loop variable '{loop_var_name}' cannot be a function parameter")
                    elif loop_var_name in self.symbol_table["variables"]:
                        var_entry = self.symbol_table["variables"][loop_var_name]
            else:
                if loop_var_name in self.symbol_table["variables"]:
                    var_entry = self.symbol_table["variables"][loop_var_name]

            if not var_entry:
                raise SemanticError(f"For loop variable '{loop_var_name}' is not declared")

            loop_var_type = var_entry["data_type"]

            if loop_var_type not in ['anda', 'andamhie']:
                raise SemanticError(f"For loop variable '{loop_var_name}' must be numeric, but it is '{loop_var_type}'")

        # Expect 'from'
        if not self.current_token() or self.current_token()[1] != 'from':
            raise SemanticError("Expected 'from' in for loop header")
        self.advance()  # Skip 'from'

        # Evaluate start expression.
        start_expr_type = self.evaluate_expression()
        if start_expr_type not in ['anda', 'andamhie', 'eklabool']:
            raise SemanticError("For loop 'from' expression must be numeric")

        # Expect 'to'
        if not self.current_token() or self.current_token()[1] != 'to':
            raise SemanticError("Expected 'to' in for loop header")
        self.advance()  # Skip 'to'

        # Evaluate end expression.
        end_expr_type = self.evaluate_expression()
        if end_expr_type not in ['anda', 'andamhie', 'eklabool']:
            raise SemanticError("For loop 'to' expression must be numeric")

        # Optionally handle 'step'
        if self.current_token() and self.current_token()[1] == 'step':
            self.advance()  # Skip 'step'
            step_expr_type = self.evaluate_expression()
            if step_expr_type not in ['anda', 'andamhie', 'eklabool']:
                raise SemanticError("For loop 'step' expression must be numeric")

        if not self.current_token() or self.current_token()[1] != ')':
            raise SemanticError("Expected ')' after for loop header")
        self.advance()  # Skip ')'

        # Enter a new block scope for the for loop header.
        self.enter_block_scope()

        if new_declaration:
            # Check that the loop variable is not already declared in any enclosing scope.
            if self.variable_exists_in_enclosing_scopes(loop_var_name):
                raise SemanticError(f"Redeclaration of variable '{loop_var_name}' in for loop header is not allowed")
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
            raise SemanticError("Expected '{' to start for loop block")
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
            for t in (left_type, right_type):
                if t not in ['anda', 'andamhie', 'eklabool', 'chika', 'givenchy']:
                    raise SemanticError(f"Invalid operand type '{t}' for logical operator '||'")
            left_type = 'eklabool'
        return left_type

    def parse_logical_and(self):
        left_type = self.parse_equality()
        while self.current_token() and self.current_token()[1] == '&&':
            self.advance()  # Skip '&&'
            right_type = self.parse_equality()
            for t in (left_type, right_type):
                if t not in ['anda', 'andamhie', 'eklabool', 'chika', 'givenchy']:
                    raise SemanticError(f"Invalid operand type '{t}' for logical operator '&&'")
            left_type = 'eklabool'
        return left_type

    def parse_equality(self):
        left_type = self.parse_relational()
        while self.current_token() and self.current_token()[1] in ['==', '!=']:
            op = self.current_token()[1]
            self.advance()
            right_type = self.parse_relational()
            if left_type not in ['anda', 'andamhie', 'eklabool', 'chika', 'givenchy'] or right_type not in ['anda', 'andamhie', 'eklabool', 'chika', 'givenchy']:
                raise SemanticError("Invalid types for equality operator")
            left_type = 'eklabool'
        return left_type

    def parse_relational(self):
        left_type = self.parse_additive()
        while self.current_token() and self.current_token()[1] in ['<', '<=', '>', '>=']:
            op = self.current_token()[1]
            self.advance()
            right_type = self.parse_additive()
            if left_type not in ['anda', 'andamhie', 'eklabool', 'givenchy'] or right_type not in ['anda', 'andamhie', 'eklabool', 'givenchy']:
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
                if left_type not in ['anda', 'andamhie', 'eklabool', 'givenchy'] or right_type not in ['anda', 'andamhie', 'eklabool', 'givenchy']:
                    raise SemanticError("Invalid types for arithmetic addition/subtraction")
                left_type = 'andamhie'
        return left_type

    def parse_multiplicative(self):
        left_type = self.parse_unary()
        while self.current_token() and self.current_token()[1] in ['*', '/', '%', '**', '//']:
            op = self.current_token()[1]
            self.advance()
            right_type = self.parse_unary()
            if left_type not in ['anda', 'andamhie', 'eklabool', 'givenchy'] or right_type not in ['anda', 'andamhie', 'eklabool', 'givenchy']:
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
                    # Check in block scopes first.
                    for scope in reversed(self.block_scopes):
                        if var_name in scope:
                            var_entry = scope[var_name]
                            break
                    if not var_entry:
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
                if operand_type not in ['anda', 'andamhie', 'eklabool', 'givenchy']:
                    raise SemanticError("Unary minus can only be applied to numeric or boolean types")
                return 'andamhie'
            elif op == '!':
                operand_type = self.parse_unary()
                if operand_type not in ['anda', 'andamhie', 'eklabool', 'chika', 'givenchy']:
                    raise SemanticError("Logical not can only be applied to numeric, boolean, or string types")
                return 'eklabool'
        else:
            return self.parse_primary()

    def parse_primary(self):
        token = self.current_token()
        if not token:
            raise SemanticError("Unexpected end of expression")

        # Handle givenchy input call.
        if token[1] == 'givenchy':
            self.advance()  # Skip 'givenchy'
            if not self.current_token() or self.current_token()[1] != '(':
                raise SemanticError("Expected '(' after 'givenchy'")
            self.advance()  # Skip '('
            if not self.current_token() or self.current_token()[1] != 'chika_literal':
                raise SemanticError("Expected string literal as argument for 'givenchy'")
            self.advance()  # Skip the string literal argument
            if not self.current_token() or self.current_token()[1] != ')':
                raise SemanticError("Expected ')' after 'givenchy' argument")
            self.advance()  # Skip ')'
            return "givenchy"

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
                        if arg_type not in ['eklabool', 'anda', 'andamhie', 'chika']:
                            raise SemanticError(f"Argument {i+1} of '{var_name}' expects a boolean type, got '{arg_type}'")
                    elif param_type == 'chika':
                        if arg_type != 'chika':
                            raise SemanticError(f"Argument {i+1} of '{var_name}' expects type 'chika', got '{arg_type}'")
                return func_entry["return_type"]
            # Process array access if present.
            while self.current_token() and self.current_token()[1] == '[':
                self.advance()  # Skip '['
                index_type = self.evaluate_expression()
                if index_type not in ['anda', 'andamhie', 'eklabool', 'givenchy']:
                    raise SemanticError("Array index must be numeric")
                if not self.current_token() or self.current_token()[1] != ']':
                    raise SemanticError("Missing ']' in array access")
                self.advance()  # Skip ']'
            # Lookup variable: check block scopes (if any), then local function scope, then global.
            var_entry = None
            if self.current_function:
                for scope in reversed(self.block_scopes):
                    if var_name in scope:
                        var_entry = scope[var_name]
                        break
                if not var_entry:
                    if var_name in self.symbol_table["functions"][self.current_function]["locals"]:
                        var_entry = self.symbol_table["functions"][self.current_function]["locals"][var_name]
                    else:
                        for param in self.symbol_table["functions"][self.current_function]["parameters"]:
                            if param[0] == var_name:
                                var_entry = {"data_type": param[1]}
                                break
                        if not var_entry and var_name in self.symbol_table["variables"]:
                            var_entry = self.symbol_table["variables"][var_name]
            else:
                if var_name in self.symbol_table["variables"]:
                    var_entry = self.symbol_table["variables"][var_name]
            if not var_entry:
                raise SemanticError(f"Undeclared variable '{var_name}'")
            
            # --- Added support for postfix operators: ++ and -- 
            while self.current_token() and self.current_token()[1] in ['++', '--']:
                op = self.current_token()[1]
                if var_entry.get("naur_flag", False):
                    raise SemanticError(f"Operator '{op}' cannot be applied to constant variable '{var_name}'")
                if self.current_function:
                    for param in self.symbol_table["functions"][self.current_function]["parameters"]:
                        if param[0] == var_name:
                            raise SemanticError(f"Operator '{op}' cannot be applied to immutable parameter '{var_name}'")
                self.advance()  # Consume the postfix operator.
            # -----------------------------------------------
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

    def process_serve_statement(self):
        """Process and validate the 'serve' statement (print statement)."""
        if self.current_token()[1] != 'serve':
            raise SemanticError("Expected 'serve' statement")

        self.advance() 
        
        if not self.current_token() or self.current_token()[1] != '(':
            raise SemanticError("Expected '(' after 'serve' statement")
        
        self.advance() 
        
        expr_type = self.evaluate_expression()
        
        if expr_type == "chika":
            if self.current_token() and self.current_token()[1] not in [')', ';', '+']:
                raise SemanticError("Invalid operation: 'chika' type only supports '+' for concatenation")
        
        if self.current_token() and self.current_token()[1] == ',':
            raise SemanticError("Multiple arguments in 'serve' statement are not allowed")
        
        if not self.current_token() or self.current_token()[1] != ')':
            raise SemanticError("Expected ')' at the end of 'serve' statement")
        
        self.advance()  
        if not self.current_token() or self.current_token()[1] != ';':
            raise SemanticError("Expected ';' at the end of 'serve' statement")
        
        self.advance()
