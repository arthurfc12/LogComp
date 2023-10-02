import sys
import re
import string
from Node import Node, BinOp, UnOp, IntVal, NoOp, SymbolTable,Identifier,Assigment,Println,Block
from Token import Token
from Tokenizer import Tokenizer

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

class PreProcessing:
    def __init__(self, source):
        self.source = source
          
    def filter(self):
        with open(self.source, 'r') as input_file:
                code = input_file.read()

        code = re.sub(r'//.*', '', code)
        return code

class Parser:
    tokens = None

    def parseBlock(self):
        childrens = []
        while self.tokens.next.type != EOF:
            node = self.parseStatement()
            childrens.append(node)
        master = Block(None,childrens)
        return master
    
    def parseStatement(self):
        if self.tokens.next.type == IDENTIFIER:
            variable = Identifier(self.tokens.next.value,[])
            self.tokens.selectNext()
            if self.tokens.next.type == EQUAL:
                self.tokens.selectNext()
                variable = Assigment(EQUAL,[variable,self.parseExpression()])
            else:
                raise Exception("erro no statement")
        elif self.tokens.next.type == PRINT:
            self.tokens.selectNext()
            if self.tokens.next.type == OPENP:
                self.tokens.selectNext()
                variable = Println(PRINT,[self.parseExpression()])
                if self.tokens.next.type == CLOSEP:
                    self.tokens.selectNext()
                    if self.tokens.next.type == END:
                        self.tokens.selectNext()
                    else:
                        raise Exception("erro no statement")
                else:
                    raise Exception("erro no statement")
        elif self.tokens.next.type == END:
            self.tokens.selectNext()
            variable = NoOp("N",[])
        else:
            raise Exception("erro no statement")
            
        return variable
    
    def parseExpression(self):
        node = self.parseTerm()
        while self.tokens.next.type == PLUS or self.tokens.next.type == MINUS:
            if self.tokens.next.type == PLUS:
                self.tokens.selectNext()
                node = BinOp(PLUS,[node,self.parseTerm()])
            elif self.tokens.next.type == MINUS:
                self.tokens.selectNext()
                node = BinOp(MINUS,[node,self.parseTerm()])
                
        if self.tokens.next.type == INT:
            raise Exception("erro no expression")
           
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
                raise Exception("erro no term")
            
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
        elif self.tokens.next.type == CLOSEP:
            self.tokens.selectNext()
            node = self.parseExpression()
            if self.tokens.next.type == OPENP:
                self.tokens.selectNext()
            else:
                raise Exception("erro no factor")
        elif self.tokens.next.type == IDENTIFIER:
            node = Identifier(self.tokens.next.value,[])
            self.tokens.selectNext()
        else:
            print(self.tokens.next.type)
            print(self.tokens.next.value)
            raise Exception("erro no factor")
        
        return node
    
    def run(self, code):
        filtered = PreProcessing(code).filter()
        identifier_table = SymbolTable()
        self.tokens = Tokenizer(filtered)
        self.tokens.selectNext()
        master_node = self.parseBlock()
        
        if self.tokens.next.type == EOF:
            a = master_node.Evaluate(identifier_table)
            return a
        else:
            raise Exception("erro no run")

if __name__ == "__main__":
    chain = sys.argv[1]

    parser = Parser()

    final = parser.run(chain)
