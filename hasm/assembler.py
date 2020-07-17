from typing import List

from hasm.types import Command
from hasm.code import Code
from hasm.symboltable import SymbolTable
from hasm.parser import Parser


class Assembler:
    def __init__(self, filepath=str):
        self.parser = Parser(filepath)
        self.code = Code()
        self.symbol_table = SymbolTable()
        self.buffer: List[str] = []

    def assemble(self) -> List[str]:
        # First pass to extract labels
        self.process_l_commands()

        while self.parser.has_more_commands():
            self.parser.advance()
            if self.parser.current_command_type == Command.A:
                self.process_a_command()
            elif self.parser.current_command_type == Command.C:
                self.process_c_command()

    def process_a_command(self):
        symbol = self.parser.symbol
        if symbol.isnumeric():
            addr = int(symbol)
            self.buffer.append(f"{addr:016b}")
        else:
            addr = self.symbol_table.get_addr(symbol)
            if addr is None:
                addr = self.symbol_table.add_variable(symbol)
            self.buffer.append(f"{addr:016b}")

    def process_c_command(self):
        dest = self.code.dest(self.parser.dest)
        comp = self.code.comp(self.parser.comp)
        jump = self.code.jump(self.parser.jump)
        self.buffer.append(f"111{comp}{dest}{jump}")

    def process_l_commands(self):
        while self.parser.has_more_commands():
            self.parser.advance()
            if self.parser.current_command_type == Command.L:
                symbol = self.parser.symbol
                if self.symbol_table.get_addr(symbol) is None:
                    self.symbol_table.add_entry(symbol, self.parser.instruction_counter)
            else:
                # account for non-L instructions to generate
                # proper line address
                self.parser.instruction_counter += 1
        self.parser.reset()
