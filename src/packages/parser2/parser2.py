from .lexer import Lexer, Token
from .error_handler import UnexpectedError

class Parser:
    def __init__(self, tokens):
        self.tokens = list(tokens)
        self.pos = 0

    def peek(self) -> Token:
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return Token("EOF", "", -1, -1)

    def advance(self) -> Token:
        tok = self.peek()
        self.pos += 1
        return tok

    def expect(self, kind: str) -> Token:
        tok = self.peek()
        if tok.type != kind:
            raise UnexpectedError(
                f"Expected `{kind}` at {tok.line}:{tok.col}, got `{tok.type}`",
                (tok.line, tok.col)
            )
        return self.advance()

    def parse(self):
        node = self.program()
        if self.peek().type != "EOF":
            tok = self.peek()
            raise UnexpectedError(
                f"Extra token `{tok.value}` after end at {tok.line}:{tok.col}",
                (tok.line, tok.col)
            )
        return node

    # --- top-level productions ---

    def program(self):
        globals_ = []
        while self.peek().type in ("NAUR", "ANDA", "ANDAMHIE", "CHIKA", "EKLABOOL"):
            globals_.append(self.var_dec_init())

        first_func = None
        if not (self.peek().type == "SHIMENET" and self.tokens[self.pos+1].type == "KWEEN"):
            first_func = self.func_def()

        self.expect("SHIMENET")
        self.expect("KWEEN")
        self.expect("LPAR")
        self.expect("RPAR")
        self.expect("LBRACE")
        body = self.kween_body()
        self.expect("RBRACE")

        other_funcs = []
        while self.peek().type in ("ANDA", "ANDAMHIE", "CHIKA", "EKLABOOL", "SHIMENET"):
            other_funcs.append(self.func_def())

        return {
            "type": "Program",
            "globals": globals_,
            "entry_func": first_func,
            "body": body,
            "other_funcs": other_funcs
        }

    # --- declarations ---

    def var_dec_init(self):
        if self.peek().type == "NAUR":
            self.advance()
            dtype = self.data_type()
            name = self.expect("ID").value
            self.expect("SEMICOLON")
            return {"type":"VarDeclInit","naur":True,"dtype":dtype,"name":name}

        tok = self.peek()
        if tok.type in ("ANDA","ANDAMHIE","CHIKA","EKLABOOL"):
            dtype = self.data_type()
            name = self.expect("ID").value
            self.expect("SEMICOLON")
            return {"type":"VarDecl","dtype":dtype,"name":name}

        if tok.type == "SHIMENET":
            self.advance()
            name = self.expect("ID").value
            self.expect("SEMICOLON")
            return {"type":"FuncPointerDecl","name":name}

        return None

    def data_type(self):
        tok = self.peek()
        if tok.type in ("ANDA","ANDAMHIE","CHIKA","EKLABOOL"):
            return self.advance().type
        raise UnexpectedError(
            f"Expected a data_type at {tok.line}:{tok.col}, got {tok.type}",
            (tok.line,tok.col)
        )

    # --- function definitions ---

    def func_def(self):
        ret_tok = self.peek()
        if ret_tok.type in ("ANDA","ANDAMHIE","CHIKA","EKLABOOL","SHIMENET"):
            ret = self.advance().type
        else:
            raise UnexpectedError(
                f"Expected return_type at {ret_tok.line}:{ret_tok.col}",
                (ret_tok.line,ret_tok.col)
            )
        name = self.expect("ID").value
        self.expect("LPAR")
        params = self.parameters()
        self.expect("RPAR")
        self.expect("LBRACE")
        body = self.func_body()
        self.expect("RBRACE")
        return {"type":"FuncDef","return":ret,"name":name,"params":params,"body":body}

    def parameters(self):
        params = []
        if self.peek().type in ("ANDA","ANDAMHIE","CHIKA","EKLABOOL"):
            while True:
                dtype = self.data_type()
                name  = self.expect("ID").value
                params.append((dtype,name))
                if self.peek().type == "COMMA":
                    self.advance()
                    continue
                break
        return params

    def func_body(self):
        stmts = []
        while self.peek().type != "RBRACE":
            stmts.append(self.statements())
        return stmts

    def kween_body(self):
        return self.func_body()

    # --- statement dispatch ---

    def statements(self):
        tok = self.peek()
        if tok.type in ("NAUR","ANDA","ANDAMHIE","CHIKA","EKLABOOL"):
            return self.local_var_decl()
        if tok.type == "ID":
            return self.assign_call_stmts()
        if tok.type == "GIVENCHY":
            return self.input_stmts()
        if tok.type == "SERVE":
            return self.output_stmts()
        if tok.type == "ADELE":
            return self.append_stmts()
        if tok.type == "ADELETE":
            return self.delete_stmts()
        if tok.type == "PAK":
            return self.conditional_stmts()
        if tok.type in ("FORDA","KERI"):
            return self.loop_stmts()
        if tok.type == "VERSA":
            return self.switch_stmts()
        if tok.type == "PUSH":
            return self.return_stmts()
        if tok.type in ("PLUS_PLUS","MINUS_MINUS"):
            return self.unary_stmts()
        raise UnexpectedError(f"Unknown statement at {tok.line}:{tok.col}", (tok.line,tok.col))

    # --- local declarations inside functions ---

    def local_var_decl(self):
        naur_case = False
        if self.peek().type == "NAUR":
            naur_case = True
            self.advance()
        dtype = self.data_type()
        name = self.expect("ID").value
        init = None
        if self.peek().type == "EQUAL":
            self.advance()
            init = self.expression()
        self.expect("SEMICOLON")
        return {
            "type": "LocalVarDeclInit" if naur_case else "LocalVarDecl",
            "naur": naur_case,
            "dtype": dtype,
            "name": name,
            "init": init
        }

    # --- statements implementations ---

    def assign_call_stmts(self):
        name = self.expect("ID").value
        next_tok = self.peek()
        if next_tok.type in (
            "EQUAL","PLUS_EQUAL","MINUS_EQUAL","MODULO_EQUAL",
            "DIVIDE_EQUAL","FLOOR_EQUAL","TIMES_EQUAL","EXPONENTIATE_EQUAL"
        ):
            op = self.advance().type
            value = self.expression()
            self.expect("SEMICOLON")
            return {"type":"AssignStmt","target":name,"op":op,"value":value}
        if next_tok.type == "LPAR":
            self.advance()
            args = self.arguments()
            self.expect("RPAR")
            self.expect("SEMICOLON")
            return {"type":"CallStmt","name":name,"args":args}
        raise UnexpectedError(
            f"Expected assignment or call at {next_tok.line}:{next_tok.col}",
            (next_tok.line,next_tok.col)
        )

    def input_stmts(self):
        dtype = None
        if self.peek().type in ("ANDA","ANDAMHIE","CHIKA","EKLABOOL"):
            dtype = self.data_type()
        target = self.expect("ID").value
        self.expect("EQUAL")
        self.expect("GIVENCHY")
        self.expect("LPAR")
        value = self.expression()
        self.expect("RPAR")
        self.expect("SEMICOLON")
        return {"type":"InputStmt","dtype":dtype,"target":target,"value":value}

    def output_stmts(self):
        self.expect("SERVE")
        self.expect("LPAR")
        expr = self.expression()
        self.expect("RPAR")
        self.expect("SEMICOLON")
        return {"type":"OutputStmt","value":expr}

    def append_stmts(self):
        self.expect("ADELE")
        self.expect("LPAR")
        name = self.expect("ID").value
        self.expect("COMMA")
        value = self.expression()
        self.expect("RPAR")
        self.expect("SEMICOLON")
        return {"type":"AppendStmt","target":name,"value":value}

    def delete_stmts(self):
        self.expect("ADELETE")
        self.expect("LPAR")
        name = self.expect("ID").value
        self.expect("LSQB")
        index = self.expression()
        self.expect("RSQB")
        self.expect("RPAR")
        self.expect("SEMICOLON")
        return {"type":"DeleteStmt","target":name,"index":index}

    def conditional_stmts(self):
        self.expect("PAK")
        self.expect("LPAR")
        cond = self.expression()
        self.expect("RPAR")
        self.expect("LBRACE")
        then_branch = []
        while self.peek().type != "RBRACE":
            then_branch.append(self.statements())
        self.expect("RBRACE")
        else_branch = None
        if self.peek().type == "GANERN":
            self.advance()
            if self.peek().type == "PAK":
                else_branch = [self.conditional_stmts()]
            else:
                self.expect("LBRACE")
                else_branch = []
                while self.peek().type != "RBRACE":
                    else_branch.append(self.statements())
                self.expect("RBRACE")
        return {"type":"IfStmt","cond":cond,"then":then_branch,"else":else_branch}

    def loop_stmts(self):
        if self.peek().type == "FORDA":
            return self.forda_statement()
        return self.keri_statement()

    def forda_statement(self):
        self.expect("FORDA")
        self.expect("LPAR")
        dtype = None
        if self.peek().type in ("ANDA","ANDAMHIE","CHIKA","EKLABOOL"):
            dtype = self.data_type()
        var = self.expect("ID").value
        self.expect("FROM")
        start = self.expression()
        self.expect("TO")
        end = self.expression()
        step = None
        if self.peek().type == "STEP":
            self.advance()
            step = self.expression()
        self.expect("RPAR")
        self.expect("LBRACE")
        body = []
        while self.peek().type != "RBRACE":
            body.append(self.statements())
        self.expect("RBRACE")
        return {"type":"ForStmt","var":var,"start":start,"end":end,"step":step,"body":body}

    def keri_statement(self):
        self.expect("KERI")
        self.expect("LPAR")
        cond = self.expression()
        self.expect("RPAR")
        self.expect("LBRACE")
        body = []
        while self.peek().type != "RBRACE":
            body.append(self.statements())
        self.expect("RBRACE")
        return {"type":"WhileStmt","cond":cond,"body":body}

    def switch_stmts(self):
        self.expect("VERSA")
        self.expect("LPAR")
        expr = self.expression()
        self.expect("RPAR")
        self.expect("LBRACE")
        cases = []
        while self.peek().type == "BETSUNG":
            self.advance()
            case_val = self.expression()
            self.expect("COLON")
            stmts = []
            while self.peek().type not in ("BETSUNG","DITECH","RBRACE"):
                stmts.append(self.statements())
            cases.append({"value":case_val,"stmts":stmts})
        default = None
        if self.peek().type == "DITECH":
            self.advance()
            self.expect("COLON")
            default = []
            while self.peek().type != "RBRACE":
                default.append(self.statements())
        self.expect("RBRACE")
        return {"type":"SwitchStmt","expr":expr,"cases":cases,"default":default}

    def return_stmts(self):
        self.expect("PUSH")
        value = self.expression()
        self.expect("SEMICOLON")
        return {"type":"ReturnStmt","value":value}

    def unary_stmts(self):
        tok = self.peek()
        # prefix op
        if tok.type in ("PLUS_PLUS","MINUS_MINUS"):
            op = self.advance().type
            target = self.expect("ID").value
            self.expect("SEMICOLON")
            return {"type":"UnaryStmt","op":op,"target":target,"post":False}
        # postfix op
        target = self.expect("ID").value
        op_tok = self.peek()
        if op_tok.type in ("PLUS_PLUS","MINUS_MINUS"):
            op = self.advance().type
            self.expect("SEMICOLON")
            return {"type":"UnaryStmt","op":op,"target":target,"post":True}
        raise UnexpectedError(f"Invalid unary statement at {tok.line}:{tok.col}", (tok.line, tok.col))

    # --- expressions & arguments ---

    def expression(self):
        tok = self.advance()
        return {"type":"Literal","value":tok.value}

    def arguments(self):
        args = []
        if self.peek().type != "RPAR":
            args.append(self.expression())
            while self.peek().type == "COMMA":
                self.advance()
                args.append(self.expression())
        return args
