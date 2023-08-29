import sys
import re
import string

class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

class Tokenizer:
    def __init__(self, source):
        #source_process = source.replace(" ","")
        self.source = source
        self.position = 0
        self.actual = Token(None,None)

    def selectNext(self):
        n = 0
        while(len(self.source)>self.position):
            if(self.source[self.position].isnumeric()):
                n = self.source[self.position]
                self.position+=1
                while(self.position != len(self.source)):
                    if(self.source[self.position].isnumeric()):
                        n += self.source[self.position]
                        self.position+=1
                    else:
                        self.actual = Token("NUM", int(n))
                        return
                self.actual = Token("NUM", int(n))
                return
            elif(self.source[self.position] == "+" and self.actual.type != "PLUS"):
                self.actual = Token("PLUS", 0)
                self.position+=1
                return
            elif(self.source[self.position] == "-" and self.actual.type != "MINUS"):
                self.actual = Token("MINUS", 0)
                self.position+=1
                return
            elif(self.source[self.position] == "*" and self.actual.type != "MULT"):
                self.actual = Token("MULT", 0)
                self.position+=1
                return
            elif(self.source[self.position] == "/" and self.actual.type != "DIV"):
                self.actual = Token("DIV", 0)
                self.position+=1
                return
            elif(self.source[self.position] == " "):
                self.position+=1
                continue
            
            else:
                raise Exception("caracter invalido")
        self.actual = Token("EOF", 0)
        return
        #pass:

class Parser:
    tokenizer = None

    @staticmethod
    def parseTerm():
        Parser.tokenizer.selectNext()
        if(Parser.tokenizer.actual.type == "NUM"): #checa se eh numerico
            result = Parser.tokenizer.actual.value
            Parser.tokenizer.selectNext()
            if(Parser.tokenizer.actual.type == "MULT" or Parser.tokenizer.actual.type == "DIV"):
                while(Parser.tokenizer.actual.type == "MULT" or Parser.tokenizer.actual.type == "DIV"):
                    if(Parser.tokenizer.actual.type == "MULT"): #metodo para mult
                        Parser.tokenizer.selectNext()
                        if(Parser.tokenizer.actual.type == "NUM"):
                            result *=Parser.tokenizer.actual.value
                        else:
                            raise Exception("sequencia invalida (multiplicacao)")
                    if(Parser.tokenizer.actual.type == "DIV"): #metodo para div
                        Parser.tokenizer.selectNext()
                        if(Parser.tokenizer.actual.type == "NUM"):
                            result /= Parser.tokenizer.actual.value
                        else:
                            raise Exception("sequencia invalida (divisao)")
                        #pass
                    Parser.tokenizer.selectNext() # vai pro prox digito
                return result
            else:
                return result
        else:
            raise Exception("sequencia invalida")
    
    def parseExpression():
        result = 0
        result += Parser.parseTerm()
        while (Parser.tokenizer.actual.type == "PLUS" or Parser.tokenizer.actual.type == "MINUS") and Parser.tokenizer.actual.type != "EOF":      
            if(Parser.tokenizer.actual.type == "PLUS" or Parser.tokenizer.actual.type == "MINUS"):
                if(Parser.tokenizer.actual.type == "PLUS"):
                    result+=Parser.parseTerm()
                elif(Parser.tokenizer.actual.type == "MINUS"):
                    result-=Parser.parseTerm()
                elif(Parser.tokenizer.actual.type == "NUM"):
                    raise Exception("sequencia invalida")
            else:
                return int(result)

    
    def code_cleanup(code):
        return(re.sub('/[*](.*?)[*]/',"", code))

    @staticmethod
    def run(code):
        Parser.tokenizer = Tokenizer(Parser.code_cleanup(code))
        return(Parser.parseExpression())
        #pass

if __name__ == "__main__":
    print(Parser.run(sys.argv[1]))    