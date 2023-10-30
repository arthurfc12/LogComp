from Tokenizer import *
from Token import Token

class Node:
    def __init__(self):
        self.value = None
        self.children : list[Node] = []
    
    def evaluate(self, symbol_table: SymbolTable):
        pass 
    
    
class BinOp(Node):
    def __init__(self, value: str, child_left: Node, child_right: Node):
        super().__init__()
        self.value = value
        self.children = [child_left, child_right]

    def evaluate(self, symbol_table: SymbolTable):
        left = self.children[0].evaluate(symbol_table)
        right = self.children[1].evaluate(symbol_table)

        left_value = left[0]
        left_type = left[1]

        right_value = right[0]
        right_type = right[1]

        if self.value == ".":
            return (str(left_value) + str(right_value), "string")

        if left_type != right_type: 
            raise ValueError(f"tipos diferentes na operacao")
        elif self.value == "+":
            return (left_value + right_value, "int")
        elif self.value == "-":
            return (left_value - right_value, "int")
        elif self.value == "*":
            return (left_value * right_value, "int")
        elif self.value == "/":
            return (left_value // right_value, "int")
        elif self.value == "||":
            return (int(left_value | right_value), "int")
        elif self.value == "&&":
            return (int(left_value & right_value), "int")
        elif self.value == "==":
            return (int(left_value == right_value), "int")
        elif self.value == ">":
            return (int(left_value > right_value), "int")
        elif self.value == "<":
            return (int(left_value < right_value), "int")
        
        
class UnOp(Node):
    def __init__(self, value: str, child: Node):
        super().__init__()
        self.value = value
        self.children = [child]

    def evaluate(self, symbol_table: SymbolTable):
        value = self.children[0].evaluate(symbol_table)[0]

        if value >= 0 and self.value == "+":
            return (value, "int")
        elif value >= 0 and self.value == "-":
            return (-abs(value), "int")
        elif value < 0 and self.value == "+":
            return (value, "int")
        elif value < 0 and self.value == "-":
            return (abs(value), "int")
        elif self.value == "!":
            return (int(not value), "int")


class IntVal(Node):
    def __init__(self, value: int):
        super().__init__()
        self.value = value

    def evaluate(self, symbol_table: SymbolTable):
        return (self.value, "int")
    

class StrVal(Node):
    def __init__(self, value: int):
        super().__init__()
        self.value = value

    def evaluate(self, symbol_table: SymbolTable):
        return (self.value, "string")


class NoOp(Node):
    def __init__(self):
        super().__init__()

    def evaluate(self, symbol_table: SymbolTable):
        return (None, None)
    

class Iden(Node):
    def __init__(self, value: str):
        super().__init__()
        self.value = value

    def evaluate(self, symbol_table: SymbolTable):
        return symbol_table.getter(self.value)
    

class Program(Node):
    def __init__(self):
        super().__init__()

    def evaluate(self, symbol_table: SymbolTable):
        for child in self.children:
            child.evaluate(symbol_table)


class Println(Node):
    def __init__(self, child: Node):
        super().__init__()
        self.children = [child]

    def evaluate(self, symbol_table: SymbolTable):
        print(self.children[0].evaluate(symbol_table)[0])

    
class Assingment(Node):
    def __init__(self, child_left: Iden, child_right: Node):
        super().__init__()
        self.children = [child_left, child_right]

    def evaluate(self, symbol_table: SymbolTable):
        iden_value = self.children[1].evaluate(symbol_table)[0]

        if type(iden_value).__name__ == "str": iden_type = "string"
        else: iden_type = "int"

        symbol_table.setter(self.children[0].value, iden_value, iden_type)

    
class If(Node):
    def __init__(self, child_cond: Node, child_true: Node, child_false: Node):
        super().__init__()
        self.children = [child_cond, child_true, child_false]

    def evaluate(self, symbol_table: SymbolTable):
        if self.children[0].evaluate(symbol_table)[0]:
            return self.children[1].evaluate(symbol_table)
        else:
            return self.children[2].evaluate(symbol_table)


class For(Node):
    def __init__(self, child_init: Node, child_cond: Node, child_inc: Node, child_do: Node):
        super().__init__()
        self.children = [child_init, child_cond, child_inc, child_do]

    def evaluate(self, symbol_table: SymbolTable):
        i = self.children[0].evaluate(symbol_table)
        while self.children[1].evaluate(symbol_table)[0]:
            self.children[3].evaluate(symbol_table)
            i = self.children[2].evaluate(symbol_table)


class Input(Node):
    def __init__(self):
        super().__init__()

    def evaluate(self, symbol_table: SymbolTable):
        return (int(input()), "int")
    

class VarDec(Node):
    def __init__(self, value: str, child_left: Node, child_right: Node = NoOp()):
        super().__init__()
        self.value = value
        self.children = [child_left, child_right]

    def evaluate(self, symbol_table: SymbolTable):
        if self.children[0].value in symbol_table.dictionary:
            raise ValueError("tipo diferente da variavel")
        symbol_table.setter(self.children[0].value, self.children[1].evaluate(symbol_table)[0], self.value)