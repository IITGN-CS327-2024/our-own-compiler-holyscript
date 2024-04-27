# from ast_classes import *
from astclasses import *
from symbol_table import *
from error_handling import *

_NUM = 1
_STRING = 2
_BOOL = 3
_LIST = 4
_TUP = 5
_DICT = 6
_UNDEF = -100
_ERROR = -1

scope_tree = Scope_tree()
functions = Stack()
E = [e1,e2,e3,e4,e5,e6,e7,e8,e9]

def type_checker(res_type, type):
    if res_type=='any':
        return True
    if isinstance(res_type,dict_type) and isinstance(type,dict_type):
        if res_type.key_type==type.key_type or res_type.key_type=='any':
            return type_checker(res_type.val_type,type.val_type)
    elif isinstance(res_type,list_type) and isinstance(type,list_type):
        return type_checker(res_type.element_type,type.element_type)
    elif isinstance(res_type,tup_type) and isinstance(type,tup_type):
        return type_checker(res_type.element_type,type.element_type)
    else:
        if res_type==type:
            return True
    return False  

def find_in_e(node):
    if isinstance(node,e1):
        return True
    elif isinstance(node,e2):
        return True
    elif isinstance(node,e3):
        return True
    elif isinstance(node,e4):
        return True
    elif isinstance(node,e5):
        return True
    elif isinstance(node,e6):
        return True
    elif isinstance(node,e7):
        return True
    elif isinstance(node,e8):
        return True
    elif isinstance(node,e9):
        return True
    return False

def analyze_expr(node, type):
    if isinstance(node,ASTNode):

        num = node.num_child
        if num==1:
            if isinstance(node,function_call):
                temp = analyze_function_call(node)
                return (type_checker(temp, type))
            elif isinstance(node,function):
                print("hi")
                temp = analyze_function(node)
                return True
            enode = find_in_e(node.children0)
            if enode==True:
                return analyze_expr(node.children0, type)
            elif isinstance(node.children0,expression):
                return analyze_expr(node.children0,type) 
            else:
                data_type = find_all_e_type(node.children0)
                if (all_e_type_consistent(node.children0,data_type))==True:
                    return type_checker(find_all_e_type(node.children0),type)
        elif num==2: 
            if isinstance(node.children0,ou):
                return analyze_expr(node.children1,'num')
            elif isinstance(node.children1,ou):
                return analyze_expr(node.children0,'num')
            elif node.children0.type=="IDENTIFIER":
                if isinstance(node.children1,access_temp):
                    idt_type = scope_tree.type_variable(node.children0)
                    if idt_type==-1:
                        error = Error(node.children0.line, "Variable {} needs to be defined first.".format(node.children0), 'Semantic Analyzer')
                    if isinstance(idt_type,dict_type):
                        access_type = access_handler(idt_type,node.children1,0)
                        return type_checker(access_type,type)
                elif node.children1.type =="LEN":
                    return type_checker(type,'num')     
                elif node.children1.type=='VAL':
                    res_type_idt = scope_tree.type_variable(node.children0)
                    if res_type_idt ==-1:
                        error = Error(node.children0.line, "Variable {} needs to be defined first.".format(node.children0), 'Semantic Analyzer')
                    if isinstance(type, list_type) and isinstance(res_type_idt,dict_type):
                        return type_checker(type.element_type,res_type_idt.val_type)

                elif node.children1.type=='KEYS':
                    res_type_idt = scope_tree.type_variable(node.children0)
                    if res_type_idt==-1:
                        error = Error(node.children0.line, "Variable {} needs to be defined first.".format(node.children0), 'Semantic Analyzer')
                    if isinstance(type, list_type) and isinstance(res_type_idt,dict_type):
                        return type_checker(type.element_type,res_type_idt.key_type)

                elif node.children1.type=='COPY':
                    res_type_idt = scope_tree.type_variable(node.children0)
                    if res_type_idt==-1:
                        error = Error(node.children0.line, "Variable {} needs to be defined first.".format(node.children0), 'Semantic Analyzer')
                    if isinstance(type,list_type) or isinstance(res_type_idt,tup_type) or isinstance(res_type_idt,dict_type):
                        return type_checker(type,res_type_idt)

            elif node.children0.type=='INT' or node.children0.type=='FLOAT' or node.children0.type=='str':
                return analyze_expr(node.children1,'num')+analyze_expr(node.children1,'str')
            
            elif node.children0.type=='SUM':
                idt_type = scope_tree.type_variable(node.children1)
                if idt_type==-1:
                    error = Error(node.children0.line, "Variable {} needs to be defined first.".format(node.children0), 'Semantic Analyzer')
                if (isinstance(idt_type,list_type) or isinstance(idt_type, tup_type)):
                    return type_checker(idt_type.element_type, type) and type=='num'         
            
            elif node.children0.type=='BANG':
                return analyze_expr(node.children1,'bool') or analyze_expr(node.children1,'num')

            else:
                if node.children0.type=='MINUS' and node.children1.type=='NUMBER':
                    return True
            
        elif num==3:
            if isinstance(node.children1,ob):
                return analyze_expr(node.children0,'num') and analyze_expr(node.children2,'num') and type_checker(type,'num')
            elif isinstance(node.children1,ol):
                return analyze_expr(node.children0,'bool') and analyze_expr(node.children2,'bool') and type_checker(type,'bool')
            elif isinstance(node.children1,obi):
                return ((analyze_expr(node.children0,'num') and analyze_expr(node.children2,'num')) or (analyze_expr(node.children0,'bool') and analyze_expr(node.children2,'bool'))) and (type_checker(type,'num') or type_checker(type,'bool'))
            elif node.children1.type=='LESS_EQUAL' or node.children1.type=='GREATER_EQUAL' or node.children1.type=='LESS' or node.children1.type=='GREATER' or node.children1.type=='BANG_EQUAL' or node.children1.type=='EQUAL_EQUAL':
                return (analyze_expr(node.children0,'num') and analyze_expr(node.children2,'num')) and type_checker(type,'bool')
            elif node.children1.type=='MINUS' or node.children1.type=='EXP':
                return analyze_expr(node.children0,'num') and analyze_expr(node.children2,'num') and type_checker('num',type)
            elif node.children1.type=='PLUS':
                return (analyze_expr(node.children0,'num') and analyze_expr(node.children2,'num')) or (analyze_expr(node.children0,'str') and analyze_expr(node.children2,'str')) and (type_checker(type,'num') or type_checker(type,'str'))
            elif node.children0.type=="IDENTIFIER":
                idt_type = scope_tree.type_variable(node.children0)
                if idt_type==-1:
                    error = Error(node.children0.line, "Variable {} needs to be defined first.".format(node.children0), 'Semantic Analyzer')
                if idt_type==-1:
                        error = Error(node.children0.line, "Variable {} needs to be defined first.".format(node.children0), 'Semantic Analyzer')
                if node.children1.type=="COUNT":
                    if isinstance(idt_type, list_type) or isinstance(idt_type,tup_type):
                        return type_checker(find_all_e_type(node.children2.children0),idt_type.element_type)
                elif node.children1.type=="APPEND":
                    return isinstance(idt_type,list_type) and analyze_expr(node.children2,idt_type.element_type)
                elif node.children1.type=="ACCESS":
                    access_type = access_handler2(idt_type,node.children2,0)
                    return type_checker(access_type,type)
                elif node.children1.type=='JOIN':
                    if node.children2.type=='IDENTIFIER':
                        return type_checker(scope_tree.type_variable(node.children0),scope_tree.type_variable(node.children2))
                elif node.children1.type=='POP':
                    return type_checker(idt_type,type) and pop_handler(idt_type,node.children2)
   
        elif num==4:
            if node.children0.type=='IDENTIFIER':
                idt_type = scope_tree.type_variable(node.children0)
                els_type = els_handler(idt_type, node.children2.children0, node.children3)
                return type_checker(idt_type,type) and els_type 

        elif num==5:
            idt_type = scope_tree.type_variable(node.children0)
            if idt_type==-1:
                error = Error(node.children0.line, "Variable {} needs to be defined first.".format(node.children0), 'Semantic Analyzer')
            if isinstance(idt_type,list_type): 
                return analyze_expr(node.children2,'num') and  analyze_expr(node.children4,'num') 
            elif idt_type=='str':
                return analyze_expr(node.children2,'num') and  analyze_expr(node.children4,'num') 
    else:
        if (node.type=='IDENTIFIER'):
            t = scope_tree.type_variable(node)
            if t==-1:
                error = Error(node.line, "Variable {} needs to be defined first.".format(t), 'Semantic Analyzer')
            return type_checker(t,type)
        elif (node.type=='NUMBER'):
            return type=='num'
        elif (node.type=='STRING'):
            return type=='str'
        elif (node.type=='SAHI' or node.type=='GALAT'):
            return type=='bool'
    return False

def check(type, node):
    if node.type=='NUMBER' and type=='num':
        return True
    elif node.type=='str' and  type=='str':
        return True
    return False
   
def pop_handler(idt_type, node):
    num = node.num_child
    for n in range(num):
        temp = getattr(node, "children{}".format(n))
        if isinstance(idt_type, dict_type):
            if not check(idt_type.key_type, temp):
                return False
            idt_type = idt_type.val_type
        if isinstance(idt_type,list_type) or isinstance(idt_type,tup_type):
            if not (temp.type=='NUMBER' and (isinstance(idt_type,list_type) or isinstance(idt_type,tup_type))):
                return False
            idt_type=idt_type.element_type
    return True


def access_handler(var_type, node,line):
    current_type = var_type
    for i in range(node.num_child):
        temp = getattr(node, "children{}".format(i))     
        if isinstance(current_type, dict_type):
            if temp.type=="STRING":
                if not current_type.key_type=='str':
                    error = Error(line, "Arguments not correct",'Semantic Analyzer') 
            elif temp.type=="NUMBER": 
                if not current_type.key_type=='num':
                    error = Error(line, "Arguments not correct",'Semantic Analyzer')
        if isinstance(current_type, dict_type):
            current_type = current_type.val_type
        else:
            current_type = current_type.element_type
    return current_type

def access_handler2(idt_type, node, line):
    cur_type = idt_type
    for i in range(node.num_child):
        temp = getattr(node, "children{}".format(i))
        if temp.type=='NUMBER' and (isinstance(cur_type,list_type) or isinstance(cur_type, tup_type)):
            cur_type = cur_type.element_type
    return cur_type
 
def els_handler(idt_type, node, all_e_node):
    num = node.num_child
    for n in range(num):
        temp = getattr(node, "children{}".format(n))
        if isinstance(idt_type, dict_type):
            if not check(idt_type.key_type, temp):
                return False
            idt_type = idt_type.val_type
        if isinstance(idt_type,list_type) or isinstance(idt_type,tup_type):
            if not (temp.type=='NUMBER' and (isinstance(idt_type,list_type) or isinstance(idt_type,tup_type))):
                return False
            idt_type=idt_type.element_type
    if type_checker(find_all_e_type(all_e_node.children0),idt_type):
        return True
    return False


def find_return_type(node):
    func_types = scope_tree.type_variable(node.children0)
    if func_types==-1:
        return 'no'
    return func_types.outputs


def all_e_type_consistent(node, type):
    if isinstance(type,list_type):
        num_child = node.children0.num_child
        # print(num_child)
        for n in range(0,num_child):
            # print(n)
            childr = "children{}".format(n)
            child = getattr(node.children0, childr)
            print(child)
            print(find_all_e_type(child),'hi')
            print(type.element_type)
            if type_checker(find_all_e_type(child),type.element_type)==0:
                return False
    elif isinstance(type, tup_type):
        num_child = node.num_child
        for n in range(num_child):
            childr = "children{}".format(n)
            child = getattr(node, childr)
            if find_all_e_type(child)!=type.element_type:
                return False 
    elif isinstance(type,dict_type):
        num_child = node.children0.num_child
        for n in range(num_child):
            childr = "children{}".format(n)
            child = getattr(node.children0, childr)
            if find_all_e_type(child.children0)!=type.key_type or find_all_e_type(child.children1)!=type.val_type:
                return False
    return True


def find_all_e_type(node):
    type_list = []
    if isinstance(node,ASTNode):
        num = node.num_child
    else: 
        if node.type=='NUMBER':
            return 'num'
        elif node.type=='STRING':
            return 'str'
        elif (node.type=='SAHI' or node.type=='GALAT'):
            return 'bool'
        else: 
            type_var = scope_tree.type_variable(node)
            if type_var==-1:
                error = Error(node.line, "Variable {} needs to be defined first.".format(node), 'Semantic Analyzer')
            return scope_tree.type_variable(node)
    while (num>0):
        if isinstance(node,els):
            try:
                node = node.children0.children0
                if isinstance(node,ASTNode):
                    num = node.num_child
                type_list.append('els')
            except:
                num = 0
                type_list.append('els')
                type_list.append('any')
        elif isinstance(node,ed):
            try:
                node = node.children0.children0
                k = None
                if node.children0.type=='NUMBER':          
                    k = 'num'
                else:
                    k = 'str'
                if isinstance(node,ASTNode):
                    num = node.num_child
                    node = node.children1
                type_list.append(['ed',k])
            except:
                num = 0
                k = "any"
                type_list.append(['ed',k])
                type_list.append('any')
        elif isinstance(node,et):
            try:
                node = node.children0.children0
                if isinstance(node,ASTNode):
                    num = node.num_child
                type_list.append('et')
            except:
                type_list.append('et')
                type_list.append('any')
        elif isinstance(node,function_call):
            return find_return_type(node)
        elif node.type=='NUMBER':
            num = 0
            type_list.append('num')
        elif node.type=='STRING':
            type_list.append('str')
            num = 0 
        else:
            type_list.append('bool')
            num = 0
    el =type_list[-1]
    new_el = None
    for e in type_list[-2::-1]:
        if isinstance(e,list):
            new_el = dict_type(e[1],el)
        if e == 'els':
            new_el = list_type(el)
        elif e=='et':
            new_el = tup_type(el)
        el = new_el
    
    return el

def list_handler(node, line):
    if node.num_child==1:
        return node.children0
    else:
        return get_type(node, line)
        
def tup_handler(node, line):
    if node.num_child==1:
        return node.children0
    else:
        return get_type(node, line)
        
def dict_handler(node, line):
    val_type = get_type(node.children3, line)
    key_type = node.children2.children0
    return key_type, val_type

def get_type(node, line):
    if node.children0=='list':
        element_type = list_handler(node.children2, line)
        result = list_type(element_type)
        return result
    elif node.children0=='tup':
        element_type = tup_handler(node.children2, line)
        result = tup_type(element_type)
        return result
    elif node.children0=='dict':
        k, val_type = dict_handler(node, line)
        if k!='num' and k!='str' and k!='bool':
            error_msg = "The dictionay can only have num, bool, or STR as the data type."
            error = Error(line, error_msg, 'Semantic Analyzer')
        result = dict_type(k, val_type)
        return result
    else:
        return node.children0

def analyze_declare(line_node):
    data_type_node = line_node.children0
    identifier = line_node.children1
    variable_type = get_type(data_type_node, identifier.line)
    value_expr = line_node.children3
    match = analyze_expr(value_expr, variable_type)
    if match:
        scope_tree.add_variable(identifier, variable_type, identifier.line)
        return True
    else:
        error_msg = "Type of expr assigned does not match with the declared data type for variable '{}'.".format(identifier)
        error = Error(identifier.line, error_msg, 'Semantic Analyzer')
        return False
    
def analyze_assignment(line_node):
    identifier = line_node.children0
    variable_type = scope_tree.type_variable(identifier)
    if isinstance(variable_type, tup_type):
        error_msg = "Tuples can not be updated or re-assigned."
        error = Error(identifier.line, error_msg, 'Semantic Analyzer')
    line = identifier.line
    if variable_type == -1:
        error_msg = "The variable '{}' needs to be defined first.".format(identifier)
        error = Error(line, error_msg, 'Semantic Analyzer')
    if line_node.num_child==3:
        equal_type = line_node.children1.children0
        if str(line_node.children2) == 'input_':
            data_type_node = line_node.children2.children1
            assign_type = get_type(data_type_node, line)
            if assign_type == variable_type:
                match = True
            else:
                match = False
            if not match:
                error = Error(line, "The inpus asks for a different data_type than that of the variable '{}'.".format(identifier))
        else:
            expression = line_node.children2
            match = analyze_expr(expression, variable_type)
            if not match : 
                error = Error(line, "The type of variable '{}' does not match with the assignment expression.".format(identifier), 'Semantic Analyzer')
        if equal_type=='+=' and (variable_type!='str' and variable_type!='num'):
            error = Error(line, "The += can only be used for str and num data_types.", 'Semantic Analyzer')
        if (equal_type=='-=' or equal_type=='/=' or equal_type=='*=') and variable_type!='num':
            error = Error(line, "The {} can only be used for num data_type".format(equal_type))
        return True
    else:
        equal_type = line_node.children2.children0
        access_node = line_node.children1
        variable_type = access_handler(variable_type, access_node, line)
        if str(line_node.children3) == 'input_':
            data_type_node = line_node.children3.children1
            assign_type = get_type(data_type_node, line)
            if assign_type == variable_type:
                match = True
            else:
                match = False
            if not match:
                error = Error(line, "The inpus asks for a different data_type than that of the variable '{}'.".format(identifier))
        else:
            expression = line_node.children3
            match = analyze_expr(expression, variable_type)
            if not match : 
                error = Error(line, "The type of variable '{}' does not match with the assignment expression.".format(identifier), 'Semantic Analyzer')
        if equal_type=='+=' and (variable_type!='str' and variable_type!='num'):
            error = Error(line, "The += can only be used for str and num data_types.", 'Semantic Analyzer')
        if (equal_type=='-=' or equal_type=='/=' or equal_type=='*=') and variable_type!='num':
            error = Error(line, "The {} can only be used for num data_type".format(equal_type))
        return True

def analyze_while(line_node):
    cond = line_node.children1
    match = analyze_expr(cond,'bool')
    if match:
        scope_tree.create_scope('while')
        for i in range(2,line_node.num_child):
            line = getattr(line_node, "children{}".format(i))
            res = analyze_line(line)
        scope_tree.close_scope()
    else:
        error_msg = "Type of expr given as while condition is not of boolean type '{}'.".format(cond)
        error = Error(line_node.children0.line, error_msg, 'Semantic Analyzer')

def analyze_for(line_node):
    declare = line_node.children1
    analyze_declare(declare)
    cond = line_node.children2
    match = analyze_expr(cond,'bool')
    if match:
        scope_tree.create_scope('for')
        for i in range(4,line_node.num_child):
            line = getattr(line_node, "children{}".format(i))
            res = analyze_line(line)
        scope_tree.close_scope()
    else:
        error_msg = "Type of expr given as for condition is not of boolean type '{}'.".format(cond)
        error = Error(line_node.children0.line, error_msg, 'Semantic Analyzer')


def analyze_function(line_node):
    func_name = line_node.children2
    line = func_name.line
    return_type = get_type(line_node.children1, line)
    arg_node = line_node.children3
    args = []
    input_names = []
    for i in range(0, arg_node.num_child, 2):
        temp_type = get_type(getattr(arg_node, "children{}".format(i)), line)
        args.append(temp_type)
        var_name = getattr(arg_node, "children{}".format(i+1))
        input_names.append(var_name)
    function_type = func_type(args, return_type, input_names)
    scope_tree.add_variable(func_name, function_type, line)
    scope_tree.create_scope('function')
    functions.push(function_type)
    for i in range(len(args)):
        scope_tree.add_variable(input_names[i], args[i], line)
    for i in range(4, line_node.num_child):
        in_line = getattr(line_node, "children{}".format(i))
        res = analyze_line(in_line) 
    if function_type.outputs != 'void':
        temp = check_return(scope_tree.current_scope)
        if not temp:
            error = Error(line, "Function misses a return statement.", 'Semantic Analyzer')
    scope_tree.close_scope()
    functions.pop()

def check_return(node):
    if node.has_return:
        return True
    else:
        if len(node.children)==0:
            return False
        else:
            flag = False
            for child in node.children:
                flag = check_return(child)
                if flag:
                    return True
            if not flag:
                return False

def analyze_return (line_node):
    line = line_node.children0.line
    expression_node = line_node.children1
    func = functions.peek()
    if func==None:
        error = Error(line, "The return statement should be inside a function.", 'Semantic Analyzer')
    if not get_type(expression_node, func):
        error = Error(line, "The return type of the expression doesnt match with the one declared.", 'Semantic Analyzer')
    else:
        scope_tree.current_scope.has_return = True

def analyze_closure(line_node):
    identifier = line_node.children1
    line = identifier.line
    return_type1 = get_type(line_node.children0, line)
    return_type2 = get_type(line_node.children4, line)
    if (return_type1 == return_type2):
        arg_node = line_node.children5
        args = []
        input_names = []
        for i in range(0, arg_node.num_child, 2):
            temp_type = get_type(getattr(arg_node, "children{}".format(i)), line)
            args.append(temp_type)
            var_name = getattr(arg_node, "children{}".format(i+1))
            input_names.append(var_name)
        function_type = func_type(args, return_type1)
        scope_tree.add_variable(identifier, function_type, line)
        scope_tree.create_scope('closure')
        functions.push(function_type)
        for i in range(len(args)):
            scope_tree.add_variable(input_names[i], args[i], line)
        for i in range(6, line_node.num_child):
            in_line = getattr(line_node, "children{}".format(i))
            res = analyze_line(in_line) 
        scope_tree.close_scope()
        functions.pop()
        if function_type.outputs != 'void':
            temp = check_return(scope_tree.current_scope)
            if not temp:
                error = Error(line, "Closure misses a return statement.", 'Semantic Analyzer')
    else:
        error_msg = "Type Mismatch in Closure statement '{}'.".format(return_type1,return_type2)
        error = Error(line, error_msg, 'Semantic Analyzer')


def analyze_function_call(line_node):
    func_name = line_node.children0
    line = func_name.line
    arg_node = line_node.children1
    func_type = scope_tree.type_variable(func_name)
    if func_type==-1:
        error = Error(line, "Function called before defining it.", 'Semantic Analyzer')
    if arg_node.num_child > len(func_type.inputs):
        error = Error(line, "Too many arguments for the function", 'Semantic Analyzer')
    if arg_node.num_child < len(func_type.inputs):
        error = Error(line, "Too few arguments for the function", 'Semantic Analyzer')
    for i in range(arg_node.num_child): 
        match = analyze_expr(getattr(arg_node, "children{}".format(i)), func_type.inputs[i])
        if not match:
            error = Error(line, "The argument at position {} doesnt matches with the defination of the function".format(i), 'Semantic Analyzer')
    return func_type.outputs


def analyze_if(line_node):
    cond = line_node.children1
    match = analyze_expr(cond.children0 , 'bool')
    if match:
        scope_tree.create_scope('if')
        for i in range(2,line_node.num_child):
            line = getattr(line_node, "children{}".format(i))
            if isinstance(line,magar_temp):
                scope_tree.close_scope()
                scope_tree.create_scope('elif')
                if (line.num_child==0):
                    continue
                else:
                    cond = line.children1
                    match2 = analyze_expr(cond.children0,'bool')
                    if match2:
                        for i in range(2,line.num_child):
                            line2 = getattr(line, "children{}".format(i))
                            analyze_line(line2)
                        scope_tree.close_scope()
                    else:
                        error_msg = "Type of expr given as elseif condition is not of boolean type '{}'.".format(cond)
                        error = Error(line.children0.line, error_msg, 'Semantic Analyzer')
            elif isinstance(line, nahitoh_temp):
                scope_tree.create_scope('else')
                for i in range(1,line.num_child):
                    line3 = getattr(line, "children{}".format(i))
                    analyze_line(line3)
                scope_tree.close_scope()
            else:
                res = analyze_line(line)
    else:
        error_msg = "Type of expr given as if condition is not of boolean type '{}'.".format(cond)
        error = Error(line_node.children0.line, error_msg, 'Semantic Analyzer')

def analyze_try(line_node):
    scope_tree.create_scope('try')
    for i in range(1,line_node.num_child):
        line = getattr(line_node, "children{}".format(i))
        if isinstance(line,varna):
            scope_tree.close_scope()
            scope_tree.create_scope('varna')
        else:
            res = analyze_line(line)
    scope_tree.close_scope()

def analyze_print(line_node):
    node = line_node.children1
    for i in range(node.num_child):
        temp = getattr(node, "children{}".format(i))
        match = analyze_expr(temp, 'num')


def analyze_line(line_node):
    if isinstance(line_node, declaration):
        res = analyze_declare(line_node)
    elif isinstance(line_node, assignment):
        res = analyze_assignment(line_node)
    elif isinstance(line_node, while_loop):
        res = analyze_while(line_node)
    elif isinstance(line_node, function):
        res = analyze_function(line_node)
    elif isinstance(line_node, function_call):
        res = analyze_function_call(line_node)
    elif isinstance(line_node, for_loop):
        res = analyze_for(line_node)
    elif isinstance(line_node, ifelse):
        res = analyze_if(line_node)
    elif isinstance(line_node, print_):
        res = analyze_print(line_node)
    elif isinstance(line_node, tryelse):
        res = analyze_try(line_node)
    elif isinstance(line_node, closure):
        res = analyze_closure(line_node)
    elif isinstance(line_node, return_func):
        res = analyze_return(line_node)
    

def analyze_program(node):
    func_type_ = func_type(['num', 'num'], 'void', ['value', 'address'])
    scope_tree.add_variable('store', func_type_, -1)
    func_type_ = func_type(['num'], 'num', ['address'])
    scope_tree.add_variable('load', func_type_, -1)
    for i in range(node.num_child):
        line = getattr(node, "children{}".format(i))
        res = analyze_line(line)
    return scope_tree