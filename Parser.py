from Tokens import *
from Expressions import *

#Grammar Rules:
#expression = equivalence;
#equivalence = implication ("=" implication)*;
#implication = or (">" or)*;
#or = and ("|" and)*;
#and = not ("&" not)*;
#not = (~) not | primary
#primary = VARIABLE | "(" expression ")";

class Parser:
    current = 0;

    def __init__(self, tokens):
        self.tokens = tokens;

    def parse(self):
        return self.expression();

    def expression(self):
        return self.equivalenceNode();
    
    def equivalenceNode(self):
        expression = self.implicationNode();

        while(self.match(TokenType.EQUIVALENCE)):
            operator = self.previous();
            right = self.implicationNode();
            expression = Binary(expression, operator, right);

        return expression;


    def implicationNode(self):
        expression = self.orNode();

        while(self.match(TokenType.IMPLICATION)):
            operator = self.previous();
            right = self.orNode();
            expression = Binary(expression, operator, right);

        return expression;

    def orNode(self):
        expression = self.andNode();

        while(self.match(TokenType.OR)):
            operator = self.previous();
            right = self.andNode();
            expression = Binary(expression, operator, right);

        return expression;

    def andNode(self):
        expression = self.notNode();

        while(self.match(TokenType.AND)):
            operator = self.previous();
            right = self.notNode();
            expression = Binary(expression, operator, right);

        return expression;

    def notNode(self):
        if(self.match(TokenType.NOT)):
            operator = self.previous();
            right = self.notNode();
            return Unary(operator, right);

        return self.primaryNode();


    def primaryNode(self):
        if(self.match(TokenType.VARIABLE)):
            return Literal(self.previous().literal);

        if(self.match(TokenType.LPAREN)):
            expression = self.expression();

            if(self.check(TokenType.RPAREN)):
                self.advance()
                return Grouping(expression);
            raise Exception(f"Expected )");


        raise Exception(f"Expected expression");


    def match(self, type):
        if(self.check(type)):
            self.advance();
            return True;
        return False;


    def check(self, type):
        if(self.isAtEnd()): return False;
        return self.peek().type == type;

    def advance(self):
        self.current += 1;

    def isAtEnd(self):
        return self.peek().type == TokenType.EOF;

    def peek(self):
        return self.tokens[self.current];

    def previous(self):
        return self.tokens[self.current - 1];
