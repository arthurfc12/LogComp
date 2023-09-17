from Token import Token

class Tokenizer:
    def __init__(self, source):
        self.source = source
        self.position = 0
        self.actual = None

    def selectNext(self):
        if self.position >= len(self.source):
            self.actual = Token("EOF", " ")
            return self.actual

        if self.source[self.position] == " ":
            self.position += 1
            self.selectNext()
        elif self.source[self.position] == "*":
            self.position += 1
            self.actual = Token("MULT", "*")
            return self.actual
        elif self.source[self.position] == "/":
            self.position += 1
            self.actual = Token("DIV", "/")
            return self.actual
        elif self.source[self.position] == "+":
            self.position += 1
            self.actual = Token("PLUS", " ")
            return self.actual
        elif self.source[self.position] == "-":
            self.position += 1
            self.actual = Token("MINUS", " ")
            return self.actual
        elif self.source[self.position] == "(":
            self.position += 1
            self.actual = Token("OPENP", " ")
            return self.actual
        elif self.source[self.position] == ")":
            self.position += 1
            self.actual = Token("CLOSEP", " ")
            return self.actual
        elif self.source[self.position].isnumeric():
            candidato = self.source[self.position]
            self.position += 1

            while self.position < len(self.source):
                if self.source[self.position].isnumeric():
                    candidato += self.source[self.position]
                    self.position += 1
                else:
                    self.actual = Token("NUM", int(candidato))
                    return self.actual

            self.actual = Token("NUM", int(candidato))
            return self.actual
        else:
            raise ValueError
