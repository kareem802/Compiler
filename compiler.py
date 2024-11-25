from preprocessor import preprocess
from lexer import tokenize
from parser import Parser
from Tree_visualizer import print_ast

with open("Test_Source_Code.txt", "r") as file:
    source_code = file.read()
5
pure_HLL = preprocess(source_code)

# print(pure_HLL)

tokens = tokenize(pure_HLL)

for token in tokens:
    print(token)


# Create a parser instance with the token list
parser = Parser(tokens)

# # Parse the tokens and obtain an Abstract Syntax Tree (AST)
ast = parser.parse()

# # Print the AST to verify output
print_ast(ast)