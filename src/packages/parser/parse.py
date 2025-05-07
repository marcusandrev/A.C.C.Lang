from error_handler import UnexpectedError

class Parser:
    def __init__(self, token_stream):
        self._token_stream = list(token_stream)
        self._source_code = ""
        for lexeme, token_type in self._token_stream:
            if token_type == "whitespace":
                self._source_code += " "
            elif token_type == "newline":
                self._source_code += "\n"
            elif token_type.startswith("id"):
                self._source_code += "id"
            else:
                self._source_code += token_type

    def get_first_set(self, non_terminals, productions):
        first_set = {nt: set() for nt in non_terminals}

        def first(symbol):
            if symbol not in non_terminals:          # terminal
                return {symbol}
            if not first_set[symbol]:
                for prod in productions:
                    head, body = map(str.strip, prod.split("->"))
                    body = body.split()
                    if head == symbol:
                        if body[0] == "λ":
                            first_set[symbol].add("λ")
                        else:
                            for sym in body:
                                sym_first = first(sym)
                                first_set[symbol].update(sym_first - {"λ"})
                                if "λ" not in sym_first:
                                    break
                            else:
                                first_set[symbol].add("λ")
            return first_set[symbol]

        for nt in non_terminals:
            first(nt)
        return first_set

    def get_follow_set(self, non_terminals, productions, first_set):
        follow_set = {nt: set() for nt in non_terminals}
        start_symbol = non_terminals[0]
        follow_set[start_symbol].add("$")

        def follow(symbol):
            for prod in productions:
                head, body = map(str.strip, prod.split("->"))
                body = body.split()
                for i, sym in enumerate(body):
                    if sym == symbol:
                        if i + 1 < len(body):
                            nxt = body[i + 1]
                            if nxt not in non_terminals:
                                follow_set[symbol].add(nxt)
                            else:
                                follow_set[symbol].update(first_set[nxt] - {"λ"})
                                if "λ" in first_set[nxt]:
                                    follow_set[symbol].update(follow(head))
                        else:
                            if head != symbol:
                                follow_set[symbol].update(follow(head))
            return follow_set[symbol]

        for nt in non_terminals:
            follow(nt)
        return follow_set

    def get_predict_set(self, productions, first_set, follow_set):
        predict_set = {}
        for prod in productions:
            head, body = map(str.strip, prod.split("->"))
            body = body.split()
            if body[0] == "λ":
                predict_set[prod] = follow_set[head]
            else:
                predict_set[prod] = set()
                if body[0] not in first_set:               # terminal
                    predict_set[prod].add(body[0])
                else:
                    predict_set[prod].update(first_set[body[0]] - {"λ"})
                    if "λ" in first_set[body[0]]:
                        predict_set[prod].update(follow_set[head])
        return predict_set

    def _locate(self, abs_index: int) -> tuple[str, tuple[int, int]]:
        prefix = self._source_code[:abs_index]
        line_no = prefix.count("\n") + 1
        col_no = abs_index - prefix.rfind("\n")          # works even if -1
        line_text = self._source_code.splitlines()[line_no - 1]
        return line_text, (line_no, col_no)

    def parse(self, input_string, non_terminals, productions, predict_set):
        stack = ["$", non_terminals[0]]
        tokens = input_string.split() + ["$"]
        index = 0                                        # token pointer

        while stack:
            top = stack.pop()
            if top == "λ":                               # ε production
                continue

            current_tok = tokens[index]

            # 1. exact terminal match
            if top == current_tok:
                index += 1
                continue

            # 2. expand non‑terminal
            if top in non_terminals:
                for prod in productions:
                    head, body = map(str.strip, prod.split("->"))
                    body_symbols = body.split()
                    if head == top and current_tok in predict_set[prod]:
                        stack.extend(reversed(body_symbols))
                        break
                else:  # no prod matched
                    line, pos = self._locate(len(" ".join(tokens[:index])))
                    raise UnexpectedError(line, pos) from None
                continue

            # 3. stray terminal on stack – syntax error
            line, pos = self._locate(len(" ".join(tokens[:index])))
            raise UnexpectedError(line, pos) from None

        # ensure all input was consumed
        if tokens[index] != "$":
            line, pos = self._locate(len(" ".join(tokens[:index])))
            raise UnexpectedError(line, pos) from None
        return True

    def start(self):
        non_terminals, productions = [], []

        with open("Files/cfg/cfg.txt", "r", encoding="utf-8") as f:
            for line in f:
                head = line.split("->")[0].strip()
                if head not in non_terminals:
                    non_terminals.append(head)
                productions.append(line.strip())

        first_set  = self.get_first_set(non_terminals, productions)
        follow_set = self.get_follow_set(non_terminals, productions, first_set)
        predict_set= self.get_predict_set(productions, first_set, follow_set)

        print("_"*20, "FIRST", "_"*20)
        for nt in first_set:
            print(f"{nt}: {first_set[nt]}")
        print("_"*20, "FOLLOW", "_"*20)
        for nt in follow_set:
            print(f"{nt}: {follow_set[nt]}")
        print("_"*20, "PREDICT", "_"*20)
        for prod in predict_set:
            print(f"{prod.replace('λ', 'λ')}: {predict_set[prod]}")

        # ---- parse your own reconstructed source
        try:
            self.parse(self._source_code, non_terminals, productions, predict_set)
            print("No syntax errors ✔")
        except UnexpectedError as err:
            print("Unexpected token:", err)

if __name__ == "__main__":
    tokens = [
        ("shimenet", "shimenet"), (" ", "whitespace"),
        ("kween", "kween"), (" ", "whitespace"),
        ("(", "("), (")", ")"), (" ", "whitespace"),
        ("{", "{"), (" ", "whitespace"),
        ("anda", "anda"), (" ", "whitespace"),
        ("id", "id_x"), (" ", "whitespace"),
        ("=", "="), (" ", "whitespace"),
        ("anda_literal", "anda_literal"), (";", ";"),
        ("}", "}"), ("\n", "newline")
    ]

    Parser(tokens).start()
