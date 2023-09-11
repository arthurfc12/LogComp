import sys
import re

class PreProcessing:
    def __init__(self, string_processed):
        self.string_processed = string_processed

    def filter_expression(self):
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
    def __init__(self, code):
        self.code = code
        self.tokenizer = Tokenizer(self.code)

    def parseFactor(self):
        result = 0
        if self.tokenizer.actual.type == "NUM":
            result = self.tokenizer.actual.value
            self.tokenizer.selectNext()
        elif self.tokenizer.actual.type == "OPENP":
            self.tokenizer.selectNext()
            result = self.parseExpression()
            if self.tokenizer.actual.type != "CLOSEP":
                raise Exception("Sequência inválida")
            self.tokenizer.selectNext()
        elif self.tokenizer.actual.type == "MINUS":
            self.tokenizer.selectNext()
            result = -self.parseFactor()
        else:
            raise ValueError("Fator inválido")
        return result

    def parseTerm(self):
        result = self.parseFactor()
        while (self.tokenizer.actual.type == "MULT" or self.tokenizer.actual.type == "DIV") and self.tokenizer.actual.type != "EOF":
            if self.tokenizer.actual.type == "MULT":
                self.tokenizer.selectNext()
                result *= self.parseFactor()
            elif self.tokenizer.actual.type == "DIV":
                self.tokenizer.selectNext()
                divisor = self.parseFactor()
                if divisor == 0:
                    raise Exception("Divisão por zero")
                result //= divisor
        return result

    def parseExpression(self):
        result = self.parseTerm()
        while (self.tokenizer.actual.type == "PLUS" or self.tokenizer.actual.type == "MINUS") and self.tokenizer.actual.type != "EOF":
            if self.tokenizer.actual.type == "PLUS":
                self.tokenizer.selectNext()
                result += self.parseTerm()
            elif self.tokenizer.actual.type == "MINUS":
                self.tokenizer.selectNext()
                result -= self.parseTerm()
            else:
                raise Exception("Sequência inválida")
        return result

    def run(self):
        result = self.parseExpression()
        if self.tokenizer.actual.type != "EOF":
            raise Exception("Sequência inválida")
        print(result)

if __name__ == "__main__":
    code = sys.argv[1]
    code = PreProcessing(code).filter_expression()
    parser = Parser(code)
    parser.run()
