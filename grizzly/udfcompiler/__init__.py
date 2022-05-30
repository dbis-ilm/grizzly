# Top level compiler call for grizzly connection
import os
from antlr4 import *
from grizzly.udfcompiler.py_parser.Python3d3Lexer import Python3d3Lexer
from grizzly.udfcompiler.py_parser.Python3d3Parser import Python3d3Parser
from grizzly.udfcompiler.py_parser.Python3d3Visitor import Python3d3Visitor

def compile(input, templates, params):
    # Check if passed argument is a file or a string
    if os.path.isfile(input):
        input_stream = FileStream(input)
    else:
        input_stream = InputStream(input)

    # Create the lexer from the input
    lexer = Python3d3Lexer(input_stream)
    # Create the tokenstream from the lexer
    stream = CommonTokenStream(lexer)
    # Create the parser with the tokenstream
    parser = Python3d3Parser(stream)
    # Create the syntax tree with the file_input as the first executed rule (node)
    tree = parser.file_input()

    # Create the grammar visitor
    visitor = Python3d3Visitor(templates, params)
    # visit the syntax tree
    visitor.visit(tree)

    #print(visitor.contains_stmts)

    # Add statements that should be queried before PL/SQL Block
    pre = "\n ".join(line for line in visitor.pre)
    
    plsql_function = ""

    # Collect all exceptions in udf
    for exception in visitor.exceptions:
        plsql_function += (f"\n{exception}")

    # Add assignment statements for DECLARE block
    for var, assignment in visitor.assignments.items():
        if var not in (param.name for param in params):
            plsql_function += (f"\n{var} {assignment};")

    # Add cursors after variable declaration
    for line in visitor.cursor:
        plsql_function += (f"\n{line};")
    
    # Add Statements for BEGIN block
    plsql_function += "\n".join(str(line) for line in visitor.statements)
    
    return pre, plsql_function
