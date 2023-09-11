import sys
import re

class PreProcessing:
    def __init__(self, entire_string):
        self.entire_string = entire_string

    def filter_expression(self):
        self.entire_string = re.sub("/\*.*?\*/", "", self.entire_string)
        return self.entire_string

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

class Parser:
    tokens = None

    @staticmethod
    def parse_factor():
        result = 0

        if Parser.tokens.actual.type == "NUM":
            result = Parser.tokens.actual.value
            Parser.tokens.selectNext()
        elif Parser.tokens.actual.type == "OPENP":
            result = Parser.parse_expression()
            if Parser.tokens.actual.type != "CLOSEP":
                raise ValueError
            Parser.tokens.selectNext()
        elif Parser.tokens.actual.type == "PLUS":
            Parser.tokens.selectNext()
            result += Parser.parse_factor()
        elif Parser.tokens.actual.type == "MINUS":
            Parser.tokens.selectNext()
            result -= Parser.parse_factor()
        else:
            raise ValueError

        return result

    @staticmethod
    def parse_term():
        result = Parser.parse_factor()

        while Parser.tokens.actual.type == "MULT" or Parser.tokens.actual.type == "DIV":
            if Parser.tokens.actual.type == "MULT":
                Parser.tokens.selectNext()
                result *= Parser.parse_factor()
            elif Parser.tokens.actual.type == "DIV":
                Parser.tokens.selectNext()
                result //= Parser.parse_factor()

        return result

    @staticmethod
    def parse_expression():
        Parser.tokens.selectNext()
        result = Parser.parse_term()

        while (Parser.tokens.actual.type == "PLUS" or Parser.tokens.actual.type == "MINUS") and Parser.tokens.actual.type != "EOF":
            if Parser.tokens.actual.type == "PLUS":
                Parser.tokens.selectNext()
                result += Parser.parse_term()
            elif Parser.tokens.actual.type == "MINUS":
                Parser.tokens.selectNext()
                result -= Parser.parse_term()
            else:
                raise ValueError

        return result

    @staticmethod
    def run(code):
        code_filter = PreProcessing(code).filter_expression()
        Parser.tokens = Tokenizer(code_filter)
        result = Parser.parse_expression()
        if Parser.tokens.actual.type != "EOF":
            raise ValueError
        print(result)

if __name__ == "__main__":
    Parser.run(sys.argv[1])
