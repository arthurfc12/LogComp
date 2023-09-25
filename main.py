import sys
import re

class Token:
    def __init__(self, type : str, value : int):
        self.type = type
        self.value = value

class PreProcessing:
    def __init__(self, pre_string):
        self.pre_string = pre_string
          
    def filter(self):
        self.pre_string = re.sub('//.*', "", self.pre_string)
        return self.pre_string.strip()
        
class Node:
    def __init__(self, value, children):
        self.value = value
        self.children = children
        
    def Evaluate():
        pass

class BinOp(Node):
    def Evaluate(self):
        if self.value == "+":
            return self.children[0].Evaluate() + self.children[1].Evaluate()
        elif self.value == "-":
            return self.children[0].Evaluate() - self.children[1].Evaluate()
        elif self.value == "*":
            return self.children[0].Evaluate() * self.children[1].Evaluate()
        elif self.value == "/":
            return self.children[0].Evaluate() // self.children[1].Evaluate()
        
        else: 
            raise ValueError("BinOP")
        
class UnOp(Node):
    def Evaluate(self):
        if self.value == "+":
            return self.children[0].Evaluate()
        elif self.value == "-":
            return -self.children[0].Evaluate()
        else: 
            raise ValueError("UnOP")
        
class IntVal(Node):
    def Evaluate(self):
        return self.value

class NoOp(Node):
    def Evaluate(self):
        pass
    
class Tokenizer:
    def __init__(self, source: str):
        self.source = source
        self.position = 0
        self.actual = None

    def selectNext(self):
        if self.position >= len(self.source):
            self.actual = Token("EOF", " ")
            return self.actual

        elif self.source[self.position].isnumeric():
            num = self.source[self.position]
            self.position += 1

            while self.position < len(self.source):
                if self.source[self.position].isnumeric():
                    num += self.source[self.position]
                    self.position += 1
                else: 
                    self.actual = Token("NUM", int(num))
                    return self.actual
            self.actual = Token("NUM", int(num))
            return self.actual

        elif self.source[self.position] == "+":
            self.position += 1
            self.actual = Token("PLUS", " ")
            return self.actual

        elif self.source[self.position] == "-" :
            self.position += 1
            self.actual = Token("MINUS", " ")
            return self.actual
        
        elif self.source[self.position] == "/":
            self.position += 1
            self.actual = Token("DIV", "/")
            return self.actual
        
        elif self.source[self.position] == "*":
            self.position += 1
            self.actual = Token("MULT", "*")
            return self.actual
        

        elif self.source[self.position] == " ":
            self.position += 1
            self.selectNext()

        elif self.source[self.position] == "(":
            self.position += 1
            self.actual = Token("OPENP", " ")
            return self.actual

        elif self.source[self.position] == ")":
            self.position += 1
            self.actual = Token("CLOSEP", " ")
            return self.actual
    
        
        else:
            raise Exception("caracter invalido")



class Parser:
    tokens: None

    def parseFactor():
       
       if Parser.tokens.next.type == "NUM":
           node = IntVal(Parser.tokens.next.value, [])
           Parser.tokens.selectNext()


       elif Parser.tokens.next.type == "PLUS":
           Parser.tokens.selectNext()
           node = UnOp("+", [Parser.parseFactor()])


       elif Parser.tokens.next.type == "MINUS":
           Parser.tokens.selectNext()
           node = UnOp("-" , [Parser.parseFactor()])
      
       elif Parser.tokens.next.type == "OPENP":
            node = Parser.parseExpression()
            if Parser.tokens.next.type != "CLOSEP":
               raise ValueError("string invalida")

            else:
                Parser.tokens.selectNext()
       else:
           raise ValueError("string invalida")
      
       return node
    

    def parserTerm():

        node = Parser.parseFactor()

        while (Parser.tokens.next.type == "MULT" or Parser.tokens.next.type == "DIV") :

            if Parser.tokens.next.type == "DIV":
                Parser.tokens.selectNext()
                node = BinOp("/", [node, Parser.parseFactor()])

            elif Parser.tokens.next.type == "MULT":
                Parser.tokens.selectNext()
                node = BinOp("*", [node, Parser.parseFactor()])

        return node
                
    

        
    def parseExpression():
        
        Parser.tokens.selectNext()
        node = Parser.parserTerm()

        while Parser.tokens.next.type != "EOF" and ((Parser.tokens.next.type == "PLUS" or Parser.tokens.next.type == "MINUS")) :

            if Parser.tokens.next.type == "PLUS":
                Parser.tokens.selectNext()
                node = BinOp("+", [node, Parser.parserTerm()])


            elif Parser.tokens.next.type == "MINUS":
                Parser.tokens.selectNext()
                node = BinOp("-", [node, Parser.parserTerm()])
                
            else: 
                raise ValueError
        return node
        


    def run(file):
        filestring = open(file, "r")
        code = filestring.read()
        filestring.close()
        processed_file = PreProcessing(code).filter()
        Parser.tokens = Tokenizer(processed_file)  
        node = Parser.parseExpression()
        
        if Parser.tokens.next.type != "EOF":
            raise Exception("string invalida")
        print(node.Evaluate())


Parser.run(sys.argv[1])