from preprocessor import preprocess
from lexer import tokenize
from parser import Parser

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

def print_ast(ast, level=0):
    # Base case: if the node is a simple value or leaf node
    if isinstance(ast, dict):
        for key, value in ast.items():
            if isinstance(value, dict):  # If the value is another dictionary, recursively print
                print("---" * level + f"{key}:")
                print_ast(value, level + 1)
            elif isinstance(value, list):  # If the value is a list, iterate and print
                print("---" * level + f"{key}:")
                for item in value:
                    print_ast(item, level + 1)
            else:  # Simple value
                print("---" * level + f"{key}: {value}")
    else:
        # If the node is a simple value (like a string, number, or identifier)
        print("---" * level + str(ast))

# Example of how to use the print function

print_ast(ast)
