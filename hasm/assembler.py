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
        parser = self.parser
        code = self.code
        symbol_table = self.symbol_table

        # First pass to extract labels
        while parser.has_more_commands():
            parser.advance()
            if parser.current_command_type == Command.L:
                symbol = parser.symbol
                if symbol_table.get_addr(symbol) is None:
                    symbol_table.add_entry(symbol, parser.instruction_counter)
            else:
                parser.instruction_counter += 1
        parser.reset()

        while parser.has_more_commands():
            parser.advance()
            if parser.current_command_type == Command.A:
                symbol = parser.symbol
                if symbol.isnumeric():
                    addr = int(symbol)
                    self.buffer.append(f"{addr:016b}")
                else:
                    addr = symbol_table.get_addr(symbol)
                    if addr is None:
                        addr = symbol_table.add_variable(symbol)
                    self.buffer.append(f"{addr:016b}")
            elif parser.current_command_type == Command.C:
                dest = code.dest(parser.dest)
                comp = code.comp(parser.comp)
                jump = code.jump(parser.jump)
                if not dest or not comp or not jump:
                    print(parser.line_number, parser.dest, parser.comp, parser.jump)
                self.buffer.append(f"111{comp}{dest}{jump}")
