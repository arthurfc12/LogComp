class Node():
    def __init__(self, value, children):
        self.value = value
        self.children = children
        
    def Evaluate():
        pass
    
class BinOp(Node):
    def Evaluate(self):
        if self.value == "+":
            return self.children[0].Evaluate() + self.children[1].Evaluate()
        elif self.value == "-":
            return self.children[0].Evaluate() - self.children[1].Evaluate()
        if self.value == "*":
            return self.children[0].Evaluate() * self.children[1].Evaluate()
        elif self.value == "/":
            return self.children[0].Evaluate() // self.children[1].Evaluate()
        else:
            raise Exception("Erro")

class UnOp(Node):
    def Evaluate(self):
        if self.value=="+":
            return 1*self.children[0].Evaluate()
        elif self.value=="-":
            return -1*self.children[0].Evaluate()
        else:
            raise Exception("Erro")
        
class IntVal(Node):
    def Evaluate(self):
        return self.value
    
class NoOp(Node):
    def Evaluate(self):
        pass