import sys
import re
import string

class PreProcessing:
    def __init__(self, string_processed):
        self.string_processed = string_processed
  
    def filter_expression(self):
        self.string_processed = re.sub("/\*.*?\*/", "", self.string_processed)
        return self.string_processed


class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

class Tokenizer:
    def __init__(self, source):
        #source_process = source.replace(" ","")
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
    
        elif self.source[self.position] == "+":
            self.position += 1
            self.actual = Token("PLUS", " ")
            return self.actual
    
        elif self.source[self.position] == "-":
            self.position += 1
            self.actual = Token("MINUS", " ")
            return self.actual
        
        elif self.source[self.position] == "*":
            self.position += 1
            self.actual = Token("MULT", "*")
            return self.actual
      
        elif self.source[self.position] == "/":
            self.position += 1
            self.actual = Token("DIV", "/")
            return self.actual
        
        elif self.source[self.position] == "(":
            self.position += 1
            self.actual = Token("OPENP", "(")
            return self.actual
        
        elif self.source[self.position] == ")":
            self.position += 1
            self.actual = Token("CLOSEP", ")")
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
            raise Exception("Token invalido")



class Parser:
    tokenizer = None

    @staticmethod
    def parseFactor():
        result = 0
        if Parser.tokenizer.actual.type == "NUM":
            result = Parser.tokenizer.actual.value
            Parser.tokenizer.selectNext()
        
        elif Parser.tokenizer.actual.type == "OPENP":
            result = Parser.parseExpression()
            if Parser.tokenizer.actual.type != "CLOSEP":
                raise Exception("sequencia invalida")
            Parser.tokenizer.selectNext()
        
        elif Parser.tokenizer.actual.type == "PLUS":
            Parser.tokenizer.selectNext()
            result += Parser.parseFactor()
      
        elif Parser.tokenizer.actual.type == "MINUS":
            Parser.tokenizer.selectNext()
            result -= Parser.parseFactor()
    
        else:
            raise ValueError
      
        return result


    @staticmethod
    def parseTerm():
        result = Parser.parseFactor()
        while((Parser.tokenizer.actual.type == "MULT" or Parser.tokenizer.actual.type == "DIV") and Parser.tokenizer.actual.type != "EOF"):
            
            if(Parser.tokenizer.actual.type == "MULT"): #metodo para mult
                Parser.tokenizer.selectNext()
                if(Parser.tokenizer.actual.type == "NUM"):
                    result *=Parser.tokenizer.actual.value
                else:
                    raise Exception("sequencia invalida (multiplicacao)")
            
            elif(Parser.tokenizer.actual.type == "DIV"): #metodo para div
                Parser.tokenizer.selectNext()
                if(Parser.tokenizer.actual.type == "NUM"):
                    result //= Parser.tokenizer.actual.value
                else:
                    raise Exception("sequencia invalida (divisao)")
                    #pass
        
        return result
    
    def parseExpression():
        Parser.tokenizer.selectNext()
        result = Parser.parseTerm()
        while(Parser.tokenizer.actual.type == "PLUS" or Parser.tokenizer.actual.type == "MINUS") and Parser.tokenizer.actual.type != "EOF":
            if(Parser.tokenizer.actual.type == "PLUS"):
                Parser.tokenizer.selectNext()
                result+=Parser.parseTerm()
            elif(Parser.tokenizer.actual.type == "MINUS"):
                Parser.tokenizer.selectNext()
                result-=Parser.parseTerm()
            else:
                raise Exception("sequencia invalida")
        if(Parser.tokenizer.actual.type != "EOF"):
            raise Exception("sequencia invalida")
        return result

    
    @staticmethod
    def run(code):
        code = PreProcessing(code).filter_expression()
        Parser.tokenizer = Tokenizer(code)
        result = Parser.parseExpression()
        if Parser.tokenizer.actual.type != "EOF":
            raise Exception("sequencia invalida")
        return result
        #pass

if __name__ == "__main__":
    print(Parser.run(sys.argv[1]))    