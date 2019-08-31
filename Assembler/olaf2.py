OPCODES = {
    # arithmetics
    "ADD": 0x01,  # addition
    "SUB": 0x02,  # substraction
    "MUL": 0x03,  # multipication
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
    "MOVR": 0x1c,  # move a register to a register

    # stack
    "PUSH": 0x1d,
    "POP": 0x1e,

    # computer
    "RST": 0x1f
}

SEGMENTS = [
    ".data",  # vars etc 
    ".text",  # the code itself
]

_SIZEOF_OPCODE = 5
_SIZEOF_SOURCE = 3
_SIZEOF_DEST   = 8