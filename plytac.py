from plyparser import Node, printChildren
import sys
from plysemantics import semanticAnalysis, setVariables, root, variables, getVarType

tNodes = {}

tCounter = 1
lCounter = 1

def generateTAC(node):
    global tCounter
    global lCounter
    if node.type == "block":
        for child in node.children:
            generateTAC(child)
    elif node.type == "declaration":
        varType = node.children[1].type
        print(varType + "decl(" + node.children[0].type + ")")
        tNodes[node] = node.children[0].type
    elif node.type == "assignment":
        generateTAC(node.children[0])
        generateTAC(node.children[1])
        print(tNodes[node.children[0]] + " := " + tNodes[node.children[1]])
    elif node.type in ["int2float", "int2string", "float2string"]:
        generateTAC(node.children[0])
        print("t" + str(tCounter) + " := " + node.type + "(" + tNodes[node.children[0]] + ")")
        tNodes[node] = "t" + str(tCounter)
        tCounter += 1
    elif node.type in ["+", "-", "/", "*", "^", "and", "or", "!=", "==", "<", ">", ">=", "<=", "concat"]:
        generateTAC(node.children[0])
        generateTAC(node.children[1])
        print("t" + str(tCounter) + " := " + tNodes[node.children[0]] + " " + node.type + " " + tNodes[node.children[1]])
        tNodes[node] = "t" + str(tCounter)
        tCounter += 1
    elif not node.children:
        if node.type[0] == "-":
            print("t" + str(tCounter) + " := 0 - " + node.type[1:])
            tNodes[node] = "t" + str(tCounter)
            tCounter += 1
        else:
            tNodes[node] = node.type

generateTAC(root)