import re
from isa import *

reserved_keys = ['==','=','<','+','-','*','/','&','|','~','int','string','print','{','}','(',')','while','interruption','input']

def read_file(path):
    res = ""
    with open(path,'r') as program:
        res = program.read()
    return res

def add_spaces(text):
    # First handle the minus operator transformation (a-x → a + -x)
    text = re.sub(r'([a-zA-Z0-9_\)])\s*-\s*([a-zA-Z0-9_\(])', r'\1 + -\2', text)
    
    # Handle special operators (- and ~) separately
    other_ops = [op for op in reserved_keys if op not in ['-', '~']]
    other_ops_sorted = sorted(other_ops, key=len, reverse=True)
    escaped_ops = [re.escape(op) for op in other_ops_sorted]
    
    # Pattern for standard operators
    ops_pattern = rf'(\s*(?:{"|".join(escaped_ops)})\s*)'
    
    # Process tilde operators - space before but not after
    text = re.sub(r'(?<!\s)(~)', r' ~', text)
    
    # Process other operators with standard spacing
    text = re.sub(ops_pattern, lambda m: f' {m.group(1).strip()} ', text)
    
    # Clean up spaces
    return ' '.join(text.split())


def generate_machine_code(opcode,r1=Registers.G1,r2=Registers.G1,val=0,addr = 0):
    code = ''
    op = f"{opcode_to_machine[opcode]:#01x}"[2:]
    r1  = f"{int(r1):#01x}"[2:]
    if (opcode == Opcode.LOADIM):
        val = f"{val:#07x}"[2:]
        while (len(val) > 5):
            val = val[1:]
        code = f"{op}8{val}{r1}"
    elif (opcode == Opcode.STORE):
        if (r2 == None): 
         addr = f"{addr:#07x}"[2:]
         code = f"{op}E{addr}{r1}"
        else:
          r2 = f"{int(r2):#01x}"[2:]
          code = f"{op}F0000{r1}{r2}"
    elif (opcode == Opcode.LOAD):
        if (r2 == None):  
         addr = f"{addr:#07x}"[2:]
         code = f"{op}A{addr}{r1}"
        else:
          r2 = f"{int(r2):#01x}"[2:]
          code = f"{op}B0000{r1}{r2}"
    elif (opcode  == Opcode.JMP):
        addr = f"{addr:#08x}"[2:]
        code = f"{op}7{addr}"
    else:
        r2 = f"{int(r2):#01x}"[2:]
        code = f"{op}00000{r1}{r2}"
        
    return code

def token_lable_or_val(token,labels,register,line_number,line):
    code = []
    try: 
        if (token[0] == '-'):
            token = int(token[1:])
            code.append(generate_machine_code(Opcode.LOADIM,register,None,token))
            code.append(generate_machine_code(Opcode.NOT,register,register,token))
            code.append(generate_machine_code(Opcode.LOADIM,Registers.BR,None,1))
            code.append(generate_machine_code(Opcode.ADD,register,Registers.BR))
        elif (token[0] == '~'):
            token = int(token[1:])
            code.append(generate_machine_code(Opcode.LOADIM,register,None,token))
            code.append(generate_machine_code(Opcode.NOT,register,register,token))
        else:    
            token = int(token)
            code.append(generate_machine_code(Opcode.LOADIM,register,None,token))
        return code
    except Exception:
        pass
    if token in labels:
        code.append(generate_machine_code(Opcode.LOAD,register,None,addr=labels.index(token)))
    elif (token[0] == '-' and token[1:] in labels):
        code.append(generate_machine_code(Opcode.LOAD,Registers.G6,None,addr=labels.index(token[1:])))
        code.append(generate_machine_code(Opcode.LOADIM,register,None,0))
        code.append(generate_machine_code(Opcode.SUB,register,Registers.G6))
    elif (token[0] == '~' and token[1:] in labels):
        code.append(generate_machine_code(Opcode.LOAD,Registers.G6,None,addr=labels.index(token[1:])))
        code.append(generate_machine_code(Opcode.NOT,register,Registers.G6))
    else:
        raise ValueError(f"{line}\nIncorrect expresion on line {line_number}")

    return code
        


            
def count_expresion(expression:str,labels,line,line_number = 0):
    code = []   
    tree = [[[ [[i.strip().rstrip() for i in ili.split("&")] for ili in div.split("|")]  for div in mul.split("/")] for mul in plus.split("*")] for plus in expression.split("+")]
    print(tree)
    code.append(generate_machine_code(Opcode.LOADIM,Registers.G1,None,0))
    for pls in tree:
        code.append(generate_machine_code(Opcode.LOADIM,Registers.G2,None,1))
        for mul in pls:
          for j in range(len(mul)):
             div = mul[j]   
             code.append(generate_machine_code(Opcode.LOADIM,Registers.G3,None,0))
             for ili in div:
                 code.append(generate_machine_code(Opcode.LOADIM,Registers.G4,None,0xFFFFF))
                 for i in ili:
                     code += token_lable_or_val(i,labels,Registers.G5,line_number,line)
                     code.append(generate_machine_code(Opcode.AND,Registers.G4,Registers.G5))
                 code.append(generate_machine_code(Opcode.OR,Registers.G3,Registers.G4))
             if j > 0:
                code.append(generate_machine_code(Opcode.DIV,Registers.G6,Registers.G3))
             else:
                code.append(generate_machine_code(Opcode.MOV,Registers.G6,Registers.G3)) 
          code.append(generate_machine_code(Opcode.MUL,Registers.G2,Registers.G6)) 
        code.append(generate_machine_code(Opcode.ADD,Registers.G1,Registers.G2)) 

    return code


# Это кринж! всё криво, но в задание же просят топорно 
def translate(text):
    lines_temp = text.split(";")
    lines_temp2 = []
    lines = []
    for line in lines_temp:
        if ('{' in line):
            scob = line.split('{')
            for i in range(len(scob)):
                lines_temp2.append(scob[i])
                if (i != len(scob) - 1): lines_temp2[-1] += '{'
        else:
            lines_temp2.append(line)
    for line in lines_temp2:
        if ('}' in line):
            scob = line.split('}')
            for i in range(len(scob)):
                lines.append(scob[i])
                if (i != len(scob) - 1): lines.append('}')
        else:
            lines.append(line)
    lines = [i.strip().rstrip() for i in lines if len(i.strip().rstrip()) > 0]
    print(lines)
    line_num = 0
    code = []
    labels = ['input','output']   #резервируем для ввода-вывода  
    type_of_labels = ['I','O']  # char or int
    branch_stack = []
    int_func_present = False
    for line in lines:
        line_num += 1
        symbols = line.split()
        if symbols[0] == 'int':
            name = symbols[1]
            if name in labels:
                 raise ValueError(f"{line}\nRedeclaration on line {line_num}")
            if (len(symbols) > 2):
                    if symbols[2] != '=':
                        raise ValueError(f"{line}\nExpected `=` after {name} on line {line_num}")
                    code += count_expresion(line.split('=')[1],labels,line,line_num)
            labels.append(name)
            type_of_labels.append("int")
            code.append(generate_machine_code(Opcode.STORE,Registers.G1,None,addr=len(labels) - 1))
        elif symbols[0] == 'string':
            if (len(symbols) > 2):
              if symbols[2] != '=':
                        raise ValueError(f"{line}\nExpected `=` after {name} on line {line_num}")
            else:
                raise ValueError(f"{line}\nExpected declaration after {name} on line {line_num}")
            name = symbols[1]
            if name in labels:
                 raise ValueError(f"{line}\nRedeclaration on line {line_num}")
            
            raw_string = symbols[3].split("'")
            if (len(raw_string) < 3):
                raise ValueError(f"{line}\nInvalid expresion on line {line_num}")
            
            lenght = int(raw_string[0])
            val = bytes(raw_string[1],"utf-8")
            labels.append(name)
            type_of_labels.append("char")
            code.append(generate_machine_code(Opcode.LOADIM,Registers.BR,None,lenght))
            code.append(generate_machine_code(Opcode.STORE,Registers.BR,None,addr=len(labels)-1))
            for i in range(lenght):
                labels.append(name)
                type_of_labels.append("char")
                if (len(val) > i): 
                 code.append(generate_machine_code(Opcode.LOADIM,Registers.BR,None,val[i]))
                else:
                 code.append(generate_machine_code(Opcode.LOADIM,Registers.BR,None,0))
                code.append(generate_machine_code(Opcode.STORE,Registers.BR,None,addr=len(labels)-1))  
        elif symbols[0] in labels:
             if (len(symbols) < 3 or not '=' in line):
                  raise ValueError(f"{line}\nIncorrect expresion on line {line_num}")
             code += count_expresion(line.split('=')[1],labels,line,line_num)
             code.append(generate_machine_code(Opcode.STORE,Registers.G1,None,addr=labels.index(symbols[0])))
        elif symbols[0] == 'if' or symbols[0] == 'while':
             operands = ['==','<']
             if symbols[-1] != '{':
                    raise ValueError(f"{line}\nExpected {"{"} on line {line_num}")
             if symbols[1] != '(':
                    raise ValueError(f"{line}\nExpected ( on line {line_num}")
             if symbols[-2] != ')':
                    raise ValueError(f"{line}\nExpected ) on line {line_num}")
             for operand in operands:
                 if operand in line:
                     break

             left_expression, right_expression = line.split('(')[1].split(')')[0].rstrip().strip().split(operand)
             code += count_expresion(right_expression,labels,line,line_num)
             code.append(generate_machine_code(Opcode.MOV,Registers.A,Registers.G1))
             code += count_expresion(left_expression,labels,line,line_num)
             if (operand == '=='): 
                 code.append(generate_machine_code(Opcode.JMPE,Registers.G1,Registers.A))  
             else:
                 code.append(generate_machine_code(Opcode.JMPL,Registers.G1,Registers.A)) 
             # Добавляем jmp без определённого адресса чтобы потом его переопределить! 
             code.append(generate_machine_code(Opcode.JMP,addr=0xFFFFFF))
             branch_stack.append((symbols[0],len(code) - 1))
        elif symbols[0] == '}':
             if (len(branch_stack) == 0): 
                raise ValueError(f"{line}\nInvalid syntax")
             brench_type,code_addr = branch_stack.pop(0)
             if (brench_type == "while"):
                 # Делаем зацикливание, прыжок на проверку условия цикла
                 code.append(generate_machine_code(Opcode.JMP,addr=code_addr-1))
             code[code_addr] = generate_machine_code(Opcode.JMP,addr=len(code))
        elif symbols[0] == "print":
            if (len(symbols) != 4):
                raise ValueError(f"{line}\nIncorrect expresion on line {line_num}")
            to_print = symbols[2]
            if (not to_print in labels):
                raise ValueError(f"{line}\nNo such string declared line {line_num}")
            if type_of_labels[labels.index(to_print)] == 'int':
                pass
                #TODO добавить возможность выводить числа
            elif type_of_labels[labels.index(to_print)] == 'char':
                code.append(generate_machine_code(Opcode.LOAD,Registers.G1,None,addr=labels.index(to_print)))
                code.append(generate_machine_code(Opcode.LOADIM,Registers.G2,None,val=labels.index(to_print)))
                code.append(generate_machine_code(Opcode.LOADIM,Registers.G3,None,val=1))
                # Счётчик в BR 
                code.append(generate_machine_code(Opcode.LOADIM,Registers.BR,None,val=0))
                #while (BR < G1)
                code.append(generate_machine_code(Opcode.JMPL,Registers.BR,Registers.G1))
                code.append(generate_machine_code(Opcode.JMP,addr=len(code)+6))
                #BR++
                code.append(generate_machine_code(Opcode.ADD,Registers.BR,Registers.G3))
                code.append(generate_machine_code(Opcode.ADD,Registers.G2,Registers.BR))
                code.append(generate_machine_code(Opcode.LOAD,Registers.G4,Registers.G2))
                code.append(generate_machine_code(Opcode.STORE,Registers.G4,None,addr=1))
                code.append(generate_machine_code(Opcode.JMP,addr=len(code)-6))
            else:
                raise ValueError(f"{line}\nYou trying to use IO port as an argument!{line_num}")
        elif symbols[0] == 'interruption':
            code.append(generate_machine_code(Opcode.HALT))
            code.append(generate_machine_code(Opcode.LOADIM,Registers.INT,None,val = len(code)))
            int_func_present = True
    if int_func_present:    
       code.append(generate_machine_code(Opcode.MOV,Registers.PC,Registers.INTPC))
    else:
       code.append(generate_machine_code(Opcode.HALT))
        
            
    return code    

             

            

if __name__ == "__main__":
    print("TRANSLATING!")
    program = add_spaces(read_file("test1.alg"))
    #print(program)
    
    code = translate(program)
    for c in range(len(code)):
        print(c,code[c])