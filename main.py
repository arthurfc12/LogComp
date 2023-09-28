import sys
import re
import string
from Node import Node, BinOp, UnOp, IntVal, NoOp

PLUS = "+"
MINUS = "-"
MULT = "*"
DIV = "/"
INT = "NUM"
EOF = "End of file"
OPENP = "("
CLOSEP = ")"


class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value


class PreProcessing:
    def __init__(self, source):
        self.source = source
          
    def filter(self):
        return re.sub(r"\/\/.*$","",self.source,flags=re.MULTILINE)


class Tokenizer:
    def __init__(self, source, next = None, position = 0):
        self.source = str(source)
        self.position = position
        self.next = next

    def selectNext(self):
        value = ""
        type = None

        if self.position >= len(self.source):
            value = "EOF"
            type = EOF
            self.next = Token(type=type, value=value)
            return

        while self.position != len(self.source):
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
            elif self.source[self.position] == " ":
                self.position += 1
                continue
            else:
                raise Exception("valor não previsto")


class Parser:
    tokens = None

    
    
    def parseExpression(self):
        node = self.parseTerm()
        while (self.tokens.next.type == PLUS or self.tokens.next.type == MINUS):
            if self.tokens.next.type == PLUS:
                self.tokens.selectNext()
                node = BinOp(PLUS,[node,self.parseTerm()])
            elif self.tokens.next.type == MINUS:
                self.tokens.selectNext()
                node = BinOp(MINUS,[node,self.parseTerm()])
        
        if self.tokens.next.type == INT:
            raise Exception("Erro no parseExpression")
           
        return node

    def parseTerm(self):
        node = self.parseFactor()
        while self.tokens.next.type == MULT or self.tokens.next.type == DIV:
            if self.tokens.next.type == MULT:
                self.tokens.selectNext()
                node = BinOp(MULT,[node,self.parseFactor()])
            elif self.tokens.next.type == DIV:
                self.tokens.selectNext()
                node = BinOp(DIV,[node,self.parseFactor()])
            else:
                raise Exception("Erro no parseTerm")
            
        return node

    
    def parseFactor(self):
        node = 0
        if self.tokens.next.type == INT:
            node = IntVal(self.tokens.next.value, [])
            self.tokens.selectNext()
        elif self.tokens.next.type == PLUS:
            self.tokens.selectNext()
            node = UnOp(PLUS,[self.parseFactor()])
        elif self.tokens.next.type == MINUS:
            self.tokens.selectNext()
            node = UnOp(MINUS,[self.parseFactor()])
            
        elif self.tokens.next.type == OPENP:
            self.tokens.selectNext()
            node = self.parseExpression()
            if self.tokens.next.type == CLOSEP:
                self.tokens.selectNext()
            else:
                raise Exception("Erro no parseFactor")
        else:
            raise Exception("Erro no parseFactor")
        return node
        

    
    def run(self, code):
        file = open(code,"r")
        new = file.read()
        file.close()
        filtered = PreProcessing(new).filter()
        filtered = filtered.strip()
        self.tokens = Tokenizer(filtered)
        self.tokens.selectNext()
        master_node = self.parseExpression()
        if self.tokens.next.type == EOF:
            return master_node.Evaluate()
        else:
            raise Exception("Code Incorrect")


if __name__ == "__main__":
    chain = sys.argv[1]

    parser = Parser()

    final = parser.run(chain)
    
    print(final)
