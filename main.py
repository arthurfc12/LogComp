import sys
import re
import string
from Node import *
from Token import Token
from Tokenizer import *


with open(sys.argv[1], 'r') as f:
    input = f.read()

class PreProcessing:
    def filter(string):
        return re.sub(r'//.*', '', string).strip()
    
class Parser:
    def __init__(self, code: str):
        self.tokenizer = Tokenizer(code, 0)
        self.signals = ["+", "-", "/", "*", "(", ")", "=", "\n", "|", "&", "=", "Println", ">", "<", "!", "if", "{", "}", "for", ";", "Scanln"]

    def program(self):
        program = Program()
        while self.tokenizer.position != len(self.tokenizer.source):
            child = self.statement()
            if self.tokenizer.next.value == "\n":
                self.tokenizer.select_next()
            program.children.append(child)
        return program

    def statement(self):   
        if self.tokenizer.next.value == "Println":
            self.tokenizer.select_next()
            if self.tokenizer.next.value != "(":
                raise ValueError(f"stetement\nLast token: {self.tokenizer.next.value}")
            return Println(self.bool_expr())
        
        elif self.tokenizer.next.value == "if":
            self.tokenizer.select_next() 
            condition = self.bool_expr()
            if self.tokenizer.next.value != "{":
                raise ValueError(f"statement\nLast token: {self.tokenizer.next.value}")
            if_true = self.block()
            if self.tokenizer.next.value == "else":
                self.tokenizer.select_next()
                if self.tokenizer.next.value != "{":
                    raise ValueError(f"statement\nLast token: {self.tokenizer.next.value}")
                if_false = self.block()
            elif (self.tokenizer.next.value == "\n") | (self.tokenizer.next.value == "EOF"):
                self.tokenizer.select_next()
                if_false = NoOp()
            else:
                raise ValueError(f"statement\nLast token: {self.tokenizer.next.value}")
            return If(condition, if_true, if_false)
        
        elif self.tokenizer.next.value == "for":
            self.tokenizer.select_next() 
            init = self.assign()
            self.tokenizer.select_next() 
            cond = self.bool_expr()
            self.tokenizer.select_next() 
            inc = self.assign()
            do = self.block()
            return For(init, cond, inc, do)
        
        elif self.tokenizer.next.value not in self.signals:
            return self.assign()
        
        elif self.tokenizer.next.value == "{":
            raise ValueError(f"Statement\nLast token: {self.tokenizer.next.value}")
        
        else:
            return NoOp()
        
    def block(self):
        self.tokenizer.select_next()
        self.tokenizer.select_next()
        while self.tokenizer.next.value != "}":
            tree = self.statement()
            self.tokenizer.select_next()
        self.tokenizer.select_next()
        return tree

    def assign(self):
        if self.tokenizer.next.value[0].isdigit():
            raise ValueError(f"Assign\nLast token: {self.tokenizer.next.value}")
        left_value = Identifier(self.tokenizer.next.value)
        self.tokenizer.select_next()
        if self.tokenizer.next.value != "=":
            raise ValueError(f"Assign\nLast token: {self.tokenizer.next.value}")
        self.tokenizer.select_next()
        return Assingment(left_value, self.bool_expr())

    def bool_expr(self):
        tree = self.bool_term()
        while self.tokenizer.next.value in ["||"]:
            signal = self.tokenizer.next.value
            self.tokenizer.select_next()
            tree = BinOp(signal, tree, self.bool_term())
        return tree

    def bool_term(self):
        tree = self.rel_expr()
        while self.tokenizer.next.value in ["&&"]:
            signal = self.tokenizer.next.value
            self.tokenizer.select_next()
            tree = BinOp(signal, tree, self.rel_expr())
        return tree
    
    def rel_expr(self):
        tree = self.parse_expression()
        while self.tokenizer.next.value in ["==", ">", "<"]:
            signal = self.tokenizer.next.value
            self.tokenizer.select_next()
            tree = BinOp(signal, tree, self.parse_expression())
        return tree
        
    def parse_expression(self):
        tree = self.parse_term()
        while self.tokenizer.next.value in ["+", "-"]:
            signal = self.tokenizer.next.value
            self.tokenizer.select_next()
            tree = BinOp(signal, tree, self.parse_term())
        return tree

    def parse_term(self):
        tree = self.parse_factor()
        while self.tokenizer.next.value in ["/", "*"]:
            signal = self.tokenizer.next.value
            self.tokenizer.select_next()
            tree = BinOp(signal, tree, self.parse_factor())
        return tree
    
    def parse_factor(self):
        if self.tokenizer.next.value.isdigit():
            number = int(self.tokenizer.next.value)
            self.tokenizer.select_next()
            return IntVal(number)
        
        elif self.tokenizer.next.value not in self.signals:
            value = self.tokenizer.next.value
            self.tokenizer.select_next()
            return Identifier(value)
        
        elif self.tokenizer.next.value in ["+", "-", "!"]:
            signal = self.tokenizer.next.value
            self.tokenizer.select_next()
            return UnOp(signal, self.parse_factor())
            
        elif self.tokenizer.next.value in ["(", ")"]:
            if self.tokenizer.next.value == "(":
                self.tokenizer.select_next()
                tree = self.bool_expr()
                if self.tokenizer.next.value == ")":
                    self.tokenizer.select_next()
                    return tree
                raise ValueError(f"Parse factor!\nLast token: {self.tokenizer.next.value}")
        
        elif self.tokenizer.next.value == "Scanln":
            self.tokenizer.select_next()
            self.tokenizer.select_next()
            self.tokenizer.select_next()
            return Input()
            
    def run(self):
        self.tokenizer.select_next()
        program = self.program()
        if self.tokenizer.next.value == "EOF":
            return program
        raise ValueError(f"Run!\nLast token: {self.tokenizer.next.value}")

def main():
    input_without_comments = PreProcessing.filter(input)
    symbol_table = SymbolTable()
    root = Parser(input_without_comments).run().Evaluate(symbol_table)
    root.Print()

if __name__ == "__main__":
    main()
