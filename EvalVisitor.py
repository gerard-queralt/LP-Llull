if __name__ is not None and "." in __name__:
    from .llullParser import llullParser
    from .llullVisitor import llullVisitor
else:
    from llullParser import llullParser
    from llullVisitor import llullVisitor

import copy


class EvalVisitor(llullVisitor):
    def __init__(self):
        self.funDict = {}
        self.currentFunction = None

    def callFun(self, funName, params):
        fun = self.funDict.get(funName)
        if(fun is None):
            raise NameError("La funcio " + funName + " no existeix")
        fun = copy.deepcopy(fun)
        callingFun = self.currentFunction
        self.currentFunction = fun

        fun.setParamValues(params)
        l = list((getattr(fun, 'ctx')).getChildren())
        i = 3  # saltem el valor de retorn, el nom i el primer parentesi
        while l[i].getText()[0] != '{':
            i += 1
        self.visit(l[i])

        self.currentFunction = callingFun

    def resolveSymbol(self, name):
        symbolDict = getattr(self.currentFunction, 'symbolDict')
        val = symbolDict.get(name)
        if val is None:
            return 0
        return val

    def assignSymbol(self, name, value):
        symbolDict = getattr(self.currentFunction, 'symbolDict')
        symbolDict[name] = copy.deepcopy(
            value) if isinstance(value, list) else value

    def visitFun(self, ctx):
        l = list(ctx.getChildren())
        name = l[1].getText()
        if self.funDict.get(name) is not None:
            raise Exception("La funcio " + name + " ja existeix")
        params = []
        i = 3
        while l[i].getText() != ')':
            if l[i].getText() != ',':
                paramName = l[i].getText()
                if paramName in params:
                    raise Exception("Nom de paràmetre repetit")
                params.append(paramName)
            i += 1
        fun = Function(name, params, ctx)
        self.funDict[name] = fun

    def visitAssig(self, ctx):
        l = list(ctx.getChildren())
        if l[1].getText() == '=':  # assignacio normal
            self.assignSymbol(l[0].getText(), self.visit(l[2]))
        else:  # assignacio composta
            curVal = self.resolveSymbol(l[0].getText())
            exprVal = self.visit(l[3])
            if isinstance(curVal, list) or isinstance(exprVal, list):
                raise Exception("Les taules no es poden operar")
            op = l[1].getText()
            if op == '+':
                curVal += exprVal
            elif op == '-':
                curVal -= exprVal
            elif op == '*':
                curVal *= exprVal
            elif op == '/':
                curVal //= exprVal
            elif op == '%':
                curVal %= exprVal
            else:
                curVal **= exprVal
            self.assignSymbol(l[0].getText(), curVal)

    def visitArray(self, ctx):
        l = list(ctx.getChildren())
        table = [0] * self.visit(l[4])
        self.assignSymbol(l[2].getText(), table)

    def visitGet(self, ctx):
        l = list(ctx.getChildren())
        table = self.resolveSymbol(l[2].getText())
        if not isinstance(table, list):
            raise Exception(l[2].getText() + " no és una taula")
        index = self.visit(l[4])
        if isinstance(index, list):
            raise Exception("L'índex no pot ser una taula")
        if len(table) <= index:
            raise IndexError("Index " + str(index) + " fora de rang")
        return table[index]

    def visitSet(self, ctx):
        l = list(ctx.getChildren())
        table = self.resolveSymbol(l[2].getText())
        if not isinstance(table, list):
            raise Exception(l[2].getText() + " no és una taula")
        index = self.visit(l[4])
        if isinstance(index, list):
            raise Exception("L'índex no pot ser una taula")
        if len(table) <= index:
            raise IndexError("Index " + str(index) + " fora de rang")
        value = self.visit(l[6])
        table[index] = copy.deepcopy(
            value) if isinstance(value, list) else value

    def visitWrite(self, ctx):
        l = list(ctx.getChildren())
        output = ""
        i = 2
        while l[i].getText() != ')':
            if l[i].getText() != ',':
                if isinstance(l[i], llullParser.ExprContext):
                    output += str(self.visit(l[i]))
                else:
                    # eliminem les cometes del començament i el final
                    output += l[i].getText()[1:-1]
                output += ' '
            i += 1
        print(output[:-1])  # eliminem l'ultim espai

    def visitRead(self, ctx):
        l = list(ctx.getChildren())
        i = 2
        while l[i].getText() != ')':
            if l[i].getText() != ',':
                self.assignSymbol(l[i].getText(), int(input(l[i].getText() + " = ")))
            i += 1

    def visitIf(self, ctx):
        l = list(ctx.getChildren())
        condition = self.visit(l[2])
        if isinstance(condition, list):
            raise Exception("La condició no pot ser una taula")
        if condition == 1:
            self.visit(l[4])
        elif len(l) > 5:
            self.visit(l[6])

    def visitWhile(self, ctx):
        l = list(ctx.getChildren())
        condition = self.visit(l[2])
        if isinstance(condition, list):
            raise Exception("La condició no pot ser una taula")
        while condition == 1:
            self.visit(l[4])
            condition = self.visit(l[2])

    def visitFor(self, ctx):
        l = list(ctx.getChildren())
        self.assignSymbol(l[2].getText(), self.visit(l[4]))
        condition = self.visit(l[6])
        if isinstance(condition, list):
            raise Exception("La condició no pot ser una taula")
        while condition == 1:
            self.visit(l[12])
            self.assignSymbol(l[8].getText(), self.visit(l[10]))
            condition = self.visit(l[6])

    def visitCall(self, ctx):
        l = list(ctx.getChildren())
        funName = l[0].getText()
        params = []
        i = 2
        while l[i].getText() != ')':
            text = l[i].getText()
            if(text != ','):
                params.append(self.visit(l[i]))
            i += 1
        self.callFun(funName, params)

    def visitNotExpr(self, ctx):
        l = list(ctx.getChildren())
        val = self.visit(l[1])
        if isinstance(val, list):
            raise Exception("Les taules no es poden operar")
        if val == 1:
            return 0
        else:
            return 1

    def visitMultDivMod(self, ctx):
        l = list(ctx.getChildren())
        first = self.visit(l[0])
        second = self.visit(l[2])
        if isinstance(first, list) or isinstance(second, list):
            raise Exception("Les taules no es poden operar")
        if l[1].getText() == "*":
            return first * second
        elif l[1].getText() == "/":
            if second == 0:
                raise ZeroDivisionError("No es pot dividir entre 0")
            return first // second
        else:
            return first % second

    def visitSumSub(self, ctx):
        l = list(ctx.getChildren())
        first = self.visit(l[0])
        second = self.visit(l[2])
        if isinstance(first, list) or isinstance(second, list):
            raise Exception("Les taules no es poden operar")
        if l[1].getText() == "+":
            return first + second
        else:
            return first - second

    def visitPow(self, ctx):
        l = list(ctx.getChildren())
        first = self.visit(l[0])
        second = self.visit(l[2])
        if isinstance(first, list) or isinstance(second, list):
            raise Exception("Les taules no es poden operar")
        return first ** second

    def visitBoolExpr(self, ctx):
        l = list(ctx.getChildren())
        first = self.visit(l[0])
        second = self.visit(l[2])
        if isinstance(first, list) or isinstance(second, list):
            raise Exception("Les taules no es poden operar")
        if l[1].getText() == "==":
            return boolToInt(first == second)

        elif l[1].getText() == "<>":
            return boolToInt(first != second)

        elif l[1].getText() == "<":
            return boolToInt(first < second)

        elif l[1].getText() == ">":
            return boolToInt(first > second)

        elif l[1].getText() == "<=":
            return boolToInt(first <= second)

        elif l[1].getText() == ">=":
            return boolToInt(first >= second)

        elif l[1].getText() == "&&":
            return boolToInt(first and second)

        else:
            return boolToInt(first or second)

    def visitParenthesis(self, ctx):
        l = list(ctx.getChildren())
        return self.visit(l[1])

    def visitValue(self, ctx):
        l = list(ctx.getChildren())
        if l[0].getSymbol().type == llullParser.SYMBOL:
            return self.resolveSymbol(l[0].getText())
        else:
            return int(l[0].getText())

    def visitBlock(self, ctx):
        l = list(ctx.getChildren())
        i = 1
        while l[i].getText() != '}':
            self.visit(l[i])
            i += 1


class Function:
    def __init__(self, name, params, ctx):
        self.name = name
        self.symbolDict = dict.fromkeys(params, None)
        self.ctx = ctx

    def __deepcopy__(self, memo):
        cls = self.__class__
        result = cls.__new__(cls)
        setattr(result, 'name', self.name)
        setattr(result, 'symbolDict', copy.deepcopy(self.symbolDict, memo))
        setattr(result, 'ctx', self.ctx)
        return result

    def setParamValues(self, values):
        if len(values) != len(self.symbolDict):
            raise Exception("Nombre de parametres incorrecte")
        i = 0
        for p in self.symbolDict:
            if p != ',':
                self.symbolDict[p] = values[i]
                i += 1


def boolToInt(b):
    if b:
        return 1
    return 0
