import sys
import re

class PreProcessing:
    def __init__(self, string_processed):
        self.string_processed = string_processed

    def filter_expression(self):
        # Remove comments and extra spaces
        self.string_processed = re.sub(r"/\*.*?\*/", "", self.string_processed)
        self.string_processed = self.string_processed.replace(" ", "")
        return self.string_processed

class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

class Tokenizer:
    def __init__(self, source):
        self.source = source
        self.position = 0
        self.actual = None

    def selectNext(self):
        while self.position < len(self.source) and self.source[self.position] == ' ':
            self.position += 1

        if self.position >= len(self.source):
            self.actual = Token("EOF", " ")
            return self.actual

        if self.source[self.position] == "+":
            self.position += 1
            self.actual = Token("PLUS", "+")
        elif self.source[self.position] == "-":
            self.position += 1
            self.actual = Token("MINUS", "-")
        elif self.source[self.position] == "*":
            self.position += 1
            self.actual = Token("MULT", "*")
        elif self.source[self.position] == "/":
            self.position += 1
            self.actual = Token("DIV", "/")
        elif self.source[self.position] == "(":
            self.position += 1
            self.actual = Token("OPENP", "(")
        elif self.source[self.position] == ")":
            self.position += 1
            self.actual = Token("CLOSEP", ")")
        elif self.source[self.position].isnumeric():
            candidato = self.source[self.position]
            self.position += 1
            while self.position < len(self.source) and self.source[self.position].isnumeric():
                candidato += self.source[self.position]
                self.position += 1
            self.actual = Token("NUM", int(candidato))
        else:
            raise Exception("Token inválido")

        return self.actual

class Parser:
    tokenizer = None

    @staticmethod
    def parseFactor():
        result = 0
        if Parser.tokenizer.actual.type == "NUM":
            result = Parser.tokenizer.actual.value
            Parser.tokenizer.selectNext()
        elif Parser.tokenizer.actual.type == "OPENP":
            Parser.tokenizer.selectNext()
            result = Parser.parseExpression()
            if Parser.tokenizer.actual.type != "CLOSEP":
                raise Exception("Sequência inválida")
            Parser.tokenizer.selectNext()
        elif Parser.tokenizer.actual.type == "MINUS":
            Parser.tokenizer.selectNext()
            result = -Parser.parseFactor()
        else:
            raise ValueError("Fator inválido")
        return result

    @staticmethod
    def parseTerm():
        result = Parser.parseFactor()
        while (Parser.tokenizer.actual.type == "MULT" or Parser.tokenizer.actual.type == "DIV") and Parser.tokenizer.actual.type != "EOF":
            if Parser.tokenizer.actual.type == "MULT":
                Parser.tokenizer.selectNext()
                result *= Parser.parseFactor()
            elif Parser.tokenizer.actual.type == "DIV":
                Parser.tokenizer.selectNext()
                divisor = Parser.parseFactor()
                if divisor == 0:
                    raise Exception("Divisão por zero")
                result //= divisor
        return result

    @staticmethod
    def parseExpression():
        result = Parser.parseTerm()
        while (Parser.tokenizer.actual.type == "PLUS" or Parser.tokenizer.actual.type == "MINUS") and Parser.tokenizer.actual.type != "EOF":
            if Parser.tokenizer.actual.type == "PLUS":
                Parser.tokenizer.selectNext()
                result += Parser.parseTerm()
            elif Parser.tokenizer.actual.type == "MINUS":
                Parser.tokenizer.selectNext()
                result -= Parser.parseTerm()
            else:
                raise Exception("Sequência inválida")
        return result

    @staticmethod
    def run(code):
        code = PreProcessing(code).filter_expression()
        Parser.tokenizer = Tokenizer(code)
        result = Parser.parseExpression()
        if Parser.tokenizer.actual.type != "EOF":
            raise Exception("Sequência inválida")
        print(result)

Parser.run(sys.argv[1])
