class Node():
    def __init__(self, value, children):
        self.value = value
        self.children = children
    
    def evaluate(self):
        pass

class BinOp(Node):
    def evaluate(self):
        if self.value == "+":
            return self.children[0].evaluate() + self.children[1].evaluate()
        elif self.value == "-":
            return self.children[0].evaluate() - self.children[1].evaluate()
        elif self.value == "*":
            return self.children[0].evaluate() * self.children[1].evaluate()
        elif self.value == "/":
            return self.children[0].evaluate() // self.children[1].evaluate()
        else:
            raise Exception("BinOp")

class UnOp(Node):
    def evaluate(self):
        if self.value == "+":
            return self.children[0].evaluate()
        elif self.value == "-":
            return -self.children[0].evaluate()
        else:
            raise Exception("UnOp")
        
class IntVal(Node):
    def evaluate(self):
        return self.value
    
class NoOp(Node):
    def evaluate(self):
        pass