from Expressions import Visitor

class AstPrinter(Visitor):
    def print(self, expression):
        return expression.accept(self);

    def visitLiteralExpression(self, element):
        return element.value;

    def visitBinaryExpression(self, element):
        return self.display(element.operator.lexeme, element.left, element.right);

    def visitUnaryExpression(self, element):
        return self.display(element.operator.lexeme, element.right);

    def visitGroupingExpression(self, element):
        return self.display("group", element.expression);

    def display(self, name, *args):
        string = "(" + name;

        for arg in args:
            string += " " + str(arg.accept(self));

        string += ")";

        return string;
