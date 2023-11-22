from Tokenizer import *
from Token import Token

class Node:
    i = 0
    assembly = open("asmheader.asm",mode="r").read()
    end_code = open("asmendcode.asm",mode="r").read()

    def __init__(self, value, children):
        self.value = value
        self.children = children
        self.id = self.newId()

    def Evaluate(self, table: SymbolTable):
        pass
    
    @staticmethod
    def newId():
        Node.i+=1
        return Node.i
    
    @staticmethod
    def add_line(line):
        Node.assembly+=line + "\n"
        
    @staticmethod
    def endcode():
        Node.assembly+=Node.end_code
        return Node.assembly
    
    
class BinOp(Node):
    def Evaluate(self, table: SymbolTable):
        var1 = self.children[1].Evaluate(table)
        Node.add_line("PUSH EAX")
        var2 = self.children[0].Evaluate(table)
        Node.add_line("POP EBX")
        
        if self.value == ".":
            return (str(var1[0])+str(var2[0]),"string")
        
        if var1[1] == var2[1]:
            if self.value == "+":
                Node.add_line("ADD EAX, EBX")
                return (var1[0] + var2[0],"int")
            elif self.value == "-":
                Node.add_line("SUB EAX, EBX")
                return (var1[0] - var2[0],"int")
            if self.value == "*":
                Node.add_line("IMUL EAX, EBX")
                return (var1[0] * var2[0],"int")
            elif self.value == "/":
                Node.add_line("IDIV EAX, EBX")
                return (var1[0] // var2[0],"int")
            elif self.value == "||":
                Node.add_line("OR EAX, EBX")
                return (int(var1[0] | var2[0]),"int")
            elif self.value == "&&":
                Node.add_line("AND EAX, EBX")
                return (int(var1[0] & var2[0]),"int")
            elif self.value == "==":
                Node.add_line("CMP EAX, EBX")
                Node.add_line("CALL binop_je")
                return (int(var1[0] == var2[0]),"int")
            elif self.value == ">":
                Node.add_line("CMP EAX, EBX")
                Node.add_line("CALL binop_jg")
                return (int(var1[0] > var2[0]),"int")
            elif self.value == "<":
                Node.add_line("CMP EAX, EBX")
                Node.add_line("CALL binop_jl")
                return (int(var1[0] < var2[0]),"int")
            else:
                raise Exception("Erro")
        else:
            raise Exception("Erro")

class UnOp(Node):
    def Evaluate(self, table: SymbolTable):
        var = self.children[0].Evaluate(table)
        if (var[1] == "int"):  
            if self.value == "+":
                return (1 * var[0] , var[1])
            elif self.value == "-":
                return (-1 * var[0],var[1])
            elif self.value == "!":
                return (not (var[0]), var[1])
            else:
                raise Exception("Erro")
        else:
            raise Exception("Erro")

class IntVal(Node):
    def Evaluate(self, table: SymbolTable):
        Node.add_line(f"MOV EAX, {self.value}")
        return (self.value,"int")
    
class StrVal(Node):
    def Evaluate(self, table: SymbolTable):
        return (self.value,"string")

class NoOp(Node):
    def Evaluate(self, table: SymbolTable):
        pass

class Identifier(Node):
    def Evaluate(self, table: SymbolTable):
        Node.add_line(f"MOV EAX, [EBP-{table.getter(self.value)[2]*4}]")   
        return table.getter(self.value)    

class Program(Node):
    def __init__(self):
        super().__init__()

    def evaluate(self, symbol_table: SymbolTable):
        for child in self.children:
            child.evaluate(symbol_table)


class Println(Node):
    def Evaluate(self, table: SymbolTable):
        Node.add_line(f"MOV EAX, [EBP-{table.getter(self.children[0].value)[2]*4}]")
        Node.add_line("PUSH EAX")
        Node.add_line("PUSH formatout")
        Node.add_line("CALL printf")
        Node.add_line("ADD ESP, 8")
        
        
class Scanln(Node):
    def Evaluate(self, table: SymbolTable):
        Node.add_line("PUSH scanint")
        Node.add_line("PUSH formatin")
        Node.add_line("call scanf")
        Node.add_line("ADD ESP, 8")
        Node.add_line("MOV EAX, DWORD [scanint]")
        return (0,"int")
    
class IFNode(Node):
    def Evaluate(self, table: SymbolTable):
        unique_id = self.id
        Node.add_line(f"IF_{unique_id}:")
        self.children[0].Evaluate(table)
        Node.add_line("CMP EAX, False")
        Node.add_line(f"JE ELSE_{unique_id}")
        self.children[1].Evaluate(table)
        Node.add_line(f"JMP ENDIF_{unique_id}")
        Node.add_line(f"ELSE_{unique_id}:")
        if len(self.children) > 2:
            self.children[2].Evaluate(table)
        Node.add_line(f"ENDIF_{unique_id}:")

class FORNode(Node):
    def Evaluate(self, table: SymbolTable):
        unique_id = self.id
        self.children[0].Evaluate(table)
        Node.add_line(f"LOOP_{unique_id}:")
        self.children[1].Evaluate(table)[0]
        Node.add_line("CMP EAX, False")
        Node.add_line(f"JE EXIT_{unique_id}")
        self.children[2].Evaluate(table)
        self.children[3].Evaluate(table)
        Node.add_line(f"JMP LOOP_{unique_id}")
        Node.add_line(f"EXIT_{unique_id}:")

class Input(Node):
    def __init__(self):
        super().__init__()

    def evaluate(self, symbol_table: SymbolTable):
        return (int(input()), "int")
    

class VarDec(Node):
    def Evaluate(self, table: SymbolTable):
        table.create(self.children[0],self.value)
        Node.add_line("PUSH DWORD 0")
        if len(self.children)>1:
            table.setter(self.children[0],self.children[1].Evaluate(table))
            Node.add_line(f"MOV [EBP-{table.getter(self.children[0])[2]*4}], EAX")

class Assigment(Node):
    def Evaluate(self, table: SymbolTable):
        right = self.children[1].Evaluate(table)
        Node.add_line(f"MOV [EBP-{table.getter(self.children[0].value)[2]*4}], EAX")
        table.setter(self.children[0].value, right)

class Block(Node):
    def Evaluate(self, table: SymbolTable):
        for node in self.children:
            node.Evaluate(table)
