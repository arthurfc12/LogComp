import sys
from PreProcessing import PreProcessing
from Node import BinOp, IntVal, UnOp
from Tokenizer import Tokenizer

class Parser:
    def __init__(self, code):
        self.tokens = Tokenizer(PreProcessing(code).filter_expression())
        self.tokens.selectNext()

    def parse_factor(self):
        if self.tokens.actual.type == "NUM":
            node = IntVal(self.tokens.actual.value, [])
            self.tokens.selectNext()
        elif self.tokens.actual.type == "OPENP":
            self.tokens.selectNext()
            node = self.parse_expression()
            if self.tokens.actual.type != "CLOSEP":
                raise Exception("Parênteses não fechados")
            self.tokens.selectNext()
        elif self.tokens.actual.type in {"PLUS", "MINUS"}:
            operator = self.tokens.actual.type
            self.tokens.selectNext()
            node = UnOp(operator, [self.parse_factor()])
        else:
            raise Exception("Fator inválido")
        return node

    def parse_term(self):
        node = self.parse_factor()
        while self.tokens.actual.type in {"MULT", "DIV"}:
            operator = self.tokens.actual.type
            self.tokens.selectNext()
            node = BinOp(operator, [node, self.parse_factor()])
        return node

    def parse_expression(self):
        node = self.parse_term()
        while self.tokens.actual.type in {"PLUS", "MINUS"}:
            operator = self.tokens.actual.type
            self.tokens.selectNext()
            node = BinOp(operator, [node, self.parse_term()])
        return node

    def run(self):
        node = self.parse_expression()
        if self.tokens.actual.type != "EOF":
            raise Exception("EOF não encontrado")
        result = node.evaluate()
        print(result)

if __name__ == "__main__":
    code = open(sys.argv[1], "r").read()
    parser = Parser(code)
    parser.run()
