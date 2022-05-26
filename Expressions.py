from abc import abstractmethod

class Visitor():
    @abstractmethod
    def visitLiteralExpression(self, element):
        pass;

    @abstractmethod
    def visitBinaryExpression(self, element):
        pass;

    @abstractmethod
    def visitUnaryExpression(self, element):
        pass;

    @abstractmethod
    def visitGroupingExpression(self, element):
        pass;

class Literal():
    def __init__(self, value):
        self.value = value;

    def accept(self, visitor):
        return visitor.visitLiteralExpression(self);

class Binary():
    def __init__(self, left, operator, right):
        self.left = left;
        self.operator = operator;
        self.right = right;

    def accept(self, visitor):
        return visitor.visitBinaryExpression(self);

class Unary():
    def __init__(self, operator, right):
        self.operator = operator;
        self.right = right;

    def accept(self, visitor):
        return visitor.visitUnaryExpression(self);
    
class Grouping():
    def __init__(self, expression):
        self.expression = expression;

    def accept(self, visitor):
        return visitor.visitGroupingExpression(self);
