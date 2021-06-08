from plyparser import Node, printChildren
import sys
from plysemantics import semanticAnalysis, setVariables, root, variables, getVarType

tNodes = {}

tCounter = 1
lCounter = 1

def generateTAC(node):
    global tCounter
    global lCounter
    if node.type in ["block", "else"]:
        for child in node.children:
            generateTAC(child)
    elif node.type == "declaration":
        varType = node.children[1].type
        print("\n" + varType + "decl(" + node.children[0].type + ")\n")
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
    elif node.type in ["+", "-", "/", "*", "^", "concat"]:
        generateTAC(node.children[0])
        generateTAC(node.children[1])
        print("t" + str(tCounter) + " := " + tNodes[node.children[0]] + " " + node.type + " " + tNodes[node.children[1]])
        tNodes[node] = "t" + str(tCounter)
        tCounter += 1
    elif node.type in ["!=", "==", "<", ">", ">=", "<="]:
        generateTAC(node.children[0])
        generateTAC(node.children[1])
        print("if (" + tNodes[node.children[0]] + " " + node.type + " " + tNodes[node.children[1]] + ") goto L" + str(lCounter))
        print("t" + str(tCounter) + " := false")
        print("goto L" + str(lCounter + 1))
        print("\nL" + str(lCounter))
        print("t" + str(tCounter) + " := true")
        print("\nL" + str(lCounter + 1))
        tNodes[node] = "t" + str(tCounter)
        tCounter += 1
        lCounter += 2
    elif node.type == "and":
        generateTAC(node.children[0])
        generateTAC(node.children[1])
        print("if (" + tNodes[node.children[0]] + ") goto L" + str(lCounter))
        print("t" + str(tCounter) + " := false")
        print("goto L" + str(lCounter + 2))
        print("\nL" + str(lCounter))
        print("if (" + tNodes[node.children[1]] + ") goto L" + str(lCounter + 1))
        print("t" + str(tCounter) + " := false")
        print("goto L" + str(lCounter + 2))
        print("\nL" + str(lCounter + 1))
        print("t" + str(tCounter) + " := true")
        print("\nL" + str(lCounter + 2))
        tNodes[node] = "t" + str(tCounter)
        tCounter += 1
        lCounter += 3
    elif node.type == "or":
        generateTAC(node.children[0])
        generateTAC(node.children[1])
        print("if (" + tNodes[node.children[0]] + ") goto L" + str(lCounter))
        print("if (" + tNodes[node.children[1]] + ") goto L" + str(lCounter))
        print("t" + str(tCounter) + " := false")
        print("goto L" + str(lCounter + 1))
        print("\nL" + str(lCounter))
        print("t" + str(tCounter) + " := true")
        print("\nL" + str(lCounter + 1))
        tNodes[node] = "t" + str(tCounter)
        tCounter += 1
        lCounter += 2
    elif node.type in ["if", "elif"]:
        generateTAC(node.children[0])
        print("if (" + tNodes[node.children[0]] + ") goto L" + str(lCounter))
        print("goto L" + str(lCounter + 1))
        print("\nL" + str(lCounter))
        saveLCount = lCounter
        lCounter += 2
        generateTAC(node.children[1])
        print("\nL" + str(saveLCount + 1))
        if(len(node.children) > 2):
            generateTAC(node.children[2])
        if(len(node.children) > 3):
            generateTAC(node.children[3])
    elif node.type == "while":
        generateTAC(node.children[0])
        print("\nL" + str(lCounter))
        print("if (" + tNodes[node.children[0]] + ") goto L" + str(lCounter+1))
        print("goto L" + str(lCounter + 2))
        print("\nL" + str(lCounter+1))
        saveLCount = lCounter
        lCounter += 3
        generateTAC(node.children[1])
        print("goto L" + str(saveLCount))
        print("\nL" + str(saveLCount + 2))

    elif not node.children:
        if node.type[0] == "-":
            print("t" + str(tCounter) + " := 0 - " + node.type[1:])
            tNodes[node] = "t" + str(tCounter)
            tCounter += 1
        else:
            tNodes[node] = node.type

#printChildren(root)
generateTAC(root)