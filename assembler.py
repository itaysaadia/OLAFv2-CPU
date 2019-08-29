import olaf2
import logging

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logging.debug("olaf assembler starting")


class OLAFAssembler:
    """
    This class exports an API to assemble olaf programs to logisim readable memory buffer
    """

    def __init__(self, oasm_file):
        """
        :param oasm_file: the filename (or opened file object) to the assembler file
        """
        try:
            self.oasm_file = open(oasm_file, "r") if type(oasm_file) is str else oasm_file
        except FileNotFoundError:
            logger.error(f"Oasm file {oasm_file} not found")
        self.should_print = True

        self._tokenized_oasm = {".text": list(), ".data": list()}
        self._vars = dict()
        self.assembly = str()

    def disassemble(self, output_file=None, should_print=True) -> str:
        """
        :param output_file: (optional) output file for the buffer of disassembly
        :param should_print: (optional) if True, prints the assembly buffer in the end 

        start the disassembly process.
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
                self.output_file = open(output_file, "w") if type(output_file) is str else output_file
            except:
                logger.error(f"Output file {output_file} could not be opened")
            try:
                self.output_file.write(self.assembly)
            except: 
                logger.warn("could not write to a file")
        return self.assembly

    def _tokenize(self):
        logger.debug(f"started parsing {self.oasm_file}")

        current_segment = None
        for line in self.oasm_file.readlines():
            if line.startswith("."):  # this dot represents segment
                segment = line.strip()
                logger.debug(f"found segment {segment}")
                if segment not in olaf2.SEGMENTS:
                    raise SyntaxError(f"invalid segment name {segment}")
                try:
                    current_segment = self._tokenized_oasm[segment]
                except IndexError:
                    raise SyntaxError(f"error locating segment {segment}")
            else:
                if current_segment is None:
                    raise SyntaxError(
                        "the oasm should start with segment name")

    def _parse_data(self):
        pass

    def _parse_text(self):
        pass

    def _replace_var_names_with_offsets(self, var_name: str):
        pass
