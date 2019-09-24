from enum import Enum

class Opcodes(Enum):
    NOP  = 0X00 # do nothing

    # arithmetics
    ADD  = 0x01  # addition
    SUB  = 0x02  # substraction
    MUL  = 0x03  # multiplication
    DIV  = 0x04  # division
    MOD  = 0x05  # modulo

    # bitwise operations
    SHL  = 0x06  # shift left
    SHR  = 0x07  # shift right
    XOR  = 0x08  # bitwise xor
    NOT  = 0x09  # bitwise not
    AND  = 0x0a  # bitwise and
    OR   = 0x0b  # bitwise and

    # relations
    TEST = 0x0c

    # control flow
    JMP  = 0x11  # jump every time
    JEQ  = 0x12  # jump if equals
    JNE  = 0x13  # jump if not equals
    JBT  = 0x14  # jump if bigger
    JST  = 0x15  # jump if smaller
    JBE  = 0x16  # jump if bigger of equals
    JLE  = 0x17  # jump if less or equals

    # user interation
    GET  = 0x18  # get user data
    OUT  = 0x19  # print out data

    # registers operations
    MOV  = 0x1a  # move a value to a register

    # stack
    CALL = 0x1b  # jmp and store IP on the stack
    PUSH = 0x1c  # push a value to the stack
    POP  = 0x1d  # pop a value from the stack 
    RET  = 0x1e  # take the value from the stack and jump to it

    # computer
    RST  = 0x1f  # restart the computer


class Registers(Enum):
    RA  = 0
    RB  = 1
    RC  = 2
    RD  = 3
    RDI = 4
    RSI = 5
    IP  = 6
    SP  = 7

_SIZEOF_OPCODE = 5
_SIZEOF_SOURCE = 3
_SIZEOF_DEST   = 8