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

            if char in ["+", "-", "*", "/", "(", ")", "\n", ">", "<", "!", "{", "}", ";", "."]:
                if size_of_token == 0:
                    self.next = Token(type(char), char)
                    self.position += 1
                    return 0
                else:
                    self.next = Token(type(token.strip()), token.strip())
                    return 0

            elif char == '"':
                if size_of_token == 0:
                    for i in range(self.position+1, len(self.source)):
                        if self.source[i] == '"':
                            end = i
                            break
                    token_str = self.source[self.position:end+1]
                    self.next = Token(type(token_str), token_str)
                    self.position += len(token_str)
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
                
            elif char == "P":
                if size_of_token == 0:
                    token_print = self.source[self.position:self.position+7]
                    if token_print == "Println":
                        self.next = Token(type(token_print), token_print)
                        self.position += len(token_print)
                        return 0
                    else:
                        token += char
                        self.position += 1
                else:
                    self.next = Token(type(token.strip()), token.strip())
                    return 0
        
            elif char == "i":
                if size_of_token == 0:
                    token_if = self.source[self.position:self.position+2]
                    if token_if == "if":
                        self.next = Token(type(token_if), token_if)
                        self.position += len(token_if)
                        return 0
                    token_int = self.source[self.position:self.position+3]
                    if token_int == "int":
                        self.next = Token(type(token_int), token_int)
                        self.position += len(token_int)
                        return 0
                    else:
                        token += char
                        self.position += 1
                else:
                    self.next = Token(type(token.strip()), token.strip())
                    return 0
                
            elif char == "e":
                if size_of_token == 0:
                    token_else = self.source[self.position:self.position+4]
                    if token_else == "else":
                        self.next = Token(type(token_else), token_else)
                        self.position += len(token_else)
                        return 0
                    else:
                        token += char
                        self.position += 1
                else:
                    self.next = Token(type(token.strip()), token.strip())
                    return 0
                
            elif char == "f":
                if size_of_token == 0:
                    token_for = self.source[self.position:self.position+3]
                    if token_for == "for":
                        self.next = Token(type(token_for), token_for)
                        self.position += len(token_for)
                        return 0
                    else:
                        token += char
                        self.position += 1
                else:
                    self.next = Token(type(token.strip()), token.strip())
                    return 0

            elif char == "v":
                if size_of_token == 0:
                    token_var = self.source[self.position:self.position+3]
                    if token_var == "var":
                        self.next = Token(type(token_var), token_var)
                        self.position += len(token_var)
                        return 0
                    else:
                        token += char
                        self.position += 1
                else:
                    self.next = Token(type(token.strip()), token.strip())
                    return 0

            elif char == "s":
                if size_of_token == 0:
                    token_string = self.source[self.position:self.position+6]
                    if token_string == "string":
                        self.next = Token(type(token_string), token_string)
                        self.position += len(token_string)
                        return 0
                    else:
                        token += char
                        self.position += 1
                else:
                    self.next = Token(type(token.strip()), token.strip())
                    return 0
                

            else:
                token += char
                self.position += 1
            
        self.next = Token(type(token.strip()), token.strip())
        return 0


class SymbolTable:
    def __init__(self):
        self.dictionary = {}

    def getter(self, key: str):
        return self.dictionary[key]
    
    def setter(self, key: str, value, type_variable: str):
        if key in self.dictionary:
            if self.dictionary[key][1] == type_variable:
                self.dictionary[key] = (value, type_variable)
            else:
                raise ValueError("Valor diferente do tipo da variável")
        else:
            self.dictionary[key] = (value, type_variable)


