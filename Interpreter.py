from Expressions import Visitor
from Tokens import TokenType

class Interpreter(Visitor):
    def interpret(self, expression):
        value = self.evaluate(expression);
        return value;

    def evaluate(self, expression):
        return expression.accept(self);

    def visitLiteralExpression(self, element):
        return element.value;

    def visitBinaryExpression(self, element):
        left = self.evaluate(element.left);
        right = self.evaluate(element.right);

        operator = element.operator.type;

        if(operator == TokenType.AND):
            return int(left and right);
        elif(operator == TokenType.OR):
            return int(left or right);
        elif(operator == TokenType.EQUIVALENCE):
            return int(left == right);
        elif(operator == TokenType.IMPLICATION):
            return int(not(left == 1 and right == 0));

    def visitUnaryExpression(self, element):
        right = self.evaluate(element.right);

        operator = element.operator.type;

        if(operator == TokenType.NOT):
            return int(not right);

    def visitGroupingExpression(self, element):
        return self.evaluate(element.expression);

