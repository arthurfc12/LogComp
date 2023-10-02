from Token import Token
import re

PLUS = "+"
MINUS = "-"
MULT = "*"
DIV = "/"
INT = "NUM"
EOF = "End of file"
OPENP = "("
CLOSEP = ")"
IDENTIFIER = "IDENTIFIER"
EQUAL = "="
PRINT = "Println"
END = "\n"

class Tokenizer:
    def __init__(self, source, next=None, position=0):
        self.source = str(source)
        self.next = next
        self.position = position

    def selectNext(self):
        value = ""
        type = None

        if self.position >= len(self.source):
            value = "EOF"
            type = EOF
            self.next = Token(type=type, value=value)
            return

        while self.position < len(self.source):
            if self.position >= len(self.source):
                self.next = Token(EOF, " ")
                return
            if re.match("[0-9]", self.source[self.position]):
                while self.position < len(self.source):
                    if re.match(r"[0-9]", self.source[self.position]):
                        value += self.source[self.position]
                        self.position += 1
                    else:
                        type = INT
                        self.next = Token(type=type, value=int(value))
                        return
                type = INT
                self.next = Token(type=type, value=int(value))
                return
            elif self.source[self.position] == "+":
                value = self.source[self.position]
                type = PLUS
                self.next = Token(type=type, value=value)
                self.position += 1
                return
            elif self.source[self.position] == "-":
                value = self.source[self.position]
                type = MINUS
                self.next = Token(type=type, value=value)
                self.position += 1
                return
            elif self.source[self.position] == "*":
                value = self.source[self.position]
                type = MULT
                self.next = Token(type=type, value=value)
                self.position += 1
                return
            elif self.source[self.position] == "/":
                value = self.source[self.position]
                type = DIV
                self.next = Token(type=type, value=value)
                self.position += 1
                return
            elif self.source[self.position] == "(":
                value = self.source[self.position]
                type = OPENP
                self.next = Token(type=type, value=value)
                self.position += 1
                return
            elif self.source[self.position] == ")":
                value = self.source[self.position]
                type = CLOSEP
                self.next = Token(type=type, value=value)
                self.position += 1
                return
            elif self.source[self.position] == "=":
                value = self.source[self.position]
                type = EQUAL
                self.next = Token(type=type, value=value)
                self.position += 1
                return
            elif self.source[self.position] == "\n":
                value = self.source[self.position]
                type = END
                self.next = Token(type=type, value=value)
                self.position += 1
                return
            elif re.match("[a-zA-Z]", self.source[self.position]):
                while self.position < len(self.source) and re.match(r"[a-zA-Z1-9_]", self.source[self.position]):
                    value += self.source[self.position]
                    self.position += 1
                if value == PRINT:
                    type = PRINT
                    self.next = Token(type=type, value=str(value))
                else:
                    type = IDENTIFIER
                    self.next = Token(type=type, value=str(value))
                return
            elif self.source[self.position] == " ":
                self.position += 1
                continue
            else:
                print(self.source[self.position])
                raise Exception("valor não previsto")
