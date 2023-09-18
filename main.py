import sys
import re


class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value


class PreProcessing:
    @staticmethod
    def filter(code):
        pattern = "[a-zA-Z]"
        text_without_letters = re.sub(pattern, "", code)
        pattern_comments = "/\*.*?\*/"
        text_without_comments = re.sub(pattern_comments, "", text_without_letters)
        return text_without_comments


class Node:
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def Evaluate(self):
        pass


class BinOp(Node):

    def Evaluate(self):
        if(self.value == "+"):
            return self.children[0].Evaluate() + self.children[1].Evaluate()
        elif (self.value == "-"):
            return self.children[0].Evaluate() - self.children[1].Evaluate()
        elif (self.value == "*"):
            return self.children[0].Evaluate() * self.children[1].Evaluate()
        elif (self.value == "/"):
            return self.children[0].Evaluate() // self.children[1].Evaluate()


class UnOp(Node):

    def Evaluate(self):
        if(self.value == "+"):
            return self.children[0].Evaluate()
        elif (self.value == "-"):
            return -self.children[0].Evaluate()


class IntVal(Node):

    def Evaluate(self):
        return self.value


class NoOp(Node):

    def Evaluate(self):
        pass


class Tokenizer:
    def __init__(self, source):
        self.source = source
        self.position = 0
        self.actual = None

    def selectNext(self):
        if(self.position >= len(self.source)):
            self.actual = Token("EOF", 0)
            return self.actual

        while(self.source[self.position] == " "):
            self.position += 1
            if(self.position >= len(self.source)):
                self.actual = Token("EOF", 0)
                return self.actual

        if(self.source[self.position] == '+'):
            self.position += 1
            self.actual = Token("PLUS", 0)
            return self.actual

        elif(self.source[self.position] == '-'):
            self.position += 1
            self.actual = Token("MINUS", 0)
            return self.actual

        elif(self.source[self.position] == '*'):
            self.position += 1
            self.actual = Token("MULT", 0)
            return self.actual

        elif(self.source[self.position] == '/'):
            self.position += 1
            self.actual = Token("DIV", 0)
            return self.actual

        elif(self.source[self.position] == '('):
            self.position += 1
            self.actual = Token("OPENP", 0)
            return self.actual

        elif(self.source[self.position] == ')'):
            self.position += 1
            self.actual = Token("CLOSEP", 0)
            return self.actual

        elif(self.source[self.position].isnumeric()):
            cadidato = self.source[self.position]
            self.position += 1
            if(self.position < len(self.source)):
                while(self.source[self.position].isnumeric()):
                    cadidato += self.source[self.position]
                    self.position += 1
                    if(self.position >= len(self.source)):
                        break
            self.actual = Token("NUM", int(cadidato))
            return self.actual

        else:
            raise ValueError("ERROR")


class Parser:
    tokens = None

    @staticmethod
    def parseFactor():
        if(Parser.tokens.actual.type == "NUM"):
            node = IntVal(Parser.tokens.actual.value,[])
            Parser.tokens.selectNext()

        elif(Parser.tokens.actual.type == "MINUS"):
            Parser.tokens.selectNext()
            node = UnOp('-', [Parser.parseFactor()])

        elif(Parser.tokens.actual.type == "PLUS"):
            Parser.tokens.selectNext()
            node = UnOp('+', [Parser.parseFactor()])

        elif(Parser.tokens.actual.type == "OPENP"):
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