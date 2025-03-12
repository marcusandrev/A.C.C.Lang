from lark import Transformer, v_args
from lark.tree import Tree

class SemanticError(Exception):
    """Custom error for semantic analysis."""
    def __init__(self, message, line=None, column=None):
        self.message = message
        self.line = line
        self.column = column

    def __str__(self):
        position = f" at line {self.line}, column {self.column}" if self.line and self.column else ""
        return f"Semantic Error{position}: {self.message}"


class SemanticAnalyzer(Transformer):
    def __init__(self):
        super().__init__()
        self.symbol_table = [{}]  # Stack-based symbol table (global scope at index 0)
        self.errors = []

    def error(self, message, token=None):
        """Logs errors with optional token position information."""
        line = token.line if hasattr(token, 'line') else None
        column = token.column if hasattr(token, 'column') else None
        self.errors.append(SemanticError(message, line, column))

    def push_scope(self):
        """Push a new local scope onto the symbol table stack."""
        self.symbol_table.append({})

    def pop_scope(self):
        """Remove the current local scope from the symbol table stack."""
        if len(self.symbol_table) > 1:  # Ensure we never pop the global scope
            self.symbol_table.pop()

    def current_scope(self):
        """Retrieve the current (innermost) scope."""
        return self.symbol_table[-1]

    def lookup(self, var):
        """Look for a variable in the current or global scope."""
        for scope in reversed(self.symbol_table):
            if var in scope:
                return scope[var]
        return None

    def get_value(self, item):
        """Helper to extract a string value from a Token or Tree."""
        if hasattr(item, "value"):
            return item.value
        elif hasattr(item, "children") and item.children:
            child = item.children[0]
            return child.value if hasattr(child, "value") else str(child)
        return str(item)

    @v_args(inline=True)
    def var_dec_init(self, *args):
        """
        Handles:
        - Single variable declaration: anda a;
        - Variable initialization: anda a = 5;
        - Multiple variables: anda a, b, c;
        - Multiple initialization: anda a = 5, b = 2, c = 3;
        """
        if len(args) < 2:
            self.error("Invalid variable declaration.")

        naur_case = args[0] if args[0] != '' else None  # Check if 'naur' is present
        data_type = self.get_value(args[1])  # Extract the type (e.g., 'anda')

        # **Extract all variable names including multi_init_values**
        def extract_variables(node):
            """ Recursively extract all variable names from var_init and multi_init_values. """
            variables = []
            if isinstance(node, Tree):
                if node.data == "var_init":
                    var_name = self.get_value(node.children[0])  # Extract first variable
                    variables.append(var_name)
                elif node.data == "multi_init_values":
                    for child in node.children:
                        if isinstance(child, Tree) and child.data == "multi_init_values_tail":
                            var_name = self.get_value(child.children[0])
                            variables.append(var_name)
                        elif isinstance(child, Tree):
                            variables.extend(extract_variables(child))
            return variables

        # **Get all variables declared in this statement**
        variables = extract_variables(args[2])  # Extract first variable + multi_init_values

        # **Store variables in symbol table**
        for var_name in variables:
            if var_name in self.current_scope():
                self.error(f"Variable '{var_name}' redeclared in the same scope.")
            else:
                self.current_scope()[var_name] = {
                    "type": data_type,
                    "const": naur_case is not None  # If 'naur' is present, it's a constant
                }

    @v_args(inline=True)
    def multi_var_dec_init(self, data_type, *var_assignments):
        """
        Handles multiple variable declarations:
        - anda a, b, c;
        - anda a = 5, b = 2, c = 3;
        """
        type_val = self.get_value(data_type)

        for var_assign in var_assignments:
            var_name_token = var_assign.children[0] if isinstance(var_assign, Tree) and var_assign.children else var_assign
            var_name = self.get_value(var_name_token)

            if var_name in self.current_scope():
                self.error(f"Variable '{var_name}' redeclared in the same scope.", var_assign)
            else:
                self.current_scope()[var_name] = {"type": type_val}

    @v_args(inline=True)
    def array_dec_init(self, data_type, array_name, array_size, array_values=None):
        """
        Handles array declarations:
        - anda a[2] = {0, 1};
        - anda a[2][2] = {{0, 1}, {2, 3}};
        - anda a[2][2][2] = {{{0, 1}, {2, 3}}, {{4, 5}, {6, 7}}};
        """
        type_val = self.get_value(data_type)
        array_name = self.get_value(array_name)

        # Extract array dimensions
        dimensions = []
        for size in array_size.children:
            dimensions.append(int(self.get_value(size)))

        if array_name in self.current_scope():
            self.error(f"Array '{array_name}' redeclared in the same scope.", array_name)
        else:
            self.current_scope()[array_name] = {
                "type": type_val,
                "dimensions": dimensions
            }

        # Validate array values if initialized
        if array_values:
            expected_size = 1
            for dim in dimensions:
                expected_size *= dim

            actual_size = len(array_values.children) if hasattr(array_values, "children") else 0

            if actual_size != expected_size:
                self.error(f"Array '{array_name}' initialization size mismatch. Expected {expected_size}, got {actual_size}.")

    def analyze(self, tree: Tree):
        """Run semantic analysis on a parse tree."""
        self.transform(tree)  # Walk and process the tree
        if self.errors:
            for error in self.errors:
                print(error)
            return False
        print("Semantic analysis successful.")
        return True

# Semantic Analyzer is now updated with:
# - Single variable declaration handling
# - Multiple variable declaration handling
# - Array declaration handling with size checking

