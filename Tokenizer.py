from Token import Token
import re

class Tokenizer:
    def __init__(self, source: str, position: int):
        self.source = source
        self.position = position
        self.next = Token(type(source), source)
    
    def select_next(self):
        if self.position == len(self.source):
            self.next = Token(type("EOF"), "EOF")
            return 0
        
        token = ""
        while self.position < len(self.source):
            char = self.source[self.position]
            size_of_token = len(token.strip())

            if char in ["+", "-", "*", "/", "(", ")", "\n", ">", "<", "!", "{", "}", ";"]:
                if size_of_token == 0:
                    self.next = Token(type(char), char)
                    self.position += 1
                    return 0
                else:
                    self.next = Token(type(token.strip()), token.strip())
                    return 0
                
            elif char == "=":
                if size_of_token == 0:
                    token_equal = self.source[self.position:self.position+2]
                    if token_equal == "==":
                        self.next = Token(type(token_equal), token_equal)
                        self.position += len(token_equal)
                        return 0
                    else:
                        self.next = Token(type(char), char)
                        self.position += 1
                        return 0
                else:
                    self.next = Token(type(token.strip()), token.strip())
                    return 0
                
            elif char in ["|", "&"]:
                if size_of_token == 0:
                    token_or = self.source[self.position:self.position+2]
                    if token_or in ["||", "&&"]:
                        self.next = Token(type(token_or), token_or)
                        self.position += len(token_or)
                        return 0
                    else:
                        token += char
                        self.position += 1
                else:
                    self.next = Token(type(token.strip()), token.strip())
                    return 0
        
            elif char == "i":
                token_if = self.source[self.position:self.position+2]
                if token_if == "if":
                    self.next = Token(type(token_if), token_if)
                    self.position += len(token_if)
                    return 0
                else:
                    token += char
                    self.position += 1
                
            elif char == "f":
                token_for = self.source[self.position:self.position+3]
                if token_for == "for":
                    self.next = Token(type(token_for), token_for)
                    self.position += len(token_for)
                    return 0
                else:
                    token += char
                    self.position += 1
                
            else:
                token += char
                self.position += 1
            
        self.next = Token(type(token.strip()), token.strip()) 
        return 0


class SymbolTable:
    def __init__(self):
        self.table = dict()
        
    def getter(self,identifier):
        try:
            return self.table[identifier]
        except:
            raise Exception(f"{identifier} variable doesn't exist")
    
    def setter(self,identifier,value):
        self.table[identifier] = value