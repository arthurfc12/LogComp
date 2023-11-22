from Tokenizer import *
from Token import Token

class SymbolTable:
    def __init__(self):
        self.table = dict()

    def getter(self, identifier):
        try:
            return self.table[identifier]
        except:
            raise Exception(f"{identifier} variavel nn existe")
        
    def create(self, identifier, type):
        if identifier in self.table.keys():
            raise Exception("variavel ja exidte")
        else:
            self.table[identifier] = (None,type)
    
    def setter(self, identifier, value):
        if identifier not in self.table.keys():
            raise Exception("variavel nn declarada")
        else:
            if (type(value[0]) == FuncDec):
                self.table[identifier] = value 
            elif (self.table[identifier][1] == value[1]):
                self.table[identifier] = value                
            else:
                raise Exception("tipagem diferentes")



class Node:
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def Evaluate(self, table: SymbolTable):
        pass


class BinOp(Node):
    def Evaluate(self, table: SymbolTable, funcTable: SymbolTable):
        var1 = self.children[0].Evaluate(table,funcTable)
        var2 = self.children[1].Evaluate(table,funcTable)
        
        if self.value == ".":
            return (str(var1[0])+str(var2[0]),"string")
        
        if var1[1] == var2[1]:
            if self.value == "+":
                return (var1[0] + var2[0],"int")
            elif self.value == "-":
                return (var1[0] - var2[0],"int")
            if self.value == "*":
                return (var1[0] * var2[0],"int")
            elif self.value == "/":
                return (var1[0] // var2[0],"int")
            elif self.value == "||":
                return (int(var1[0] | var2[0]),"int")
            elif self.value == "&&":
                return (int(var1[0] & var2[0]),"int")
            elif self.value == "==":
                return (int(var1[0] == var2[0]),"int")
            elif self.value == ">":
                return (int(var1[0] > var2[0]),"int")
            elif self.value == "<":
                return (int(var1[0] < var2[0]),"int")
            else:
                raise Exception("Erro")
        else:
            raise Exception("Erro")

class UnOp(Node):
    def Evaluate(self, table: SymbolTable, funcTable: SymbolTable):
        var = self.children[0].Evaluate(table,funcTable)
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
    def Evaluate(self, table: SymbolTable, funcTable: SymbolTable):
        return (self.value,"int")
    
class NoOp(Node):
    def Evaluate(self, table: SymbolTable, funcTable: SymbolTable):
        pass
    
class StrVal(Node):
    def Evaluate(self, table: SymbolTable, funcTable: SymbolTable):
        return (self.value,"string")

class Identifier(Node):
    def Evaluate(self, table: SymbolTable, funcTable: SymbolTable):
        return table.getter(self.value)

class VarDec(Node):
    def Evaluate(self, table: SymbolTable, funcTable: SymbolTable):
        table.create(self.children[0],self.value)
        if len(self.children)>1:
            a =self.children[1].Evaluate(table,funcTable)
            table.setter(self.children[0],a)

class Assigment(Node):
    def Evaluate(self, table: SymbolTable, funcTable: SymbolTable):
        table.setter(self.children[0].value, self.children[1].Evaluate(table,funcTable))

class Println(Node):
    def Evaluate(self, table: SymbolTable, funcTable: SymbolTable):
        print(self.children[0].Evaluate(table,funcTable)[0])
        
class Scanln(Node):
    def Evaluate(self, table: SymbolTable, funcTable: SymbolTable):
        return (int(input()),"int")

class Block(Node):
    def Evaluate(self, table: SymbolTable, funcTable: SymbolTable):
        for node in self.children:
            if type(node) == ReturnNode:
                guarda = node.Evaluate(table,funcTable)
                return guarda
            node.Evaluate(table,funcTable)
            
class IFNode(Node):
    def Evaluate(self, table: SymbolTable, funcTable: SymbolTable):
        if self.children[0].Evaluate(table,funcTable)[0]:
            self.children[1].Evaluate(table,funcTable)
        elif len(self.children) > 2:
            self.children[2].Evaluate(table,funcTable)

class FORNode(Node):
    def Evaluate(self, table: SymbolTable, funcTable: SymbolTable):
        self.children[0].Evaluate(table,funcTable)
        while self.children[1].Evaluate(table,funcTable)[0]:            
            self.children[2].Evaluate(table,funcTable)
            self.children[3].Evaluate(table,funcTable)
            
class FuncDec(Node):
    def Evaluate(self, table: SymbolTable, funcTable: SymbolTable):
        table.create(self.value[0],self.value[1])
        funcTable.create(self.value[0],self.value[1])
        funcTable.setter(self.value[0],(self,self.value[1]))
    
class FuncCall(Node):
    def Evaluate(self, table: SymbolTable, funcTable: SymbolTable):
        decnode,type = funcTable.getter(self.value)
        local_ST = SymbolTable()
        i = 1
        while i < len(decnode.children) - 1:
            decnode.children[i].Evaluate(local_ST,funcTable)
            local_ST.setter(decnode.children[i].children[0],self.children[i-1].Evaluate(table,funcTable))
            i+=1
            
        a = decnode.children[-1].Evaluate(local_ST,funcTable)
        return a
        
class ReturnNode(Node):
    def Evaluate(self, table: SymbolTable,funcTable: SymbolTable):
        return self.children[0].Evaluate(table,funcTable)