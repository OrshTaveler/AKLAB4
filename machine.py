import sys
from isa import machine_to_opcode,Registers,Opcode
from translator import get_code


data_ofset = 0
memory = [
    # Data segment
    # 0 (lable1):val1
    # 1 (lable2):val2
    # ....
    # n-1 (lablen):valn
    # -------------------------
    # Program segment
    # ...
]

operands = {
    "imval": 0,
    "r1": 0,
    "r2": 0,
    "addr": 0,
}

ALUL = 0
ALUR = 0
N = 0
Z = 1
BUFFER = 0
STOP = 0
INPUT = []
IRQ = 0

def reset_global():
    global ALUL 
    global ALUR 
    global N 
    global Z  
    global BUFFER  
    global STOP  
    global INPUT  
    global IRQ  
    global CLCK
    global memory
    global data_ofset
    global registers
    global signals

    ALUL = 0
    ALUR = 0
    N = 0
    Z = 1
    BUFFER = 0
    STOP = 0
    INPUT = []
    IRQ = 0
    CLCK = 0
    memory = []
    data_ofset = 0

    for reg in registers:
        registers[reg] = 0x0
        
    signals = {
    "regs_latchs": [],
    "s_alur": 0,
    "s_alul": 0,
    "alu_op": 0,
    "alur_latch": 0,
    "alul_latch": 0,
    "ar_latch": 0,
    "s_dst": 0,
    "res_latch": 0,
    "write": 0,
    "read": 0,
}




# registers values
registers = {
    Registers.G1: 0x0,
    Registers.G2: 0x0,
    Registers.G3: 0x0,
    Registers.G4: 0x0,
    Registers.G5: 0x0,
    Registers.G6: 0x0,
    Registers.PC: 0x0,
    Registers.INT: 0x0,
    Registers.INTPC: 0x0,
    Registers.AR: 0x0,
    Registers.B: 0x0,
    Registers.A: 0x0,
    Registers.BR: 0x0,
}


signals = {
    "regs_latchs": [],
    "s_alur": 0,
    "s_alul": 0,
    "alu_op": 0,
    "alur_latch": 0,
    "alul_latch": 0,
    "ar_latch": 0,
    "s_dst": 0,
    "res_latch": 0,
    "write": 0,
    "read": 0,
}
#    ALU CODES
#    0: "pass",
#    1: '+',
#    2: '-',
#    3: '*',
#    4: '/',
#    5: '|',
#    6: '&'
alu_codes = {
    Opcode.ADD: 1,
    Opcode.SUB: 2,
    Opcode.MUL: 3,
    Opcode.DIV: 4,
    Opcode.OR: 5,
    Opcode.AND: 6,
    Opcode.NOT: 7,
    Opcode.JMPL: 2,
    Opcode.JMPE: 2,
    Opcode.JNE: 2,
}

CLCK = 0
buffer = 0
irq = 0


def alu(alur, alul, code):
    global Z
    global N

    if type(alur) is str:
        alur = int(alur)
    if type(alul) is str:
        alul = int(alul)

    if alur == 1048575:
        alur = -1
    if alul == 1048575:
        alul = -1

    if code == 1:
        res = alur + alul
    elif code == 2:
        res = alur - alul
    elif code == 3:
        res = alul * alur
    elif code == 4:
        res = (alur - alur % alul) // alul
    elif code == 5:
        res = alur | alul
    elif code == 6:
        res = alul & alur
    elif code == 0:
        return alur
    elif code == 7:
        res = ~alur

    if res == 0:
        Z = 1
        N = 0
    elif res < 0:
        N = 1
        Z = 0
    else:
        N = 0
        Z = 0

    return res


# Генерируем набор сигналов на каждый из машинных циклов
# Машинные циклы:
# Instruction decode (не будет сигналов потому как будет считать, что это делается по волшебству)
# Operand fetch
# Memory
# Write Back
def decode_instruction(instruction: int):
    global STOP

    op = instruction[0]
    mode = bin(int(instruction[1], 16))[2:]
    while len(mode) < 4:
        mode = "0" + mode
    mode_code = [int(i) for i in mode]
    mach_cicles = {
        "OF": {k: signals[k] for k in signals},
        "EX": {k: signals[k] for k in signals},
        "MM": {k: signals[k] for k in signals},
        "WB": {k: signals[k] for k in signals},
    }
    # Проверяем есть ли загрузка/чтение mode_code[0] == 1
    if mode_code[0] == 1:
        # Проверка на загрузку imval
        if mode_code[2] + mode_code[3] == 0:
            imval = instruction[2:7]
            r1 = int(instruction[7], 16)
            mach_cicles["OF"]["s_alur"] = 0xB  # code for imval
            mach_cicles["OF"]["alur_latch"] = 1

            mach_cicles["EX"]["s_dst"] = 0xB  # code for res from ALU
            mach_cicles["EX"]["res_latch"] = 1
            mach_cicles["EX"]["regs_latchs"] = [r1]
            operands["imval"] = int(imval, 16)
            return mach_cicles

        # Проверяем загружаем или читаем:
        if mode_code[1] == 1:  # загружаем
            if mode_code[3] == 1:
                r1 = int(instruction[-2], 16)
                r2 = int(instruction[-1], 16)
                mach_cicles["OF"]["s_dst"] = r1  # code for res from register
                mach_cicles["OF"]["res_latch"] = 1
                mach_cicles["OF"]["ar_latch"] = 1

                mach_cicles["EX"]["s_dst"] = r2
                mach_cicles["EX"]["res_latch"] = 1

                mach_cicles["MM"]["write"] = 1
            else:
                r1 = int(instruction[-1], 16)
                addr = instruction[2:7]
                mach_cicles["OF"]["s_alur"] = 0xB  # imval code
                mach_cicles["OF"]["alur_latch"] = 1
                mach_cicles["OF"]["s_dst"] = 0xB  # code for res from ALU
                mach_cicles["OF"]["res_latch"] = 1
                mach_cicles["OF"]["ar_latch"] = 1
                operands["imval"] = int(addr, 16)

                mach_cicles["EX"]["s_dst"] = r1
                mach_cicles["EX"]["res_latch"] = 1

                mach_cicles["MM"]["write"] = 1
        else:  # читаем
            if mode_code[3] == 1:
                r1 = int(instruction[-2], 16)
                r2 = int(instruction[-1], 16)
                mach_cicles["OF"]["s_dst"] = r1  # code for res from register
                mach_cicles["OF"]["res_latch"] = 1
                mach_cicles["OF"]["ar_latch"] = 1

                mach_cicles["MM"]["read"] = 1
                mach_cicles["MM"]["s_dst"] = 0xC  # code for res from memory
                mach_cicles["MM"]["res_latch"] = 1

                mach_cicles["WB"]["regs_latchs"] = [r2]
            else:
                r1 = int(instruction[-1], 16)
                addr = instruction[2:7]
                mach_cicles["OF"]["s_alur"] = 0xB  # imval code
                mach_cicles["OF"]["alur_latch"] = 1
                mach_cicles["OF"]["s_dst"] = 0xB  # code for res from ALU
                mach_cicles["OF"]["res_latch"] = 1
                mach_cicles["OF"]["ar_latch"] = 1
                operands["imval"] = int(addr, 16)

                mach_cicles["MM"]["ar_latch"] = 0
                mach_cicles["MM"]["read"] = 1
                mach_cicles["MM"]["s_dst"] = 0xC  # code for res from memory
                mach_cicles["MM"]["res_latch"] = 1

                mach_cicles["WB"]["regs_latchs"] = [r1]
    else:
        op_name = machine_to_opcode[int(op, 16)]
        if op_name == Opcode.JMP:
            imval = instruction[2:8]
            mach_cicles["OF"]["s_alur"] = 0xB  # imval code
            mach_cicles["OF"]["alur_latch"] = 1
            mach_cicles["OF"]["s_dst"] = 0xB  # code for res from ALU
            mach_cicles["OF"]["res_latch"] = 1
            operands["imval"] = int(imval, 16) - 1

            mach_cicles["WB"]["regs_latchs"] = [Registers.PC]
        elif op_name == Opcode.MOV:
            r1 = int(instruction[-2], 16)
            r2 = int(instruction[-1], 16)
            operands["r1"] = r1
            operands["r2"] = r2
            mach_cicles["OF"]["s_dst"] = r2
            mach_cicles["OF"]["res_latch"] = 1

            mach_cicles["EX"]["regs_latchs"] = [r1]

        elif op_name == Opcode.HALT:
            STOP = 1
        else:
            r1 = int(instruction[-2], 16)
            r2 = int(instruction[-1], 16)
            operands["r1"] = r1
            operands["r2"] = r2
            mach_cicles["OF"]["s_alur"] = r1
            mach_cicles["OF"]["s_alul"] = r2
            mach_cicles["OF"]["alur_latch"] = 1
            mach_cicles["OF"]["alul_latch"] = 1

            mach_cicles["EX"]["alu_op"] = alu_codes[op_name]
            mach_cicles["EX"]["s_dst"] = 0xB  # code for res from ALU

            if (
                op_name != Opcode.JMPL
                and op_name != Opcode.JMPE
                and op_name != Opcode.JNE
            ):
                mach_cicles["EX"]["res_latch"] = 1
                mach_cicles["WB"]["regs_latchs"] = [r1]
            else:
                mach_cicles["EX"]["res_latch"] = 0

    return mach_cicles


def control_unit(irq):
    global CLCK
    global IRQ
    
    instruction = memory[registers[Registers.PC] + data_ofset]
    mach_cicles = decode_instruction(instruction)
    op_name = machine_to_opcode[int(instruction[0], 16)]

    state = {
        "inst": instruction,
        "op": op_name,
    }

    # print(state)
    if instruction == "e00000ae":
        IRQ = 0

    if STOP == 1:
        return state
    for cicle in mach_cicles:
        CLCK += 1
        data_path(mach_cicles[cicle])

    if not irq:
        registers[Registers.PC] += 1
        if op_name == Opcode.JMPL and N == 1:
            registers[Registers.PC] += 1
        elif op_name == Opcode.JMPE and Z == 1:
            registers[Registers.PC] += 1
        elif op_name == Opcode.JNE and Z == 0:
            registers[Registers.PC] += 1

    else:
        if IRQ == 1:
            registers[Registers.INTPC] = registers[Registers.PC]
            registers[Registers.PC] = registers[Registers.INT]
    # print (CLCK,instruction,op_name,memory[1])
    return state


def data_path(signals: dict):
    global BUFFER
    global ALUL
    global ALUR

    if signals["s_alur"] == 0xB:
        if signals["alur_latch"] == 1:
            ALUR = operands["imval"]
    else:
        if signals["alur_latch"] == 1:
            ALUR = registers[operands["r1"]]

    if signals["alul_latch"] == 1:
        ALUL = registers[operands["r2"]]

    alu_res = alu(ALUR, ALUL, signals["alu_op"])
    if signals["res_latch"] == 1:
        if signals["s_dst"] == 0xB:
            BUFFER = alu_res
        elif signals["s_dst"] == 0xC:
            if signals["read"] == 1:
                BUFFER = memory[registers[Registers.AR]]
        else:
            BUFFER = registers[signals["s_dst"]]
    for s in signals["regs_latchs"]:
        registers[s] = BUFFER

    if signals["ar_latch"] == 1:
        registers[Registers.AR] = BUFFER
    if signals["write"] == 1:
        memory[registers[Registers.AR]] = BUFFER


def load_program(code):
    for _ in range(data_ofset):
        memory.append("0")
    for c in code:
        memory.append(c)

def main(code_file, inpt_file):
    global IRQ
    global data_ofset
    reset_global()

    code, labels = get_code(code_file)
    inpt_file_name = inpt_file
    with open(inpt_file_name, "r") as inpt:
        for i in inpt.readlines():
            s = i.split()
            if len(s) > 1:
                INPUT.append((int(s[0]), s[1]))
            else:
                INPUT.append((int(s[0]), " "))

    data_ofset = len(labels)
    load_program(code)

    time_cnt = 0
    journal = ""
    prev_out = memory[1]
    output = ""
    irq = False
    while STOP == 0:
        time_cnt += 1
        inpt = None
        for i in INPUT:
            if i[0] == time_cnt:
                irq = True
                IRQ = 1
                inpt = i[1]
                memory[0] = ord(i[1])

        control_unit(irq)
        if inpt:
            journal += f'INPUT: "{inpt}"\n'
        if memory[1] != -1:
            prev_out = int(memory[1])
            if prev_out != 0:
                output += chr(int(prev_out))
                journal += f'OUTPUT: "{chr(prev_out)}"\n'
            memory[1] = -1
        irq = False
        inpt = None

    for i in range(8):
        journal += f"{Registers(i).name}: {hex(int(registers[i]))}\n"
    journal += "----------------------\n"
    journal += "Memory dump:\n"
    for i in range(len(memory)):
        try:
            journal += f"{i}. {hex(int(memory[i]))}\n"
        except ValueError:
            journal += f"{i}. {hex(int(memory[i], 16))}\n"
    journal += "----------------------\n"
    journal += f"TOTAL OUTPUT:\n{output}"
    with open("log.txt", "w") as res:
        res.write(journal)
    with open("output.txt", "w") as res:
        res.write(output)

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
