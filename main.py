from Tokens import TokenType
from Lexer import Lexer 
from Parser import Parser
from Interpreter import Interpreter
from AstPrinter import AstPrinter
from QuineMcCluskey import QuineMcCluskey

from sys import platform
from shutil import which
import os
 
def instructions():
    print('''instructions:
~ not
& and
| or
> implication
= equivalence
            ''')
def main():
    instructions();

    text = input("expression > ");

    lexer = Lexer(text);
    tokensList = lexer.scanTokens();

    parser = Parser(tokensList); 
    ast = parser.parse();

    astPrinter = AstPrinter()
    print(astPrinter.print(ast))

    interpreter = Interpreter();

    variables = list();
    minterm = list();

    table = "";
        
    for t in tokensList:
        if(t.type == TokenType.VARIABLE and t.lexeme not in variables):
            variables.append(t.lexeme);

    ##table string
    string ="|"

    for i in range(len(variables)):
        string += "  " + variables[i] + "  |";
    string += "  " + "=" + "  |";
    table += string;

    for i in range(0, 1 << len(variables)):
        inputNum = format(i, f'#0{len(variables) + 2}b')[2:];

        for t in tokensList:
            if(t.type == TokenType.VARIABLE):
                index = variables.index(t.lexeme);
                t.literal = int(inputNum[index]);

        parser = Parser(tokensList); 
        ast = parser.parse();

        value = interpreter.interpret(ast)

        if(value == 1):
            minterm.append(inputNum);

        #table string
        string ="|";
        for j in range(len(inputNum)):
            string += "  " + inputNum[j] + "  |";
        string += "  " + str(value) + "  |";
        table +="\n" + string;

    if(platform == "linux" or platform == "linux2"):
        easterEgg(table);
    else:
        print(table);

    #Quine-McCluskey
    if(len(minterm) == 1 << len(variables)):
        #it just generates one big essential prime
        print("TAUTOLOGY: all values evaluate to 1")
        print(text)
    elif(not len(minterm)):
        #it doesn't generate anything
        print("CONTRADICTION: all values evaluate to 0")
        print(text)
    else:
        qm = QuineMcCluskey(variables, minterm);
        simplification = qm.simplify();
        if(platform == "linux" or platform == "linux2"):
            easterEgg(f"    SIMPLIFIED VERSION\n {simplification}");
        else:
            print(simplification);

def easterEgg(table):
    #this is totally useless but it's cool, only works on linux
    if(which("cowsay") is not None and which("lolcat") is not None):
        os.system(f"echo \"{table}\" | cowsay -n -f $(ls /usr/share/cows/ | shuf -n1) | lolcat");
    else:
        print("PRO TIP: install cowsay and lolcat for an easter egg!")
        print(table);

if __name__ == "__main__":
    main()
