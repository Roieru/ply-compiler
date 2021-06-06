from plyparser import Node, root, printChildren
import sys
import re
import copy

class VariablePLY:
    def __init__(self,value,typ):
        self.typ = typ
        self.value = value

variables = { }

def getVarType(node, varName):
    if node in variables.keys() and varName in (o.value for o in variables[node]):
        return [x for x in variables[node] if x.value == varName][0].typ
    if node.type == "else" or node.type == "elif":
        currentNode = node.parent
        while((currentNode.type == "if" or currentNode.type == "elif") and currentNode.parent):
            currentNode = currentNode.parent
        return getVarType(currentNode, varName)
    if node.parent:
        return getVarType(node.parent, varName)
    else:
        return None

def findScopeNode(node):
    if(node.type in ["block", "for", "dowh", "if", "elif", "else", "while"]):
        return node
    if(node.parent):
        return findScopeNode(node.parent)
    return Node('Self')

def printVariables(r):
    if r.type == "declaration":
        print(r.children[0].type + " declared as " + r.children[1].type + " inside a " + findScopeNode(r).type)
        scopeNode = findScopeNode(r)
        if scopeNode in variables.keys():
            variables[scopeNode].append(VariablePLY(r.children[0].type, r.children[1].type))
        else:
            variables[scopeNode] = [VariablePLY(r.children[0].type, r.children[1].type)]
    if r.children:
        for child in r.children:
            printVariables(child)

def isWithinScope(node, varName):
    if node in variables.keys() and varName in (o.value for o in variables[node]):
        return True
    if node.type == "else" or node.type == "elif":
        currentNode = node.parent
        while((currentNode.type == "if" or currentNode.type == "elif") and currentNode.parent):
            currentNode = currentNode.parent
        return isWithinScope(currentNode, varName)
    if node.parent:
        return isWithinScope(node.parent, varName)
    else:
        return False

def treeNumTypeCheck(node):
    if node.children:
        for child in node.children:
            treeNumTypeCheck(child)
        if node.children[0].ptype == node.children[1].ptype:
            node.ptype = node.children[0].ptype
        else:
            for i in range(len(node.children)):
                if node.children[i].ptype == "int":
                    parseNode = Node('int2float', ptype="float")
                    node.children[i].parent = parseNode
                    parseNode.children = [node.children[i]]
                    node.children[i] = parseNode
            node.ptype = "float"

    else:
        if(re.fullmatch(r'-?\d+([uU]|[lL]|[uU][lL]|[lL][uU])?', node.type)):
            node.ptype = "int"
        elif(re.fullmatch(r'-?((\d+)(\.\d+)(e(\+|-)?(\d+))?|(\d+)e(\+|-)?(\d+))([lL]|[fF])?', node.type)):
            node.ptype = "float"
        else:
            if(not isWithinScope(node, node.type)):
                sys.exit("Variable " + node.type + " has not been declared.")
            varType = getVarType(node, node.type)
            if varType == "string" or varType == "boolean":
                sys.exit("Invalid operation.")
            node.ptype = varType
    #print(node.type + " is " + node.ptype)

def treeStrTypeCheck(node):
    if node.type == "num2string":
        treeNumTypeCheck(node.children[0])
        node.type = node.children[0].ptype + "2string"
        node.ptype = "string"
    elif not node.children:
        if not re.fullmatch(r'\"([^\\\n]|(\\.))*?\"', node.type):
            if not isWithinScope(node, node.type):
                sys.exit("Variable " + node.type + " has not been declared.")
            varType = getVarType(node, node.type)
            if varType != "string":
                sys.exit("Invalid operation.")
        node.ptype = "string"
    else:
        for child in node.children:
            treeStrTypeCheck(child)

def setVariables(r):
    if(r.type == "declaration"):
        if isWithinScope(r, r.children[0].type):
            sys.exit("Variable " + r.children[0].type + " has already been declared within scope.")
        #print(r.children[0].type + " declared as " + r.children[1].type + " inside a " + findScopeNode(r).type)
        scopeNode = findScopeNode(r)
        if scopeNode in variables.keys():
            variables[scopeNode].append(VariablePLY(r.children[0].type, r.children[1].type))
        else:
            variables[scopeNode] = [VariablePLY(r.children[0].type, r.children[1].type)]
    if r.children:
        for child in r.children:
            setVariables(child)

def semanticAnalysis(r):

    checkChildren = True

    if(r.type == "assignment"):
        correctType = ""
        if r.children[0].type == "declaration":
            correctType = r.children[0].children[1].type
        elif (not isWithinScope(r, r.children[0].type)):
            sys.exit("Variable " + r.children[0].type + " has not been declared.")
    elif(r.type in ["+", "-", "/", "*", "^"] or re.match(r'-?\d+([uU]|[lL]|[uU][lL]|[lL][uU])?', r.type)):
        treeNumTypeCheck(r)
        checkChildren = False
    elif(r.type in ["concat", "num2string"] or re.fullmatch(r'\"([^\\\n]|(\\.))*?\"', r.type)):
        treeStrTypeCheck(r)
        checkChildren = False
    if r.children and checkChildren:
        for child in r.children:
            semanticAnalysis(child)

#printVariables(root)
setVariables(root)
semanticAnalysis(root)
printChildren(root)