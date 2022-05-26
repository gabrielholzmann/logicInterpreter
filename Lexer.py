from Tokens import *

class Lexer:
    availableTokens = ['~', '&', '|', '>', '=', '(', ')'];
    tokens = list();
    start = 0;
    current = 0;

    def __init__(self, source):
        self.source = source.replace(" ", "");

    def isAtEnd(self):
        return self.current == len(self.source);

    def scanTokens(self):
        while (not self.isAtEnd()):
            self.start = self.current;
            self.scanToken();

        self.tokens.append(Token(TokenType.EOF, "", None));

        return self.tokens

    def advance(self):
        self.current += 1;
        return self.source[self.current - 1];

    def scanToken(self):
        c = self.advance();

        if(c.isalpha()):
            self.addToken(TokenType.VARIABLE, self.source[self.start]);
        elif(c in self.availableTokens):
            self.addToken(TokenType(self.availableTokens.index(c)));
        else:
            raise Exception(f"Illegal character {c}");

    def addToken(self, type, literal = None):
        lexeme = self.source[self.start:self.current];
        self.tokens.append(Token(type, lexeme, literal)); 
