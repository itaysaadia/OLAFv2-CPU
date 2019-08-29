import struct
import olaf2 
import logging

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logging.debug("olaf assembler starting")

def disassemble(oasm_file) -> dict():
    logger.debug("parsing started")
    oasm_file = open(oasm_file) if type(oasm_file) is str else oasm_file

    disassembly = {".text": list(), ".data": list()}
    current_segment = None
    for line in oasm_file.readlines():
        if line.startswith("."):  # this line represents segment
            segment = line.strip()
            logger.debug(f"found segment {segment}")
            if segment not in olaf2.SEGMENTS:
                raise SyntaxError(f"invalid segment name {segment}")
            try:
                current_segment = disassembly[segment]
            except IndexError:
                raise SyntaxError(f"error locating segment {segment}")
        else:
            if current_segment is None:
                raise SyntaxError("the oasm should start with segment name")


def _parse_text():
    pass


def _disassemble(assembler_prog : dict) -> bytes:
    pass
