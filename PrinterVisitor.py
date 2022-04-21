if __name__ is not None and "." in __name__:
    from .llullParser import llullParser
    from .llullVisitor import llullVisitor
else:
    from llullParser import llullParser
    from llullVisitor import llullVisitor

from colorama import init
from termcolor import colored


class PrinterVisitor(llullVisitor):
    def __init__(self):
        init()  # colorama
        self.level = 0
        self.firstFun = True

    def visitFun(self, ctx):
        l = list(ctx.getChildren())
        if not self.firstFun:
            print("")
        else:
            self.firstFun = False
        print(colored(l[0].getText(), 'red'), colored(l[1].getText(), 'magenta'), end="")
        i = 2
        while l[i - 1].getText() != ')':
            print(l[i].getText(), end="")
            if l[i].getText() == ',':
                print(" ", end="")
            i += 1
        self.visit(l[i])
        print("")

    def visitAssig(self, ctx):
        l = list(ctx.getChildren())
        exprIndex = 2
        if l[1].getText() == '=':  # assignacio normal
            print(l[0].getText() + " = ", end="")
        else:  # assignacio composta
            print(l[0].getText(), l[1].getText() + "= ", end="")
            exprIndex += 1
        self.visit(l[exprIndex])

    def visitArray(self, ctx):
        l = list(ctx.getChildren())
        print("array(" + l[2].getText() + ", ", end="")
        self.visit(l[4])
        print(")", end="")

    def visitGet(self, ctx):
        l = list(ctx.getChildren())
        print("get(" + l[2].getText() + ", ", end="")
        self.visit(l[4])
        print(")", end="")

    def visitSet(self, ctx):
        l = list(ctx.getChildren())
        print("set(" + l[2].getText() + ", ", end="")
        self.visit(l[4])
        print(", ", end="")
        self.visit(l[6])
        print(")", end="")

    def visitWrite(self, ctx):
        l = list(ctx.getChildren())
        print("write(", end="")
        i = 2
        while l[i].getText() != ')':
            if l[i].getText() != ',':
                if isinstance(l[i], llullParser.ExprContext):
                    self.visit(l[i])
                else:
                    print(colored(l[i].getText(), 'green'), end="")
            else:
                print(", ", end="")
            i += 1
        print(")", end="")

    def visitRead(self, ctx):
        l = list(ctx.getChildren())
        print("read(", end="")
        i = 2
        while l[i - 1].getText() != ')':
            print(l[i].getText(), end="")
            if l[i].getText() == ',':
                print(" ", end="")
            i += 1

    def visitIf(self, ctx):
        l = list(ctx.getChildren())
        print(colored("if", 'red'), "(", end="")
        self.visit(l[2])
        print(")", end="")
        if l[4].getRuleIndex() != llullParser.RULE_block:
            print("")
            print("    " * (self.level + 1), end="")
        self.visit(l[4])
        if len(l) > 5:
            if l[4].getRuleIndex() != llullParser.RULE_block:
                print("")
                print("    " * self.level, end="")
            else:
                print(" ", end="")
            print(colored("else", 'red'), end="")
            if l[6].getRuleIndex() != llullParser.RULE_block:
                print(" ", end="")
            self.visit(l[6])

    def visitWhile(self, ctx):
        l = list(ctx.getChildren())
        print(colored("while", 'red'), "(", end="")
        self.visit(l[2])
        print(")", end="")
        if l[4].getRuleIndex() != llullParser.RULE_block:
            print("")
            print("    " * (self.level + 1), end="")
        self.visit(l[4])

    def visitFor(self, ctx):
        l = list(ctx.getChildren())
        print(colored("for", 'red'), "(" + l[2].getText() + " = ", end="")
        self.visit(l[4])
        print("; ", end="")
        self.visit(l[6])
        print("; " + l[8].getText() + " = ", end="")
        self.visit(l[10])
        print(")", end="")
        if l[12].getRuleIndex() != llullParser.RULE_block:
            print("")
            print("    " * (self.level + 1), end="")
        self.visit(l[12])

    def visitCall(self, ctx):
        l = list(ctx.getChildren())
        print(colored(l[0].getText(), 'blue') + "(", end="")
        i = 2
        while l[i].getText() != ')':
            text = l[i].getText()
            if(text != ','):
                self.visit(l[i])
            else:
                print(", ", end="")
            i += 1
        print(")", end="")

    def visitNotExpr(self, ctx):
        l = list(ctx.getChildren())
        print("!", end="")
        self.visit(l[1])

    def visitMultDivMod(self, ctx):
        l = list(ctx.getChildren())
        self.visit(l[0])
        print(" " + l[1].getText() + " ", end="")
        self.visit(l[2])

    def visitSumSub(self, ctx):
        l = list(ctx.getChildren())
        self.visit(l[0])
        print(" " + l[1].getText() + " ", end="")
        self.visit(l[2])

    def visitPow(self, ctx):
        l = list(ctx.getChildren())
        self.visit(l[0])
        print(" " + l[1].getText() + " ", end="")
        self.visit(l[2])

    def visitBoolExpr(self, ctx):
        l = list(ctx.getChildren())
        self.visit(l[0])
        print(" " + l[1].getText() + " ", end="")
        self.visit(l[2])

    def visitParenthesis(self, ctx):
        l = list(ctx.getChildren())
        print("(", end="")
        self.visit(l[1])
        print(")", end="")

    def visitValue(self, ctx):
        l = list(ctx.getChildren())
        if l[0].getSymbol().type == llullParser.SYMBOL:
            print(l[0].getText(), end="")
        else:
            print(colored(l[0].getText(), 'cyan'), end="")

    def visitBlock(self, ctx):
        l = list(ctx.getChildren())
        print(" {")
        self.level += 1
        i = 1
        while l[i].getText() != '}':
            print("    " * self.level, end="")
            self.visit(l[i])
            print("")
            i += 1
        self.level -= 1
        print("    " * self.level + "}", end="")
