import sys
import re
from PreProcessing import PreProcessing
from Node import BinOp, IntVal, NoOp, UnOp
from Tokenizer import Tokenizer


class Parser:
    tokens = None

    @staticmethod
    def parseFactor():

        if(Parser.tokens.actual.type == "NUM"):
            node = IntVal(Parser.tokens.actual.value,
                          [])
            Parser.tokens.selectNext()

        elif(Parser.tokens.actual.type == "MINUS"):
            Parser.tokens.selectNext()
            node = UnOp('-', [Parser.parseFactor()])

        elif(Parser.tokens.actual.type == "PLUS"):
            Parser.tokens.selectNext()
            node = UnOp('+', [Parser.parseFactor()])

        elif(Parser.tokens.actual.type == "OPNEP"):
            Parser.tokens.selectNext()
            node = Parser.parseExpression()
            if(Parser.tokens.actual.type == "CLOSEP"):
                Parser.tokens.selectNext()
            else:
                raise ValueError("ERROR")

        else:
            raise ValueError("ERROR")

        return node

    @staticmethod
    def parseTerm():
        node = Parser.parseFactor()

        while((Parser.tokens.actual.type == "MULT" or Parser.tokens.actual.type == "DIV")):

            if(Parser.tokens.actual.type == "MULT"):
                Parser.tokens.selectNext()
                node = BinOp('*', [node, Parser.parseFactor()])

            elif(Parser.tokens.actual.type == "DIV"):
                Parser.tokens.selectNext()
                node = BinOp('/', [node, Parser.parseFactor()])

        return node

    @staticmethod
    def parseExpression():
        node = Parser.parseTerm()

        while((Parser.tokens.actual.type == "MINUS" or Parser.tokens.actual.type == "PLUS")):

            if(Parser.tokens.actual.type == "MINUS"):
                Parser.tokens.selectNext()
                node = BinOp('-', [node, Parser.parseTerm()])

            elif(Parser.tokens.actual.type == "PLUS"):
                Parser.tokens.selectNext()
                node = BinOp('+', [node, Parser.parseTerm()])

        return node

    def run(code):
        f = open(code, "r")
        code = f.read()
        f.close()
        postProCode = PreProcessing.filter(code)
        Parser.tokens = Tokenizer(postProCode)
        Parser.tokens.selectNext()

        result = Parser.parseExpression()
        if(Parser.tokens.actual.type != "EOF"):
            raise ValueError("ERROR")
        return result.Evaluate()


if(len(sys.argv) <= 1):
    raise ValueError("ERROR")


arg = str(sys.argv[1])
print(Parser.run(arg))