from abc import ABC, abstractmethod
import re
import logging 

import olaf2

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class Oasm(ABC):
    regex = re.compile("")
    assembly = ""
    @abstractmethod
    def parse(self):
        pass


class OasmData(Oasm):
    regex = re.compile(
        r"(char|int)\s(\w+)\[(\d+)\s*\;{0,1}.*")

    def __init__(self, var_type, name, length, address):
        self.var_type = var_type
        self.name = name

        if length:
            if type(length) is str:
                self.length = int(length, 16) if length.startswith("0x") else int(length)
            elif type(length) is int:
                self.length = length
            else:
                raise SyntaxError(f"bad legnth type {type(length)}")
        elif self.var_type == "int":
            self.length = 1
        # self.assembly = "0 " * self.length
        self.address = address

    def parse(self):
        logger.debug(f"parsing data. {self}")
        return self.assembly
        
    def __len__(self) -> int:
        return self.length

    def __str__(self):
        return f"{self.var_type} {self.name}[{self.length}] @ {hex(self.address)}"
    
    def __repr__(self):
        return f"<OasmData {str(self)}>"

            
class OasmRoData(Oasm):
    regex = re.compile(
        r"(char|int)\s(\w+)(?:\[(\d*)\])?\s=\s\"(.+)\"\s*\;{0,1}.*")

    def __init__(self, var_type, name, length, value, address):
        self.var_type = var_type
        self.name = name
        self.value = value

        if length:
            self.length = length
        elif self.var_type == "int":
            self.length = 1
        else:
            self.length = len(self.value) + 1
        self.address = address

    def parse(self):
        logger.debug(f"parsing rodata.")
        if not (self.var_type and self.name and self.value):
            raise SyntaxError("invalid data")
        self.assembly = ""
        if self.var_type == "int":
            assert int(self.value, base=10 if not self.value.startswith("0x") else 16) <= 0xff
            self.assembly += hex(int(self.value, base=10 if not self.value.startswith("0x") else 16))[2:]
        elif self.var_type == "char": 
            for char in self.value:
                self.assembly += f"{hex(ord(char))[2:]} "
            self.assembly += "0"
        else:
            raise SyntaxError("invalid type")
        self.assembly += " "
        logger.debug(f"data found! {self} is ({self.assembly})")
        return self.assembly

    def __str__(self):
        return f"{self.var_type} {self.name}[{self.length}] = {self.value} @ {hex(self.address)}"
        
    def __repr__(self):
        return f"<OasmRoData {str(self)}>"

    def __len__(self) -> int:
        return self.length


class OasmText(Oasm):
    regex = re.compile(
        r"^\s*\t*(\w{2,4})[^\S\r\n]?(?:(\$?\'?\w+\'?)){0,}(?:,[^\S\r\n])?([\S\']+){0,}\s*\;{0,1}.*$")
    
    # commands that the word comes after the opcode represents 8 bits long data
    _opcodes_uses_2nd_param_as_data = [
        olaf2.Opcodes.OUT, 
        olaf2.Opcodes.JMP,
        olaf2.Opcodes.JEQ,
        olaf2.Opcodes.JNE,
        olaf2.Opcodes.JBT,
        olaf2.Opcodes.JST,
        olaf2.Opcodes.JBE,
        olaf2.Opcodes.JLE,
    ] 

    def __init__(self, line=0, opcode=None, source=None, destination=None, functions=dict(), variables=dict()):
        self.line = line
        try:
            self.opcode = olaf2.Opcodes[opcode]
        except KeyError:
            raise SyntaxError(f"opcode \"{opcode}\" not found")
        self.source = source
        self.destination = destination
        self.functions = functions
        self.variables = variables

    def parse(self):
        logger.debug(f"parsing code. ")
        instruction = 0
        if self.opcode:
            instruction += self.opcode.value
        if self.source:
            if self.opcode in self._opcodes_uses_2nd_param_as_data and not self.destination:
                self.destination = self.source
                self.source = "0"
            if self.source.lower().startswith("0x"):
                instruction += int(self.source, 16) << olaf2._SIZEOF_OPCODE 
            elif (self.source.startswith("'") and self.source.endswith("'")) or \
                (self.source.startswith('"') and self.source.endswith('"')):
                instruction += ord(self.source[1]) << (olaf2._SIZEOF_OPCODE + olaf2._SIZEOF_SOURCE)
            elif self.source.startswith("#"):
                instruction += self.variables[self.source[1:]].address << (olaf2._SIZEOF_OPCODE + olaf2._SIZEOF_SOURCE)
            elif self.source.startswith("$"):
                instruction += olaf2.Registers[self.source[1:]].value << olaf2._SIZEOF_OPCODE
            else:
                instruction += int(self.source) << olaf2._SIZEOF_OPCODE   
        if self.destination:
            if self.destination.startswith("0x"):
                instruction += int(self.destination, 16) << (olaf2._SIZEOF_OPCODE + olaf2._SIZEOF_SOURCE)
            elif self.destination.startswith("@"):
                instruction += self.functions[self.destination[1:]] << (olaf2._SIZEOF_OPCODE + olaf2._SIZEOF_SOURCE)
            elif (self.destination.startswith("'") and self.destination.endswith("'")) or \
                (self.destination.startswith('"') and self.destination.endswith('"')):
                instruction += ord(self.destination[1]) << (olaf2._SIZEOF_OPCODE + olaf2._SIZEOF_SOURCE)
            elif self.destination.startswith("#"):
                instruction += self.variables[self.destination[1:]].address << (olaf2._SIZEOF_OPCODE + olaf2._SIZEOF_SOURCE)
            elif self.destination.startswith("$"):
                instruction += olaf2.Registers[self.destination[1:]].value << (olaf2._SIZEOF_OPCODE + olaf2._SIZEOF_SOURCE)
            else:
                instruction += int(self.destination) << (olaf2._SIZEOF_OPCODE + olaf2._SIZEOF_SOURCE)
        logger.debug(f"instruction found! {self} is {hex(instruction)} ({instruction})")
        self.assembly += f"{hex(instruction)[2:]} "
        return self.assembly

    def __str__(self):
        return f"opcode={self.opcode}, source={self.source}, destination={self.destination} @ {hex(self.line)}"

    def __repr__(self):
        return f"<OasmText: {self.opcode} {self.source}, {self.destination} @ {hex(self.line)}>"


segments = {
    ".rodata": OasmRoData,
    ".data": OasmData,
    ".text": OasmText,
}