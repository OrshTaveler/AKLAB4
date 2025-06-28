from enum import Enum,IntEnum


class Opcode(Enum):
    JMPE    = 'jmpe' # jump if r1 == r2 
    JMP     = 'jmp'  # jump anyway   
    JMPL    = 'jmpl' # jump if r1 < r2
    AND     = 'and'
    NOT     = 'not'
    MUL     = 'mul'  
    OR      = 'or'
    SUB     = 'sub'
    ADD     = 'add'
    MOV     = 'mov'
    DIV     = 'div'
    LOAD    = 'ld'
    STORE   = 'sv'
    LOADIM  = 'ldi'
    HALT    = 'halt'
    JNE     = 'jne'




class Registers(IntEnum):

    INT = 0b1111
    INTPC = 0b1110
    G1 = 0b0000
    G2 = 0b0001
    G3 = 0b0010
    G4 = 0b0011
    G5 = 0b0100
    G6 = 0b0101
    A  = 0b0110
    BR = 0b0111
    B  = 0b1000
    AR = 0b1001
    PC = 0b1010
    

opcode_to_machine = {
    Opcode.JMPE     : 0b1000,
    Opcode.JMP      : 0b1001,
    Opcode.MUL      : 0b1010,
    Opcode.OR       : 0b1011,
    Opcode.SUB      : 0b1100,
    Opcode.ADD      : 0b1101,
    Opcode.MOV      : 0b1110,
    Opcode.DIV      : 0b1111,
    Opcode.LOAD     : 0b0001,
    Opcode.STORE    : 0b0010,
    Opcode.LOADIM   : 0b0011,
    Opcode.JMPL     : 0b0100,
    Opcode.HALT     : 0b0101,
    Opcode.AND      : 0b0110,
    Opcode.NOT      : 0b0111,
    Opcode.JNE      : 0b0000
}
machine_to_opcode = {
    0b1000: Opcode.JMPE,
    0b1001: Opcode.JMP,
    0b1010: Opcode.MUL,
    0b1011: Opcode.OR ,
    0b1100: Opcode.SUB,
    0b1101: Opcode.ADD,
    0b1110: Opcode.MOV,
    0b1111: Opcode.DIV,
    0b0001: Opcode.LOAD,
    0b0010: Opcode.STORE,
    0b0011: Opcode.LOADIM,
    0b0100: Opcode.JMPL,
    0b0101: Opcode.HALT,
    0b0110: Opcode.AND,
    0b0111: Opcode.NOT,
    0b0000: Opcode.JNE
}
#3 38000000  G1 = 0
#4 38000011  G2 = 1
#5 38000002  G3 = 0
#6 38fffff3  G4 = FFFF
#7 380000a4  G5 = A
#8 60000034  
#9 b0000023
#10 e0000052
#11 a0000015
#12 d0000001
#13 2E000020
#14 50000000
