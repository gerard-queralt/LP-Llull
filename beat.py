from antlr4 import *
from llullLexer import llullLexer
from llullParser import llullParser
from PrinterVisitor import PrinterVisitor
import sys

fileName = sys.argv[1]

if not fileName.endswith(".llull"):
    raise Exception("Arxiu invàlid; ha de ser un arxiu .llull")

input_stream = FileStream(fileName, encoding='utf-8')

lexer = llullLexer(input_stream)
token_stream = CommonTokenStream(lexer)
parser = llullParser(token_stream)
tree = parser.root()

beatificador = PrinterVisitor()
beatificador.visit(tree)
