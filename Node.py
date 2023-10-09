from Tokenizer import *

class Node:
    def __init__(self):
        self.value = None
        self.children : list[Node] = []
    
    def Evaluate(self, symbol_table: SymbolTable):
        pass 
    
    
class BinOp(Node):
    def __init__(self, value: str, child_left: Node, child_right: Node):
        super().__init__()
        self.value = value
        self.children = [child_left, child_right]

    def Evaluate(self, symbol_table: SymbolTable):
        left_value = self.children[0].Evaluate(symbol_table)
        right_value = self.children[1].Evaluate(symbol_table)

        if self.value == "+":
            return left_value + right_value
        elif self.value == "-":
            return left_value - right_value
        elif self.value == "*":
            return left_value * right_value
        elif self.value == "/":
            return left_value // right_value
        elif self.value == "||":
            return left_value | right_value
        elif self.value == "&&":
            return left_value & right_value
        elif self.value == "==":
            return left_value == right_value
        elif self.value == ">":
            return left_value > right_value
        elif self.value == "<":
            return left_value < right_value
        else:
            raise Exception("Erro")
                
        
class UnOp(Node):
    def __init__(self, value: str, child: Node):
        super().__init__()
        self.value = value
        self.children = [child]

    def Evaluate(self, symbol_table: SymbolTable):
        value = self.children[0].Evaluate(symbol_table)

        if value >= 0 and self.value == "+":
            return value
        elif value >= 0 and self.value == "-":
            return -abs(value)
        elif value < 0 and self.value == "+":
            return value
        elif value < 0 and self.value == "-":
            return abs(value)
        elif self.value == "!":
            return not value
        else:
            raise Exception("Erro")



class IntVal(Node):
    def __init__(self, value: int):
        super().__init__()
        self.value = value

    def Evaluate(self, symbol_table: SymbolTable):
        return self.value


class NoOp(Node):
    def __init__(self):
        super().__init__()

    def Evaluate(self, symbol_table: SymbolTable):
        return None
    

class Identifier(Node):
    def __init__(self, value: str):
        super().__init__()
        self.value = value

    def Evaluate(self, symbol_table: SymbolTable):
        return symbol_table.getter(self.value)
    

class Program(Node):
    def __init__(self):
        super().__init__()

    def Evaluate(self, symbol_table: SymbolTable):
        for child in self.children:
            child.Evaluate(symbol_table)


class Println(Node):
    def __init__(self, child: Node):
        super().__init__()
        self.children = [child]

    def Evaluate(self, symbol_table: SymbolTable):
        print(self.children[0].Evaluate(symbol_table))

    
class Assingment(Node):
    def __init__(self, child_left: Identifier, child_right: Node):
        super().__init__()
        self.children = [child_left, child_right]

    def Evaluate(self, symbol_table: SymbolTable):
        symbol_table.setter(self.children[0].value, self.children[1].Evaluate(symbol_table))

    
class If(Node):
    def __init__(self, child_conditional: Node, child_true: Node, child_false: Node):
        super().__init__()
        self.children = [child_conditional, child_true, child_false]

    def Evaluate(self, symbol_table: SymbolTable):
        if self.children[0].Evaluate(symbol_table):
            return self.children[1].Evaluate(symbol_table)
        else:
            return self.children[2].Evaluate(symbol_table)


class For(Node):
    def __init__(self, child_init: Node, child_conditional: Node, child_increment: Node, child_do: Node):
        super().__init__()
        self.children = [child_init, child_conditional, child_increment, child_do]

    def Evaluate(self, symbol_table: SymbolTable):
        i = self.children[0].Evaluate(symbol_table)
        while self.children[1].Evaluate(symbol_table):
            self.children[3].Evaluate(symbol_table)
            i = self.children[2].Evaluate(symbol_table)


class Input(Node):
    def __init__(self):
        super().__init__()

    def Evaluate(self, symbol_table: SymbolTable):
        return int(input())