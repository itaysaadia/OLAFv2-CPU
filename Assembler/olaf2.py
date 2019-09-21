OPCODES = {
    "NOP": 0X00,
    # arithmetics
    "ADD": 0x01,  # addition
    "SUB": 0x02,  # substraction
    "MUL": 0x03,  # multiplication
    "DIV": 0x04,  # division
    "MOD": 0x05,  # modulo

    # bitwise operations
    "SHL": 0x06,  # shift left
    "SHR": 0x07,  # shift right
    "XOR": 0x08,  # bitwise xor
    "NOT": 0x09,  # bitwise not
    "AND": 0x0a,  # bitwise and
    "OR": 0x0b,  # bitwise and

    # relations
    "TEST":  0x0c,  

    # control flow
    "JMP": 0x12,  # jump every time
    "JEQ": 0x13,  # jump if equals
    "JNE": 0x14,  # jump if not equals
    "JBT": 0x15,  # jump if bigger
    "JST": 0x16,  # jump if smaller
    "JBE": 0x17,  # jump if bigger of equals
    "JLE": 0x18,  # jump if less or equals

    # user interation
    "GET": 0x19,  # get user data
    "OUT": 0x1a,  # print out data

    # registers operations
    "MOV": 0x1b,  # move a value to a register

    # stack
    "RET": 0x1c,  # take the value from the stack and jump to it
    "PUSH": 0x1d,  # push a value to the stack
    "POP": 0x1e,  # pop a value from the stack 

    # computer
    "RST": 0x1f,  # restart the computer
}

SEGMENTS = [
    ".data",  # vars etc 
    ".text",  # the code itself
]

_SIZEOF_OPCODE = 5
_SIZEOF_SOURCE = 3
_SIZEOF_DEST   = 8