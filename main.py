#import sys
#import string

class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

class Tokenizer:
    def __init__(self, source):
        source_process = source.replace(" ","")
        self.source = source_process
        self.position = 0
        self.actual = Token(None,None)

    def selectNext(self):
        n = 0
        while(len(self.source)!=self.position):
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
            elif(self.source[self.position] == "+"):
                self.actual = Token("PLUS", 0)
                self.position+=1
                return
            elif(self.source[self.position] == "-"):
                self.actual = Token("MINUS", 0)
                self.position+=1
                return
            elif(self.position == self.source):
                self.actual = Token("EOF", 0)
                continue
            
            else:
                raise Exception("caracter invalido")

        #pass:

class Parser:
    tokenizer = None

    @staticmethod
    def parseExpression():
        Parser.tokenizer.selectNext()
        if(Parser.tokenizer.actual.type == "NUM"): #checa se eh numerico
            result = Parser.tokenizer.actual.value
            Parser.tokenizer.selectNext()
            if(Parser.tokenizer.actual.type == "PLUS" or Parser.tokenizer.actual.type == "MINUS"):
                while(Parser.tokenizer.actual.type == "PLUS" or Parser.tokenizer.actual.type == "MINUS"):
                    if(Parser.tokenizer.actual.type == "PLUS"): #metodo para adicao
                        Parser.tokenizer.selectNext()
                        if(Parser.tokenizer.actual.type == "NUM"):
                            result +=Parser.tokenizer.actual.value
                        else:
                            raise Exception("sequencia invalida (adicao)")
                    elif(Parser.tokenizer.actual.type == "MINUS"): #metodo para subtracao
                        Parser.tokenizer.selectNext()
                        if(Parser.tokenizer.actual.type == "NUM"):
                            result -= Parser.tokenizer.actual.value
                        else:
                            raise Exception("sequencia invalida (subtracao)")
                        #pass
                    Parser.tokenizer.selectNext() # vai pro prox digito
            else:
                raise Exception("sequencia invalida")
            return result
        else:
            raise Exception("sequencia invalida")
    @staticmethod
    def run(code):
        Parser.tokenizer = Tokenizer(code)
        return(Parser.parseExpression())
        #pass

#if __name__ == "__main__":
#    print(Parser.run(sys.argv[1]))    