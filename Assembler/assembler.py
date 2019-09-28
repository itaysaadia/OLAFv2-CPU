import logging
import re
import sys

import olaf2
import oasm

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

        self._tokenized_oasm = {".text": list(), ".data": list(), ".rodata": list(), "functions": dict()}
        self._vars = dict()
        self.assembly = "v2.0 raw\n0 "

    def assemble(self, output_file=None, should_print=False) -> str:
        """
        :param output_file: (optional) output file for the buffer of disassembly
        :param should_print: (optional) if True, prints the assembly buffer in the end 

        start the assembling process.
        prints is should_print is True.
        writes to a file if output_file is set.
        returns a string buffer of ascii-printable "assembly"
        """

        logger.info(f"started parsing {self.oasm_file.name}")
        try:
            self._tokenize()
        except SyntaxError as e:
            logger.error("the oasm file is incorrect")
            raise e

        for segment in [".rodata", ".data", ".text"]:
            for line in self._tokenized_oasm[segment]:
                self.assembly += line.parse()

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
        self.assembly += "\n"
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
        logger.info("tokenizing")
        opcode_address = 1  # we are adding NOP at the beggining 
        current_segment_handler = oasm.Oasm
        segment = ""
        for line_number, line in enumerate(self.oasm_file.readlines()):
            line = line.rstrip().strip()
            if not line or line.startswith(";"):
                continue
            logger.debug(f"reading line {line_number}: {line}")
            line_number += 1  # first line of the file is 1
            if line.startswith("."):  # this dot represents segment
                segment = line
                logger.debug(f"found segment {segment}")
                if segment not in self._tokenized_oasm.keys():
                    raise SyntaxError(
                        f"invalid segment name {segment} in line {line_number}")
                try:
                    current_segment_handler = oasm.segments[segment]
                except IndexError:
                    raise SyntaxError(
                        f"error locating segment {segment} in line {line_number}")
            else:
                if current_segment_handler is None:
                    raise SyntaxError(
                        "the oasm should start with segment name")
                
                if not current_segment_handler.regex.match(line):
                    raise SyntaxError(
                        f"invalid length of line in line {line_number} of {self.oasm_file.name}: {line}")
                elif segment == ".text":
                    opcode, source, destination = current_segment_handler.regex.search(line).groups()
                    if line.endswith(":"):
                        self._tokenized_oasm["functions"][line[:-1]] = opcode_address
                    else:
                        opcode_address += 1 
                        self._tokenized_oasm[".text"].append(
                            oasm.OasmText(line_number, opcode, source, destination)
                        )
                elif segment in [".rodata", ".data"]:
                    var_type, var_name, var_value = current_segment_handler.regex.search(line).groups()
                    self._tokenized_oasm[".data"].append(
                        current_segment_handler()
                    )
                else:
                    raise SyntaxError(f"Unknown segment {current_segment_handler}")
                logger.debug(f"added {current_segment_handler.regex.search(line).groups()}")
        for i in self._tokenized_oasm[".text"]:
            i.functions = self._tokenized_oasm["functions"] 


if __name__ == "__main__":
    if 3 != len(sys.argv):
        logger.error(f"Usage {sys.argv[0]} OASM_FILE")
        exit(-1)
    assembler = OLAFAssembler(sys.argv[1])
    assembler.assemble(output_file=sys.argv[2])
