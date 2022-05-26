from enum import Enum

class TokenType(Enum):
    NOT = 0
    AND = 1
    OR = 2
    IMPLICATION = 3
    EQUIVALENCE = 4
    LPAREN = 5
    RPAREN = 6
    VARIABLE = 7
    EOF = 8

class Token:
    def __init__(self, type, lexeme, literal):
       self.type = type;
       self.lexeme = lexeme;
       self.literal = literal;

    def __repr__(self) -> str:
        return f'TYPE: {self.type} LEXEME: {self.lexeme} LITERAL {self.literal}';

