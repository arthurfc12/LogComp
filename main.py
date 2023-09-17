import sys
from PreProcessing import PreProcessing
from Node import BinOp, IntVal, NoOp, UnOp
from Tokenizer import Tokenizer


class Parser:
    tokens = None

    @staticmethod
    def parse_factor():
        node = 0

        if Parser.tokens.actual.type == "NUM":
            node = IntVal(Parser.tokens.actual.value,[])
            Parser.tokens.selectNext()
        elif Parser.tokens.actual.type == "OPENP":
            node = Parser.parse_expression()
            if Parser.tokens.actual.type != "CLOSEP":
                raise ValueError
            Parser.tokens.selectNext()
        elif Parser.tokens.actual.type == "PLUS":
            Parser.tokens.selectNext()
            node = UnOp("+",[Parser.parse_factor()])
        elif Parser.tokens.actual.type == "MINUS":
            Parser.tokens.selectNext()
            node = UnOp("-",[Parser.parse_factor()])
        else:
            raise Exception("Factor")  

        return node

    @staticmethod
    def parse_term():
        node = Parser.parse_factor()

        while Parser.tokens.actual.type == "MULT" or Parser.tokens.actual.type == "DIV":
            if Parser.tokens.actual.type == "MULT":
                Parser.tokens.selectNext()
                node = BinOp("*",[node, Parser.parse_factor()])
            elif Parser.tokens.actual.type == "DIV":
                Parser.tokens.selectNext()
                node = BinOp("/",[node, Parser.parse_factor()])
            else:
                raise Exception("Term")

        return node

    @staticmethod
    def parse_expression():
        Parser.tokens.selectNext()
        node = Parser.parse_term()

        while (Parser.tokens.actual.type == "PLUS" or Parser.tokens.actual.type == "MINUS") and Parser.tokens.actual.type != "EOF":
            if Parser.tokens.actual.type == "PLUS":
                Parser.tokens.selectNext()
                node = BinOp("+", [node, Parser.parse_term()])
            elif Parser.tokens.actual.type == "MINUS":
                Parser.tokens.selectNext()
                node = BinOp("-", [node, Parser.parse_term()])
            else:
                raise Exception("Expression")

        return node

    @staticmethod
    def run(code):
        file = open(code, "r")
        code = file.read()
        file.close()
        code_filter = PreProcessing(code).filter_expression()
        Parser.tokens = Tokenizer(code_filter)
        node = Parser.parse_expression()
        if Parser.tokens.actual.type != "EOF":
            raise ValueError
        print(node.evaluate())

if __name__ == "__main__":
    Parser.run(sys.argv[1])
