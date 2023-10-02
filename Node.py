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


class Node():
    def __init__(self, value, children):
        self.value = value
        self.children = children
        
    def Evaluate(self,table : SymbolTable):
        pass

class BinOp(Node):
    def Evaluate(self,table : SymbolTable):
        if self.value == "+":
            return self.children[0].Evaluate(table) + self.children[1].Evaluate(table)
        elif self.value == "-":
            return self.children[0].Evaluate(table) - self.children[1].Evaluate(table)
        if self.value == "*":
            return self.children[0].Evaluate(table) * self.children[1].Evaluate(table)
        elif self.value == "/":
            return self.children[0].Evaluate(table) // self.children[1].Evaluate(table)
        else:
            raise Exception("Erro")

class UnOp(Node):
    def Evaluate(self, table : SymbolTable):
        if self.value=="+":
            return 1*self.children[0].Evaluate(table)
        elif self.value=="-":
            return -1*self.children[0].Evaluate(table)
        else:
            raise Exception("Erro")
        
class IntVal(Node):
    def Evaluate(self,table : SymbolTable):
        return self.value
    
class NoOp(Node):
    def Evaluate(self,table : SymbolTable):
        pass

class Identifier(Node):
    def Evaluate(self,table : SymbolTable):
        return table.getter(self.value)
    
class Assigment(Node):
    def Evaluate(self, table : SymbolTable):
        table.setter(self.children[0].value, self.children[1].Evaluate(table))
        
class Println(Node):
    def Evaluate(self, table : SymbolTable):
        print(self.children[0].Evaluate(table))
        
class Block(Node):
    def Evaluate(self, table: SymbolTable):
        for node in self.children:
            node.Evaluate(table)