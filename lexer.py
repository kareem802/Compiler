import re

# construct token dictionary for (keywrods - identifiers - operators - number - punctuation - whitespace)  

TOKEN_PATTERNS = {
    # Keywords
    "VAR_KEYWORD": r"\b(var|num|bool|str)\b",
    "IF": r"\bif\b",
    "ELIF": r"\belif\b",
    "ELSE": r"\belse\b",
    "FUNC": r"\bfunc\b",
    "PRINT": r"\bprint\b",

    # Identifiers
    "IDENTIFIER": r"\b[a-zA-Z_][a-zA-Z0-9_]*\b",

    # Operators
    "COMPARISON_OPERATOR": r"(<=|>=|==|!=|<|>)",
    "ASSIGN": r"=",
    "OPERATOR": r"[+\-*/]",
    # "PLUS": r"\+",
    # "MINUS": r"-",
    # "MULTIPLY": r"\*",
    # "DIVIDE": r"/",

    # Numbers and Strings
    "NUMBER": r"\b\d+\b",
    "STRING": r'"[^"]*"',  # Match text between double quotes

    # Punctuation
    "LPAREN": r"\(",
    "RPAREN": r"\)",
    "LBRACE": r"\{",
    "RBRACE": r"\}",
    "SEMICOLON": r";",

    # Whitespace (ignored by the lexer)
    "WHITESPACE": r"\s+",

    # Comments
    "COMMENT": r"\^\^.*"
}



# using named capturing groups. we combine every pattern with its token name in a single regex

# REGEX_TOKENS = "|".join(f"(?P<{token}>{pattern})" for token, pattern in TOKEN_PATTERNS.items())


# def tokenize(code):
#     tokens = []

#     for match in re.finditer(REGEX_TOKENS, code):
#         token_type = match.lastgroup
#         token_value = match.group(token_type)

#         if token_type != "WHITESPACE" and token_type != "COMMENT":
#             tokens.append((token_type, token_value))
    
#     return tokens

def tokenize(source_code):
    tokens = []
    while source_code:
        match = None
        for token_type, pattern in TOKEN_PATTERNS.items():
            regex = re.compile(pattern)
            match = regex.match(source_code) # match the begining of the text
            if match:
                text = match.group(0)
                if token_type != 'WHITESPACE' and token_type != 'COMMENT':  # Ignore whitespace
                    tokens.append((token_type, text))
                source_code = source_code[len(text):]
                break
        if not match:
            raise ValueError(f"Unrecognized token: {source_code[0]}")
    return tokens