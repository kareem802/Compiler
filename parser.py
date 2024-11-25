class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0

    def current_token(self):
        return self.tokens[self.position] if self.position < len(self.tokens) else ('EOF', '')

    def match(self, expected_type):
        token = self.current_token()
        if token[0] == expected_type:
            self.position += 1
            return token
        else:
            raise SyntaxError(f"Expected {expected_type} but found {token[0]}")

    def parse(self):
        return self.program()

    # Program -> StatementList
    def program(self):
        return self.statement_list()

    # StatementList -> Statement StatementList | ε
    def statement_list(self):
        statements = []
        while self.current_token()[0] not in ('EOF', '}'):
            statement = self.statement()
            if statement is None:  # Base case for ε
                break
            statements.append(statement)
        return {'type': 'StatementList', 'statements': statements}

    # Statement -> VariableDeclaration | FunctionDefinition | IfStatement | ForLoop | FunctionCall | Comment | ε
    def statement(self):
        current_type = self.current_token()[0]
        if current_type == 'VAR_KEYWORD':
            return self.variable_declaration()
        elif current_type == 'PRINT':
            return self.print_statement()
        elif current_type == 'FUNC':
            return self.function_definition()
        elif current_type == 'IF':
            return self.if_statement()
        elif current_type == 'FOR':
            return self.for_loop()
        elif current_type == 'SEMICOLON':  # Check for standalone semicolon
            self.match('SEMICOLON')  # Match and ignore it
            return {'type': 'EmptyStatement'}  # Return an empty statement node
        elif current_type == 'IDENTIFIER' or current_type == 'KEYWORD':
            return self.function_call()
        return None  # ε (empty production)

        
    # Condition -> BoolExpr (ComparisonOperator BoolExpr)*
    def condition(self):
        left = self.expression()  # Parse the first part of the condition (e.g., a boolean or numeric expression)

        # Check if there is a comparison operator to make a composite condition
        while self.current_token()[0] == 'COMPARISON_OPERATOR':
            operator = self.match('COMPARISON_OPERATOR')  # Match the comparison operator (e.g., ==, !=, >, <)
            right = self.expression()  # Parse the right side of the comparison
            left = {'type': 'Condition', 'left': left, 'operator': operator, 'right': right}  # Build the condition as a composite structure

        return left  # Return the full condition expression

    def print_statement(self):
            self.match('PRINT')   # Match "print" keyword
            self.match('LPAREN')       # Match opening parenthesis
            expression = self.expression()  # Parse the expression inside the parentheses
            self.match('RPAREN')       # Match closing parenthesis
            self.match('SEMICOLON')       # Match closing SEMICOLON
            return {'type': 'PrintStatement', 'expression': expression}

    # VariableDeclaration -> VarKeyword Identifier "=" Expression ";"
    def variable_declaration(self):
        var_type = self.match('VAR_KEYWORD')
        identifier = self.match('IDENTIFIER')
        self.match('ASSIGN')  # Assign symbol
        expression = self.expression()
        self.match('SEMICOLON')
        return {'type': 'VariableDeclaration', 'var_type': var_type, 'identifier': identifier, 'expression': expression}

    # FunctionDefinition -> "func" Identifier "{" FunctionBody "}"
    def function_definition(self):
        self.match('FUNC')
        identifier = self.match('IDENTIFIER')
        self.match('LBRACE')
        body = self.statement_list()
        self.match('RBRACE')
        return {'type': 'FunctionDefinition', 'identifier': identifier, 'body': body}

    # IfStatement -> "if" "(" Condition ")" "{" Action "}" ElifPart ElsePart
    def if_statement(self):
        self.match('IF')
        self.match('LPAREN')
        condition = self.condition()
        self.match('RPAREN')
        self.match('LBRACE')
        action = self.statement_list()
        self.match('RBRACE')
        elif_part = self.elif_part()
        else_part = self.else_part()
        return {'type': 'IfStatement', 'condition': condition, 'action': action, 'elif_part': elif_part, 'else_part': else_part}

    # ElifPart -> "elif" "(" Condition ")" "{" Action "}" | ε
    def elif_part(self):
        if self.current_token()[0] == 'ELIF':
            self.match('ELIF')
            self.match('LPAREN')
            condition = self.condition()
            self.match('RPAREN')
            self.match('LBRACE')
            action = self.statement_list()
            self.match('RBRACE')
            return {'type': 'ElifPart', 'condition': condition, 'action': action}
        return None  # ε

    # ElsePart -> "else" "{" Action "}" | ε
    def else_part(self):
        if self.current_token()[0] == 'ELSE':
            self.match('ELSE')
            self.match('LBRACE')
            action = self.statement_list()
            self.match('RBRACE')
            return {'type': 'ElsePart', 'action': action}
        return None  # ε

    # ForLoop -> "for" "(" VariableDeclaration "," Condition "," LoopAction ")" "{" ActionList "}"
    def for_loop(self):
        self.match('FOR')
        self.match('LPAREN')
        var_decl = self.variable_declaration()
        self.match('SEMICOLON')
        condition = self.condition()
        self.match('SEMICOLON')
        loop_action = self.loop_action()
        self.match('RPAREN')
        self.match('LBRACE')
        action_list = self.statement_list()
        self.match('RBRACE')
        return {'type': 'ForLoop', 'init': var_decl, 'condition': condition, 'loop_action': loop_action, 'body': action_list}

    # LoopAction -> Identifier "=" Expression
    def loop_action(self):
        identifier = self.match('IDENTIFIER')
        self.match('ASSIGN')
        expression = self.expression()
        return {'type': 'LoopAction', 'identifier': identifier, 'expression': expression}

    # FunctionCall -> (Identifier | Keyword) "(" Expression ")"
    def function_call(self):
        identifier = self.match('IDENTIFIER')
        self.match('LPAREN')
        expression = self.expression()
        self.match('RPAREN')
        return {'type': 'FunctionCall', 'identifier': identifier, 'expression': expression}

   # Expression -> BoolExpr | NumExpr | StrExpr | Identifier
    def expression(self):
        current_type = self.current_token()[0]
        if current_type == 'TRUE' or current_type == 'FALSE':
            return self.bool_expr()
        elif current_type == 'NUMBER' or current_type == 'IDENTIFIER':  # Add IDENTIFIER here
            return self.num_expr()
        elif current_type == 'STRING':
            return self.str_expr()
        raise SyntaxError(f"Unexpected token in expression: {self.current_token()}")

    # BoolExpr -> "true" | "false"
    def bool_expr(self):
        bool_token = self.match('TRUE') if self.current_token()[0] == 'TRUE' else self.match('FALSE')
        return {'type': 'BoolExpr', 'value': bool_token}

    # NumExpr -> (Number | Identifier) (Operator (Number | Identifier))*
    def num_expr(self):
        # First term could be a number or an identifier
        left = self.match('NUMBER') if self.current_token()[0] == 'NUMBER' else self.match('IDENTIFIER')
        
        # Check for further operations
        while self.current_token()[0] == 'OPERATOR':
            op = self.match('OPERATOR')
            # Right term could be a number or an identifier
            right = self.match('NUMBER') if self.current_token()[0] == 'NUMBER' else self.match('IDENTIFIER')
            left = {'type': 'NumExpr', 'left': left, 'operator': op, 'right': right}
        
        return left

    # StrExpr -> '"' StringContent '"'
    def str_expr(self):
        str_value = self.match('STRING')
        return {'type': 'StrExpr', 'value': str_value}
    