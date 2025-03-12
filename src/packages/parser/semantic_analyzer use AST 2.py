from lark import Transformer, v_args
from lark.tree import Tree
from .error_handler import SemanticError

class SemanticAnalyzer(Transformer):
    def __init__(self):
        super().__init__()
        self.symbol_table = []  # Stack-based symbol table (global scope at index 0)
        self.errors = []

    def error(self, message, token=None):
        """Logs errors with optional token position information."""
        line = token.line if hasattr(token, 'line') else None
        column = token.column if hasattr(token, 'column') else None
        self.errors.append(SemanticError(message, line, column))

    def push_scope(self):
        """Push a new local scope onto the symbol table stack."""
        print(self.symbol_table)
        self.symbol_table.append({})

    def pop_scope(self):
        """Remove the current local scope from the symbol table stack."""
        print(self.symbol_table)
        if len(self.symbol_table) > 1:  # Ensure we never pop the global scope
            self.symbol_table.pop()

    def current_scope(self):
        """Retrieve the current (innermost) scope."""
        print(self.symbol_table)
        return self.symbol_table[-1]

    def lookup(self, var):
        """
        Look for a variable in the current scope first,
        then in the outer (global) scope.
        """
        for scope in reversed(self.symbol_table):  # Start from the innermost
            if var in scope:
                return scope[var]
        return None

    def get_value(self, item):
        """Helper to extract a string value from a Token or a Tree."""
        if hasattr(item, "value"):
            return item.value
        elif hasattr(item, "children") and item.children:
            child = item.children[0]
            return child.value if hasattr(child, "value") else str(child)
        return str(item)

    @v_args(inline=True)
    def var_dec_init(self, const_specifier, data_type, var_init, *args):
        """
        Handles global variable declarations.
        Example:
            naur anda x;
        """
        const_flag = self.get_value(const_specifier)  # Should be "naur"
        type_val = self.get_value(data_type)  # Should be "anda"

        # Extract variable name
        var_name_token = var_init.children[0] if isinstance(var_init, Tree) and var_init.children else var_init
        var_name = self.get_value(var_name_token)

        if var_name in self.symbol_table[0]:  # Check only global scope
            self.error(f"Semantic Error: Variable '{var_name}' redeclared in global scope.", var_init)
        else:
            # Store variable in the global scope symbol table
            self.symbol_table[0][var_name] = {
                "type": type_val,
                "const": const_flag == "naur"
            }

    @v_args(inline=True)
    def local_dec_init(self, *args):
        """
        Handles local variable declarations inside functions.
        Example:
            naur_case data_type var_init SEMICOLON
        """
        var_name_token = None
        type_val = None

        if len(args) == 4:
            _, type_token, var_init_tree, _ = args
            var_name_token = var_init_tree.children[0]
            type_val = self.get_value(type_token)
        elif len(args) == 5:
            type_token, var_name_token, _, _, _ = args
            type_val = self.get_value(type_token)

        if var_name_token:
            var = self.get_value(var_name_token)

            # Ensure variable is stored in the current function’s local scope
            if var in self.current_scope():
                self.error(f"Semantic Error: Variable '{var}' redeclared in local scope.", var_name_token)
            else:
                self.current_scope()[var] = {"type": type_val}

    @v_args(inline=True)
    def assign_stmts(self, var_name, *_):
        """
        Handles assignments such as:
            x = 10;
        Ensures variables exist before assignment.
        """
        var = var_name.value  

        # Check if the variable exists in the current function's local scope or global scope
        if self.lookup(var) is None:
            self.error(f"Semantic Error: Variable '{var}' used before declaration.", var_name)

    @v_args(inline=True)
    def func_def(self, *args):
        """
        Handles function definitions.
        Example:
            shimenet sum() { ... }
        """
        if len(args) < 2:
            return  # Skip if function definition is empty

        return_type, func_name = args[:2]
        fname = self.get_value(func_name)

        if fname in self.symbol_table[0]:  # Check in global scope
            self.error(f"Semantic Error: Function '{fname}' already defined.", func_name)
        else:
            self.symbol_table[0][fname] = {"type": "function"}  # Store function in global scope

        # Push a new scope for function's local variables
        self.push_scope()

    @v_args(inline=True)
    def func_call(self, func_name, *_):
        """
        Handles function calls.
        Example:
            myFunc();
        """
        fname = self.get_value(func_name)
        if self.lookup(fname) is None:
            self.error(f"Semantic Error: Function '{fname}' called before definition.", func_name)

    def analyze(self, tree: Tree):
        """Run semantic analysis on a parse tree."""
        self.transform(tree)  # Walk and process the tree
        if self.errors:
            for error in self.errors:
                print(error)
            return False
        print("Semantic analysis successful.")
        return True
