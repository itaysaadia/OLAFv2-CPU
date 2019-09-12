import logging
import re
import sys

import olaf2

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.debug("olaf assembler starting")


class OLAFAssembler:
    """
    This class exports an API to assemble olaf programs to logisim readable memory buffer
    """

    def __init__(self, oasm_file):
        """
        :param oasm_file: the filename (or opened file object) to the assembler file
        """
        try:
            self.oasm_file = open(oasm_file, "r") if type(
                oasm_file) is str else oasm_file
        except FileNotFoundError:
            logger.error(f"Oasm file {oasm_file} not found")
        self.should_print = True
        self._regex_line_of_code = re.compile(
            r"(^\w{2,4})(?:\s(\$?\w)+(?:,\s)(\S+))?$")
        self._regex_line_of_data = re.compile(
            r'''(?:str|int)\s(\w+)\s=\s(.+)''')

        self._tokenized_oasm = {".text": list(), ".data": list()}
        self._vars = dict()
        self.assembly = "v2.0 raw"

    def assemble(self, output_file=None, should_print=False) -> str:
        """
        :param output_file: (optional) output file for the buffer of disassembly
        :param should_print: (optional) if True, prints the assembly buffer in the end 

        start the assembling process.
        prints is should_print is True.
        writes to a file if output_file is set.
        returns a string buffer of ascii-printable "assembly"
        """

        try:
            self._tokenize()
        except SyntaxError as e:
            logger.error("the oasm file is incorrect")
            raise e
        self._parse_data()
        self._parse_text()
        if self.should_print:
            print(self.assembly)
        if output_file:
            try:
                self.output_file = open(output_file, "w") if type(
                    output_file) is str else output_file
            except:
                logger.error(f"Output file {output_file} could not be opened")
            try:
                self.output_file.write(self.assembly)
            except:
                logger.warn("could not write to a file")
        return self.assembly

    def _tokenize(self):
        """
        this function parse the file and splits the program to a dictionary of text and data.
        example:
        self._tokenized_oasm = {
            ".text": [
                ("MOV", "$x", 0),      # move 0 to the var x
                ("PUSH", "RA", None),  # None if one or more arguments are not necessary
            ]
            ".data": {
                "x": (0, 8),  # (address of x in ram, size of var)
                "y": (8, 8),  # (address of x in ram, size of var)
            }
        }
        """
        logger.debug(f"started parsing {self.oasm_file.name}")

        current_segment = None
        for line_number, line in enumerate(self.oasm_file.readlines()):
            line = line.rstrip().strip()
            if not line:
                continue
            logger.debug(f"reading line {line_number}: {line}")
            line_number += 1  # first line of the file is 1
            if line.startswith("."):  # this dot represents segment
                segment = line
                logger.debug(f"found segment {segment}")
                if segment not in olaf2.SEGMENTS:
                    raise SyntaxError(
                        f"invalid segment name {segment} in line {line_number}")
                try:
                    current_segment = segment
                except IndexError:
                    raise SyntaxError(
                        f"error locating segment {segment} in line {line_number}")
            else:
                if current_segment is None:
                    raise SyntaxError(
                        "the oasm should start with segment name")
                elif current_segment == ".text":
                    if not self._regex_line_of_code.match(line):
                        raise SyntaxError(
                            f"invalid length of line in line {line_number} of {self.oasm_file.name}: {line}")
                    self._tokenized_oasm[".text"].append(
                        self._regex_line_of_code.search(line).groups()
                    )
                    logger.debug(f"added {self._regex_line_of_code.search(line).groups()}")
                elif current_segment == ".data":
                    if not self._regex_line_of_data.match(line):
                        raise SyntaxError(
                            f"invalid line in {line_number} of {self.oasm_file.name}: {line}")
                    self._tokenized_oasm[".data"].append(
                        self._regex_line_of_data.search(line).groups()
                    )
                    logger.debug(f"added {self._regex_line_of_data.search(line).groups()}")
                else:
                    raise SyntaxError(f"Unknown segment {current_segment}")

    def _parse_data(self):
        logger.debug("parsing data")

    def _parse_text(self):
       for i, line in enumerate(self._tokenized_oasm[".text"]):
            instruction, source, destination = line
            logger.debug(f"parsing code. instruction={instruction}, source={source}, destination={destination}")
            if i % 8 == 0:
                self.assembly += "\n"
            try:
                opcode = olaf2.OPCODES[instruction.upper()]
            except IndexError:
                raise SyntaxError(f"opcode \"{instruction}\" not found")
            if source:
                if source.startswith("0x"):
                    opcode += int(source, 16) << olaf2._SIZEOF_OPCODE 
                else:
                    opcode += int(source) << olaf2._SIZEOF_OPCODE 
            if destination:
                if destination.startswith("0x"):
                    opcode += int(destination, 16) << (olaf2._SIZEOF_OPCODE + olaf2._SIZEOF_SOURCE)
                else:
                    opcode += int(destination) << (olaf2._SIZEOF_OPCODE + olaf2._SIZEOF_SOURCE)
            logger.debug(f"opcode found! {line} is {hex(opcode)}")
            self.assembly += f"{hex(opcode)[2:]} "

    def _replace_var_names_with_offsets(self, var_name: str):
        pass


if __name__ == "__main__":
    if 3 != len(sys.argv):
        logger.error(f"Usage {sys.argv[0]} OASM_FILE")
        exit(-1)
    assembler = OLAFAssembler(sys.argv[1])
    assembler.assemble(output_file=sys.argv[2])
