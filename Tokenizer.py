from Token import Token 

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
            self.actual = Token("OPNEP", 0)
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
            raise ValueError("TOKENIZER")
