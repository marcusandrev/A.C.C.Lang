from .error_handler import SemanticError

# --- AST Node Classes ---

class ASTNode:
    pass

class ProgramNode(ASTNode):
    def __init__(self, statements):
        self.statements = statements

    def __repr__(self):
        return f"ProgramNode({self.statements})"

class FunctionDeclNode(ASTNode):
    def __init__(self, return_type, name, parameters, body, is_prototype=False):
        self.return_type = return_type
        self.name = name
        self.parameters = parameters  # list of (param_name, param_type)
        self.body = body              # list of statements (None for prototype)
        self.is_prototype = is_prototype

    def __repr__(self):
        return (f"FunctionDeclNode({self.name}, {self.return_type}, "
                f"params={self.parameters}, body={self.body} prototype={self.is_prototype})")

class VarDeclNode(ASTNode):
    def __init__(self, data_type, name, initializer=None, is_constant=False, is_array=False, dimensions=None):
        self.data_type = data_type
        self.name = name
        self.initializer = initializer  # Can be an expression node or array initializer list
        self.is_constant = is_constant
        self.is_array = is_array
        self.dimensions = dimensions  # List of dimension expressions if array

    def __repr__(self):
        return (f"VarDeclNode({self.name}, {self.data_type}, initializer={self.initializer}, "
                f"const={self.is_constant}, array={self.is_array}, dimensions={self.dimensions})")

class AssignmentNode(ASTNode):
    def __init__(self, identifier, operator, expression):
        self.identifier = identifier
        self.operator = operator
        self.expression = expression

    def __repr__(self):
        return f"AssignmentNode({self.identifier} {self.operator} {self.expression})"

class FunctionCallNode(ASTNode):
    def __init__(self, name, arguments):
        self.name = name
        self.arguments = arguments  # List of expression nodes

    def __repr__(self):
        return f"FunctionCallNode({self.name}, args={self.arguments})"

class ReturnNode(ASTNode):
    def __init__(self, expression=None):
        self.expression = expression  # Expression node or None

    def __repr__(self):
        return f"ReturnNode({self.expression})"

class PrintNode(ASTNode):
    def __init__(self, expression):
        self.expression = expression

    def __repr__(self):
        return f"PrintNode({self.expression})"

class IfNode(ASTNode):
    def __init__(self, condition, then_block, else_if_blocks=None, else_block=None):
        self.condition = condition
        self.then_block = then_block         # List of statements
        self.else_if_blocks = else_if_blocks if else_if_blocks is not None else []  # List of tuples: (condition, statements)
        self.else_block = else_block         # List of statements

    def __repr__(self):
        return f"IfNode({self.condition}, then={self.then_block}, else_if={self.else_if_blocks}, else={self.else_block})"

class WhileNode(ASTNode):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body  # List of statements

    def __repr__(self):
        return f"WhileNode({self.condition}, {self.body})"

class DoWhileNode(ASTNode):
    def __init__(self, body, condition):
        self.body = body        # List of statements
        self.condition = condition

    def __repr__(self):
        return f"DoWhileNode(body={self.body}, cond={self.condition})"

class ForNode(ASTNode):
    def __init__(self, loop_var, start_expr, end_expr, step_expr, body, new_declaration=False, var_type=None):
        self.loop_var = loop_var
        self.start_expr = start_expr
        self.end_expr = end_expr
        self.step_expr = step_expr  # Can be None
        self.body = body            # List of statements
        self.new_declaration = new_declaration
        self.var_type = var_type    # Type if variable is declared in the loop header

    def __repr__(self):
        return (f"ForNode({self.loop_var}, from={self.start_expr}, to={self.end_expr}, "
                f"step={self.step_expr}, new_decl={self.new_declaration}, body={self.body})")

class SwitchNode(ASTNode):
    def __init__(self, expression, cases, default_case=None):
        self.expression = expression
        self.cases = cases          # List of tuples: (case_expression, list of statements)
        self.default_case = default_case  # List of statements or None

    def __repr__(self):
        return f"SwitchNode({self.expression}, cases={self.cases}, default={self.default_case})"

class BreakNode(ASTNode):
    def __repr__(self):
        return "BreakNode()"

class ContinueNode(ASTNode):
    def __repr__(self):
        return "ContinueNode()"

class BlockNode(ASTNode):
    def __init__(self, statements):
        self.statements = statements

    def __repr__(self):
        return f"BlockNode({self.statements})"

# --- Expression Nodes ---

class LiteralNode(ASTNode):
    def __init__(self, value, literal_type):
        self.value = value
        self.literal_type = literal_type  # e.g., 'anda', 'chika'

    def __repr__(self):
        return f"LiteralNode({self.value}, {self.literal_type})"

class IdentifierNode(ASTNode):
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"IdentifierNode({self.name})"

class BinaryOpNode(ASTNode):
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator  # e.g., '+', '-', '&&'
        self.right = right

    def __repr__(self):
        return f"BinaryOpNode({self.left} {self.operator} {self.right})"

class UnaryOpNode(ASTNode):
    def __init__(self, operator, operand, is_postfix=False):
        self.operator = operator  # e.g., '-', '!', '++'
        self.operand = operand
        self.is_postfix = is_postfix

    def __repr__(self):
        pos = " (postfix)" if self.is_postfix else ""
        return f"UnaryOpNode({self.operator}{pos} {self.operand})"

class ArrayAccessNode(ASTNode):
    def __init__(self, array, index_exprs):
        self.array = array       # Typically an IdentifierNode
        self.index_exprs = index_exprs  # List of expression nodes for indices

    def __repr__(self):
        return f"ArrayAccessNode({self.array}, indices={self.index_exprs})"

class InputCallNode(ASTNode):
    def __init__(self, prompt):
        self.prompt = prompt  # The prompt string

    def __repr__(self):
        return f"InputCallNode({self.prompt})"

class UnaryOpStatementNode(ASTNode):
    def __init__(self, operator, operand, is_postfix=False):
        self.operator = operator
        self.operand = operand
        self.is_postfix = is_postfix

    def __repr__(self):
        pos = " (postfix)" if self.is_postfix else ""
        return f"UnaryOpStatementNode({self.operator}{pos} {self.operand})"


# --- AST Generator Class ---

class ASTGenerator:
    def __init__(self, token_stream):
        # Filter out whitespace, newline, and comment tokens.
        self.tokens = [t for t in token_stream if t[0][1] not in ['whitespace', 'newline', 'comment']]
        self.index = 0

    def current_token(self):
        if 0 <= self.index < len(self.tokens):
            return self.tokens[self.index][0]
        return None

    def next_token(self):
        if self.index + 1 < len(self.tokens):
            return self.tokens[self.index + 1][0]
        return None

    def advance(self):
        self.index += 1

    def expect(self, expected_value, error_message):
        token = self.current_token()
        if not token or token[1] != expected_value:
            raise SemanticError(error_message, self.tokens[self.index][1][0])
        self.advance()
        return token

    def generate(self):
        """Main entry point: generate the AST for the whole program."""
        statements = []
        # Parse all top-level statements
        while self.current_token():
            stmt = self.parse_statement()
            if stmt is not None:
                if isinstance(stmt, list):
                    statements.extend(stmt)
                else:
                    statements.append(stmt)
        # --- Post-Processing: Replace function prototypes with their definitions ---
        # Build a dictionary mapping function names to their definition node (if any)
        func_defs = {}
        for stmt in statements:
            if isinstance(stmt, FunctionDeclNode):
                if not stmt.is_prototype:
                    func_defs[stmt.name] = stmt
                elif stmt.name not in func_defs:
                    func_defs[stmt.name] = stmt
        # Replace prototypes with definitions when available.
        final_statements = []
        seen_funcs = set()
        for stmt in statements:
            if isinstance(stmt, FunctionDeclNode):
                if stmt.name in seen_funcs:
                    continue
                if stmt.is_prototype and func_defs[stmt.name] is not stmt:
                    final_statements.append(func_defs[stmt.name])
                else:
                    final_statements.append(stmt)
                seen_funcs.add(stmt.name)
            else:
                final_statements.append(stmt)
        return ProgramNode(final_statements)

    def parse_statement(self):
        token = self.current_token()
        if not token:
            return None
        if token[1] in ['naur', 'anda', 'andamhie', 'chika', 'eklabool', 'shimenet']:
            return self.parse_declaration()
        elif token[1] == 'pak':
            return self.parse_if_statement()
        elif token[1] == 'serve':
            return self.parse_print_statement()
        elif token[1] == 'push':
            return self.parse_return_statement()
        elif token[1] == 'keri':
            if self.next_token() and self.next_token()[1] == 'lang':
                return self.parse_do_while_loop()
            else:
                return self.parse_while_loop()
        elif token[1] == 'versa':
            return self.parse_switch_statement()
        elif token[1] == 'forda':
            return self.parse_for_loop()
        elif token[1] == 'amaccana':
            self.advance()
            self.expect(';', "Expected ';' after 'amaccana'")
            return BreakNode()
        elif token[1] == 'gogogo':
            self.advance()
            self.expect(';', "Expected ';' after 'gogogo'")
            return ContinueNode()
        elif token[1] == '{':
            return self.parse_block()
        elif token[1] == 'id':
            if self.next_token() and self.next_token()[1] == '(':
                return self.parse_function_call_statement()
            elif self.next_token() and (self.next_token()[1] == '[' or self.next_token()[1] in ['=', '+=', '-=', '*=', '/=', '%=', '**=', '//=']):
                return self.parse_assignment_statement()
            elif self.next_token() and self.next_token()[1] in ['++', '--']:
                return self.parse_unary_statement(postfix=True)
            else:
                self.advance()
                return None
        elif token[1] in ['++', '--']:
            return self.parse_unary_statement(postfix=False)
        else:
            self.advance()
            return None

    def parse_unary_statement(self, postfix=False):
        if postfix:
            operand = IdentifierNode(self.current_token()[0])
            self.advance()
            op = self.current_token()[1]
            self.advance()
            self.expect(';', "Expected ';' after unary expression")
            return UnaryOpStatementNode(op, operand, is_postfix=True)
        else:
            op = self.current_token()[1]
            self.advance()
            operand = IdentifierNode(self.current_token()[0])
            self.advance()
            self.expect(';', "Expected ';' after unary expression")
            return UnaryOpStatementNode(op, operand, is_postfix=False)

    def parse_declaration(self):
        is_constant = False
        token = self.current_token()
        if token[1] == 'naur':
            is_constant = True
            self.advance()
            token = self.current_token()
        if token[1] == 'shimenet':
            self.advance()  # Skip 'shimenet'
            if self.current_token() and self.current_token()[1] == 'kween':
                func_name = "kween"
                self.advance()
            elif self.current_token() and self.current_token()[1] == 'id':
                func_name = self.current_token()[0]
                self.advance()
            else:
                raise SemanticError("Expected function name after 'shimenet'", self.tokens[self.index][1][0])
            return self.parse_function_declaration('shimenet', func_name)
        else:
            if token[1] not in ['anda', 'andamhie', 'chika', 'eklabool']:
                raise SemanticError("Expected a type token", self.tokens[self.index][1][0])
            data_type = token[1]
            self.advance()  # Skip type token
            if not self.current_token() or self.current_token()[1] != 'id':
                raise SemanticError("Expected identifier after type", self.tokens[self.index][1][0])
            var_name = self.current_token()[0]
            self.advance()  # Skip identifier
            if self.current_token() and self.current_token()[1] == '(':
                return self.parse_function_declaration(data_type, var_name)
            else:
                var_decl = self.parse_variable_declaration(data_type, var_name, is_constant)
                declarations = [var_decl]
                while self.current_token() and self.current_token()[1] == ',':
                    self.advance()  # Skip comma
                    if not self.current_token() or self.current_token()[1] != 'id':
                        raise SemanticError("Expected identifier after comma in declaration", self.tokens[self.index][1][0])
                    var_name = self.current_token()[0]
                    self.advance()
                    declarations.append(self.parse_variable_declaration(data_type, var_name, is_constant))
                self.expect(';', "Missing semicolon at end of declaration")
                return declarations[0] if len(declarations) == 1 else declarations

    def parse_variable_declaration(self, data_type, var_name, is_constant):
        is_array = False
        dimensions = []
        initializer = None
        while self.current_token() and self.current_token()[1] == '[':
            is_array = True
            self.advance()  # Skip '['
            dim_expr = self.parse_expression()
            dimensions.append(dim_expr)
            self.expect(']', "Expected ']' after array dimension")
        if self.current_token() and self.current_token()[1] == '=':
            self.advance()  # Skip '='
            if is_array:
                initializer = self.parse_array_initializer(dimensions, data_type)
            else:
                initializer = self.parse_expression()
        return VarDeclNode(data_type, var_name, initializer, is_constant, is_array, dimensions if is_array else None)

    def parse_array_initializer(self, dimensions, data_type):
        self.expect('{', "Expected '{' to start array initializer")
        elements = []
        while self.current_token() and self.current_token()[1] != '}':
            if self.current_token()[1] == '{':
                element = self.parse_array_initializer(dimensions, data_type)
            else:
                element = self.parse_expression()
            elements.append(element)
            if self.current_token() and self.current_token()[1] == ',':
                self.advance()
        self.expect('}', "Expected '}' at end of array initializer")
        return elements

    def parse_function_declaration(self, return_type, func_name):
        self.expect('(', "Expected '(' after function name")
        parameters = []
        while self.current_token() and self.current_token()[1] != ')':
            if self.current_token()[1] in ['anda', 'andamhie', 'chika', 'eklabool']:
                param_type = self.current_token()[1]
                self.advance()
                if not self.current_token() or self.current_token()[1] != 'id':
                    raise SemanticError("Expected parameter name in function declaration", self.tokens[self.index][1][0])
                param_name = self.current_token()[0]
                parameters.append((param_name, param_type))
                self.advance()
                if self.current_token() and self.current_token()[1] == ',':
                    self.advance()
                elif self.current_token() and self.current_token()[1] != ')':
                    raise SemanticError("Expected ',' or ')' in parameter list", self.tokens[self.index][1][0])
            else:
                raise SemanticError("Unexpected token in parameter list", self.tokens[self.index][1][0])
        self.expect(')', "Missing closing parenthesis in function declaration")
        if self.current_token() and self.current_token()[1] == ';':
            self.advance()
            return FunctionDeclNode(return_type, func_name, parameters, None, is_prototype=True)
        elif self.current_token() and self.current_token()[1] == '{':
            body = self.parse_block().statements
            return FunctionDeclNode(return_type, func_name, parameters, body, is_prototype=False)
        else:
            raise SemanticError("Expected ';' or '{' after function parameter list", self.tokens[self.index][1][0])

    def parse_assignment_statement(self):
        # --- parse the LHS as either a bare identifier or an array access ---
        lhs = self.parse_primary()
        if not isinstance(lhs, (IdentifierNode, ArrayAccessNode)):
            raise SemanticError(
                "Invalid assignment target",
                self.tokens[self.index][1][0]
            )

        # next must be one of the assignment operators
        ops = ['=', '+=', '-=', '*=', '/=', '%=', '**=', '//=']
        if not self.current_token() or self.current_token()[1] not in ops:
            raise SemanticError(
                "Expected assignment operator",
                self.tokens[self.index][1][0]
            )
        op = self.current_token()[1]
        self.advance()

        # parse the RHS expression
        expr = self.parse_expression()
        self.expect(';', "Expected ';' at end of assignment statement")

        return AssignmentNode(lhs, op, expr)

    def parse_function_call_statement(self):
        if not self.current_token() or self.current_token()[1] != 'id':
            raise SemanticError("Expected function name", self.tokens[self.index][1][0])
        func_name = self.current_token()[0]
        self.advance()  # Skip function name
        node = self.parse_function_call_expr(func_name)
        self.expect(';', "Expected ';' after function call")
        return node

    def parse_function_call_expr(self, func_name):
        self.expect('(', "Expected '(' after function name in function call")
        args = []
        while self.current_token() and self.current_token()[1] != ')':
            arg = self.parse_expression()
            args.append(arg)
            if self.current_token() and self.current_token()[1] == ',':
                self.advance()
        self.expect(')', f"Missing ')' in function call to '{func_name}'")
        return FunctionCallNode(func_name, args)

    def parse_print_statement(self):
        self.advance()  # Skip 'serve'
        self.expect('(', "Expected '(' after 'serve'")
        expr = self.parse_expression()
        self.expect(')', "Expected ')' at the end of 'serve' statement")
        self.expect(';', "Expected ';' at the end of 'serve' statement")
        return PrintNode(expr)

    def parse_return_statement(self):
        self.advance()  # Skip 'push'
        expr = None
        if self.current_token() and self.current_token()[1] != ';':
            expr = self.parse_expression()
        self.expect(';', "Missing semicolon after return statement")
        return ReturnNode(expr)

    def parse_if_statement(self):
        self.expect('pak', "Expected 'pak' for if statement")
        self.expect('(', "Expected '(' after 'pak'")
        condition = self.parse_expression()
        self.expect(')', "Expected ')' after condition in 'pak'")
        then_block = self.parse_block().statements
        else_if_blocks = []
        else_block = None
        while self.current_token() and self.current_token()[1] == 'ganern':
            self.advance()  # Skip 'ganern'
            if self.current_token() and self.current_token()[1] == 'pak':
                self.advance()  # Skip 'pak'
                self.expect('(', "Expected '(' after 'ganern pak'")
                elif_condition = self.parse_expression()
                self.expect(')', "Expected ')' after condition in 'ganern pak'")
                elif_block = self.parse_block().statements
                else_if_blocks.append((elif_condition, elif_block))
            else:
                else_block = self.parse_block().statements
                break
        return IfNode(condition, then_block, else_if_blocks, else_block)

    def parse_while_loop(self):
        self.expect('keri', "Expected 'keri' for while loop")
        self.expect('(', "Expected '(' after 'keri' for while loop condition")
        condition = self.parse_expression()
        self.expect(')', "Expected ')' after while loop condition")
        body = self.parse_block().statements
        return WhileNode(condition, body)

    def parse_do_while_loop(self):
        self.expect('keri', "Expected 'keri' for do-while loop")
        self.expect('lang', "Expected 'lang' after 'keri' for do-while loop")
        body = self.parse_block().statements
        self.expect('keri', "Expected 'keri' after do-while loop block for loop condition")
        self.expect('(', "Expected '(' after 'keri' in do-while loop condition")
        condition = self.parse_expression()
        self.expect(')', "Expected ')' after do-while loop condition")
        return DoWhileNode(body, condition)

    def parse_switch_statement(self):
        self.expect('versa', "Expected 'versa' for switch statement")
        self.expect('(', "Expected '(' after 'versa'")
        expression = self.parse_expression()
        self.expect(')', "Expected ')' after switch expression")
        self.expect('{', "Expected '{' to start switch block")
        cases = []
        default_case = None
        while self.current_token() and self.current_token()[1] != '}':
            token = self.current_token()
            if token[1] == 'betsung':
                self.advance()  # Skip 'betsung'
                case_expr = self.parse_expression()
                self.expect(':', "Expected ':' after case label")
                case_statements = []
                while self.current_token() and self.current_token()[1] not in ['betsung', 'ditech', '}']:
                    stmt = self.parse_statement()
                    if stmt is not None:
                        if isinstance(stmt, list):
                            case_statements.extend(stmt)
                        else:
                            case_statements.append(stmt)
                cases.append((case_expr, case_statements))
            elif token[1] == 'ditech':
                self.advance()  # Skip 'ditech'
                self.expect(':', "Expected ':' after default clause")
                default_case = []
                while self.current_token() and self.current_token()[1] not in ['betsung', '}']:
                    stmt = self.parse_statement()
                    if stmt is not None:
                        if isinstance(stmt, list):
                            default_case.extend(stmt)
                        else:
                            default_case.append(stmt)
            else:
                self.advance()
        self.expect('}', "Expected '}' to close switch block")
        return SwitchNode(expression, cases, default_case)

    def parse_for_loop(self):
        self.expect('forda', "Expected 'forda' for for loop")
        self.expect('(', "Expected '(' after 'forda'")
        new_declaration = False
        declared_type = None
        loop_var = None
        if self.current_token() and self.current_token()[1] in ['anda', 'andamhie', 'chika', 'eklabool']:
            new_declaration = True
            declared_type = self.current_token()[1]
            self.advance()  # Skip type token
            if not self.current_token() or self.current_token()[1] != 'id':
                raise SemanticError("Expected identifier for for loop variable declaration", self.tokens[self.index][1][0])
            loop_var = self.current_token()[0]
            self.advance()  # Skip identifier
        else:
            if not self.current_token() or self.current_token()[1] != 'id':
                raise SemanticError("Expected identifier for for loop variable", self.tokens[self.index][1][0])
            loop_var = self.current_token()[0]
            self.advance()  # Skip identifier
        self.expect('from', "Expected 'from' in for loop header")
        start_expr = self.parse_expression()
        self.expect('to', "Expected 'to' in for loop header")
        end_expr = self.parse_expression()
        step_expr = None
        if self.current_token() and self.current_token()[1] == 'step':
            self.advance()  # Skip 'step'
            step_expr = self.parse_expression()
        self.expect(')', "Expected ')' after for loop header")
        body = self.parse_block().statements
        return ForNode(loop_var, start_expr, end_expr, step_expr, body, new_declaration, declared_type)

    def parse_block(self):
        self.expect('{', "Expected '{' to start block")
        statements = []
        while self.current_token() and self.current_token()[1] != '}':
            stmt = self.parse_statement()
            if stmt is not None:
                if isinstance(stmt, list):
                    statements.extend(stmt)
                else:
                    statements.append(stmt)
        self.expect('}', "Expected '}' to end block")
        return BlockNode(statements)

    # --- Expression Parsing Methods ---
    
    def parse_expression(self):
        return self.parse_logical_or()

    def parse_logical_or(self):
        left = self.parse_logical_and()
        while self.current_token() and self.current_token()[1] == '||':
            op = self.current_token()[1]
            self.advance()
            right = self.parse_logical_and()
            left = BinaryOpNode(left, op, right)
        return left

    def parse_logical_and(self):
        left = self.parse_equality()
        while self.current_token() and self.current_token()[1] == '&&':
            op = self.current_token()[1]
            self.advance()
            right = self.parse_equality()
            left = BinaryOpNode(left, op, right)
        return left

    def parse_equality(self):
        left = self.parse_relational()
        while self.current_token() and self.current_token()[1] in ['==', '!=']:
            op = self.current_token()[1]
            self.advance()
            right = self.parse_relational()
            left = BinaryOpNode(left, op, right)
        return left

    def parse_relational(self):
        left = self.parse_additive()
        while self.current_token() and self.current_token()[1] in ['<', '<=', '>', '>=']:
            op = self.current_token()[1]
            self.advance()
            right = self.parse_additive()
            left = BinaryOpNode(left, op, right)
        return left

    def parse_additive(self):
        left = self.parse_multiplicative()
        while self.current_token() and self.current_token()[1] in ['+', '-']:
            op = self.current_token()[1]
            self.advance()
            right = self.parse_multiplicative()
            left = BinaryOpNode(left, op, right)
        return left

    def parse_multiplicative(self):
        left = self.parse_unary()
        while self.current_token() and self.current_token()[1] in ['*', '/', '%', '**', '//']:
            op = self.current_token()[1]
            self.advance()
            right = self.parse_unary()
            left = BinaryOpNode(left, op, right)
        return left

    def parse_unary(self):
        token = self.current_token()
        if token and token[1] in ['!', '-', '++', '--']:
            op = token[1]
            self.advance()
            operand = self.parse_unary()
            return UnaryOpNode(op, operand)
        else:
            return self.parse_primary()

    def parse_primary(self):
        token = self.current_token()
        if not token:
            raise SemanticError("Unexpected end of expression", self.tokens[self.index-1][1][0])
        if token[1] == 'givenchy':
            self.advance()  # Skip 'givenchy'
            self.expect('(', "Expected '(' after 'givenchy'")
            prompt_token = self.current_token()
            if prompt_token[1] != 'chika_literal':
                raise SemanticError("Expected string literal as argument for 'givenchy'", self.tokens[self.index][1][0])
            prompt_value = prompt_token[0].strip('"')
            self.advance()
            self.expect(')', "Expected ')' after 'givenchy' argument")
            return InputCallNode(prompt_value)
        if token[1].endswith('_literal'):
            lit_type = token[1].split('_')[0]
            node = LiteralNode(token[0], lit_type)
            self.advance()
            return node
        elif token[1] in ['korik', 'eme']:
            self.advance()
            token_value = True if token[1] == 'korik' else False
            return LiteralNode(token_value, 'eklabool')
        elif token[1] == 'id':
            ident_name = token[0]
            self.advance()
            if self.current_token() and self.current_token()[1] == '(':
                return self.parse_function_call_expr(ident_name)
            node = IdentifierNode(ident_name)
            while self.current_token() and self.current_token()[1] == '[':
                self.advance()  # Skip '['
                index_expr = self.parse_expression()
                self.expect(']', "Missing ']' in array access")
                node = ArrayAccessNode(node, [index_expr])
            while self.current_token() and self.current_token()[1] in ['++', '--']:
                op = self.current_token()[1]
                self.advance()
                node = UnaryOpNode(op, node, is_postfix=True)
            return node
        elif token[1] == '(':
            self.advance()  # Skip '('
            expr = self.parse_expression()
            self.expect(')', "Missing ')' in expression")
            return expr
        else:
            raise SemanticError(f"Unexpected token '{token[0]}' in expression", self.tokens[self.index][1][0])
