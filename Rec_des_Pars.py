buffer = []
scan_cnt = 0

KEYWORD = {"main", "if", "then", "else", "while", "do", "begin",
           "end", "var", "integer", "real", "for", "function",
           "array", "procedure", "result", "program", "READ", "WRITE"}
RELOP = {"=", "<>", "<=", ">=", ">", "<"}
ADDOP = {"+", "-", "or"}
MULOP = {"*", "/", "div", "mod", "and"}
ASSIGNOP = {":="}
SPECIALSYMBOL = {"(", ")", ",", ":", ";"}
CONSTANT = list(range(0, 10))

def Type_Detection(type):
    if type in KEYWORD:
        return "KEYWORD"
    elif type in RELOP:
        return "RELOP"
    elif type in ADDOP:
        return "ADDOP"
    elif type in MULOP:
        return "MULOP"
    elif type in ASSIGNOP:
        return "ASSIGNOP"
    elif type in SPECIALSYMBOL:
        return "SPECIALSYMBOL"
    elif type in CONSTANT:
        return "CONSTANT"
    else:
        return "IDENTIFIER"


with open("source_code.txt") as f:
    token_table = open("token_table.txt", "w")
    for line in f:
        for word in line.split():
            temp = [word, Type_Detection(word)]
            buffer.extend([temp])
            token_table.write(str(temp) + "\n")
    token_table.close()


def nextToken():
    global scan_cnt
    if scan_cnt > len(buffer):
        return "Error in reading buffer!"
    else:
        temp = [buffer[scan_cnt]]
        scan_cnt += 1
        return temp

# print(nextToken())

def identifier_list(token):
    # if identifier_list(token):
    if token[0][1] == "IDENTIFIER":
        token = nextToken()
        if token[0][0] == ",":
            token = nextToken()
            if token[0][1] == "IDENTIFIER":
                return True
        else:
            global scan_cnt
            scan_cnt -= 1
            return True
    # elif token[0][1] == "IDENTIFIER":
    #     return True


def standard_type(token):
    if token[0][0] == "integer":
        return True
    elif token[0][0] == "real":
        return True


def array_type(token):
    if token[0][0] == "array":
        token = nextToken()
        if token[0][0] == "[":
            token = nextToken()
            if token[0][1] == "CONSTANT":
                token = nextToken()
                if token[0][0] == "..":
                    token = nextToken()
                    if token[0][1] == "CONSTANT":
                        token = nextToken()
                        if token[0][0] == "]":
                            token = nextToken()
                            if token[0][0] == "of":
                                token = nextToken()
                                if standard_type(token):
                                    return True


def type_func(token):
    if standard_type(token):
        return True
    elif array_type(token):
        return True


def declaration_list(token):
    if identifier_list(token):
        token = nextToken()
        if token[0][0] == ":":
            token = nextToken()
            if type_func(token):
                token = nextToken()
                if token[0][0] == ";":
                    return True
    elif declaration_list(token):
        token = nextToken()
        if identifier_list(token):
            token = nextToken()
            if token[0][0] == ":":
                token = nextToken()
                if type_func(token):
                    token = nextToken()
                    if token[0][0] == ";":
                        return True


def declarations(token):
    if token[0][0] == "var":
        token = nextToken()
        if declaration_list(token):
            return True
    else:
        global scan_cnt
        scan_cnt -= 1
        return True


def parameter_list(token):
    if identifier_list(token):
        token = nextToken()
        if token[0][0] == ":":
            token = nextToken()
            if type_func(token):
                return True
    elif parameter_list(token):
        token = nextToken()
        if token[0][0] == ";":
            token = nextToken()
            if identifier_list(token):
                token = nextToken()
                if token[0][0] == ":":
                    token = nextToken()
                    if type_func(token):
                        return True


def arguments(token):
    if token[0][0] == "(":
        token = nextToken()
        if parameter_list(token):
            token = nextToken()
            if token[0][0] == ")":
                return True
    else:
        global scan_cnt
        scan_cnt -= 1
        return True


def subprogram_head(token):
    if token[0][0] == "function":
        token = nextToken()
        if token[0][1] == "IDENTIFIER":
            token = nextToken()
            if arguments(token):
                token = nextToken()
                if token[0][0] == ":":
                    token = nextToken()
                    if token[0][0] == "result":
                        token = nextToken()
                        if standard_type(token):
                            token = nextToken()
                            if token[0][0] == ";":
                                return True
    elif token[0][0] == "procedure":
        token = nextToken()
        if token[0][1] == "IDENTIFIER":
            token = nextToken()
            if arguments(token):
                token = nextToken()
                if token[0][0] == ";":
                    return True


def subprogram_declaration(token):
    if subprogram_head(token):
        token = nextToken()
        if declarations(token):
            token = nextToken()
            if compound_statement(token):
                return True


def subprogram_declarations(token):
    # if subprogram_declarations(token):
    #     token = nextToken()
    if subprogram_declaration(token):
            return True
    else:
        global scan_cnt
        scan_cnt -= 1
        return True


def function_reference(token):
    if token[0][1] == "IDENTIFIER":
        token = nextToken()
        if token[0][0] == "(":
            token = nextToken()
            if expression_list(token):
                token = nextToken()
                if token[0][0] == ")":
                    return True
        else:
            global scan_cnt
            scan_cnt -= 1
            return True


def factor(token):
    if function_reference(token):
        return True
    elif variable(token):
        return True
    elif token[0][1] == "CONSTANT":
        return True
    elif token[0][0] == "(":
        token = nextToken()
        if expression(token):
            token = nextToken()
            if token[0][0] == ")":
                return True
    elif function_reference(token):
        return True
    elif token[0][0] == "not":
        token = nextToken()
        if factor(token):
            return True


def term(token):
    if factor(token):
        return True
    elif term(token):
        token = nextToken()
        if token[0][1] == "MULOP":
            token = nextToken()
            if factor(token):
                return True


def sign(token):
    if token[0][0] == "+":
        return True
    elif token[0][0] == "-":
        return True
    else:
        global scan_cnt
        scan_cnt -= 1
        return True


def simple_expression(token):
    if term(token):
        return True
    elif sign(token):
        token = nextToken()
        if term(token):
            return True
    elif simple_expression(token):
        token = nextToken()
        if token[0][1] == "ADDOP":
            token = nextToken()
            if term(token):
                return True


def expression(token):
    if simple_expression(token):
        token = nextToken()
        if token[0][1] == "RELOP":
            token = nextToken()
            if simple_expression(token):
                return True
        else:
            global scan_cnt
            scan_cnt -= 1
            return True


def expression_list(token):
    if expression(token):
        # return True
    # elif expression_list(token):
        token = nextToken()
        if token[0][0] == ",":
            token = nextToken()
            if expression(token):
                return True
        else:
            global scan_cnt
            scan_cnt -= 1
            return True


def variable(token):
    if token[0][1] == "IDENTIFIER":  #-------wrong
        token = nextToken()
        if token[0][0] == "[":
            token = nextToken()
            if expression(token):
                token = nextToken()
                if token[0][0] == "]":
                    return True
        else:
            global scan_cnt
            scan_cnt -= 1
            return True


def procedure_statement(token):
    if token[0][1] == "IDENTIFIER":
        token = nextToken()
        if token[0][0] == "(":
            token = nextToken()
            if expression(token):
                token = nextToken()
                if token[0][0] == ")":
                    return True
        else:
            global scan_cnt
            scan_cnt -= 1
            token = nextToken()
            if token[0][1] == "IDENTIFIER":
                return True


def elementary_statement(token):
    if variable(token):
        token = nextToken()
        if token[0][1] == "ASSIGNOP":
            token = nextToken()
            if expression(token):
                return True
    elif procedure_statement(token):
        return True
    elif compound_statement(token):
        return True


def restricted_statement(token):
    if elementary_statement(token):
        return True
    elif token[0][0] == "if":
        token = nextToken()
        if expression(token):
            token = nextToken()
            if token[0][0] == "then":
                token = nextToken()
                if restricted_statement(token):
                    token = nextToken()
                    if token[0][0] == "else":
                        token = nextToken()
                        if restricted_statement(token):
                            return True
    elif token[0][0] == "while":
        token = nextToken()
        if expression(token):
            token = nextToken()
            if token[0][0] == "do":
                token = nextToken()
                if restricted_statement(token):
                    return True


def statement(token):z
    if elementary_statement(token):
        return True
    elif token[0][0] == "if":
        token = nextToken()
        if expression(token):
            token = nextToken()
            if token[0][0] == "then":
                token = nextToken()
                if restricted_statement(token):
                    token = nextToken()
                    if token[0][0] == "else":
                        token = nextToken()
                        if statement(token):
                            return True
    elif token[0][0] == "if":
        token = nextToken()
        if expression(token):
            token = nextToken()
            if token[0][0] == "then":
                token = nextToken()
                if statement(token):
                    return True
    elif token[0][0] == "while":
        token = nextToken()
        if expression(token):
            token = nextToken()
            if token[0][0] == "do":
                token = nextToken()
                if statement(token):
                    return True


def statement_list(token):
    if statement(token):
        return True
    elif statement_list(token):
        token = nextToken()
        if token[0][0] == ";":
            token = nextToken()
            if statement(token):
                return True


def compound_statement(token):
    if token[0][0] == "begin":
        token = nextToken()
        if statement_list(token):
            token = nextToken()
            if token[0][0] == "end":
                return True


def program(token):
    if token[0][0] == "program":
        token = nextToken()
        if token[0][1] == "IDENTIFIER":
            token = nextToken()
            if token[0][0] == "(":
                token = nextToken()
                # print(token)
                if identifier_list(token):
                    token = nextToken()
                    if token[0][0] == ")":
                        token = nextToken()
                        if token[0][0] == ";":
                            token = nextToken()
                            if declarations(token):
                                token = nextToken()
                                if subprogram_declarations(token):
                                    token = nextToken()
                                    if compound_statement(token):
                                        return True


if __name__ == '__main__':
    if program(nextToken()):
        print("Parse Successfully Done!")
    else:
        print("Some Error has occurred during parsing!")

