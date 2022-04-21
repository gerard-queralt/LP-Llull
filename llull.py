from antlr4 import *
from llullLexer import llullLexer
from llullParser import llullParser
from EvalVisitor import EvalVisitor
import sys

fileName = sys.argv[1]

if not fileName.endswith(".llull"):
    raise Exception("Arxiu invàlid; ha de ser un arxiu .llull")

input_stream = FileStream(fileName, encoding='utf-8')

initialFun = "main"
params = []
if len(sys.argv) > 2:
    initialFun = sys.argv[2]
    params = list(map(int, sys.argv[3:]))

lexer = llullLexer(input_stream)
token_stream = CommonTokenStream(lexer)
parser = llullParser(token_stream)
tree = parser.root()

evaluator = EvalVisitor()
evaluator.visit(tree)
evaluator.callFun(initialFun, params)
