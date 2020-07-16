from typing import List

from hasm.types import Command, C_Instruction
from hasm.code import Code
from hasm.symboltable import SymbolTable


class Parser:
    def __init__(self, filepath: str):
        self.filepath = filepath
        self.line_number = 0
        self.file: List[str] = self.load_file(filepath)
        self.current_command_type: Command = None
        self._symbol: str = None
        self._comp: str = None
        self._dest: str = None
        self._jump: str = None
        self.instruction_counter = 0

    def load_file(self, filepath: str) -> List[str]:
        output: List[str] = []
        with open(filepath) as f:
            for line in f.readlines():
                line = self._process_line(line)
                if line:
                    output.append(line)
        return output

    def _process_line(self, line: str) -> str:
        line = line.strip()
        if line.startswith("/") or line == "\n":
            return ""
        for index, char in enumerate(line):
            if char == " ":
                return line[:index]
        return line

    def reset(self):
        self.line_number = 0

    def reset_commands(self):
        self.current_command_type = None
        self._symbol = None
        self._comp = None
        self._dest = None
        self._jump = None

    def has_more_commands(self) -> bool:
        """Returns whether or not there are more commands in the input"""
        return self.line_number < len(self.file)

    def advance(self):
        """Reads the next command from the input and makes it the current command.
        Should be called only if has_more_commands() is true."""
        self.current_command_type = self.command_type()
        if self.current_command_type == Command.A:
            self._symbol = self.parse_a()
        if self.current_command_type == Command.C:
            self._dest, self._comp, self._jump = self.parse_c()
        if self.current_command_type == Command.L:
            self._symbol = self.parse_l()

        self.line_number += 1

    @property
    def current_command(self):
        if self.file:
            return self.file[self.line_number]
        return ""

    def command_type(self) -> Command:
        """Returns the type of the currentcommand:
        A_COMMAND for @Xxx where Xxx is either a symbol or a decimal number
        C_COMMAND for dest=comp;jump
        L_COMMAND(actually, pseudo-command) for (Xxx) where Xxx is a symbol.
        """
        self.reset_commands()
        command = self.current_command
        if command.startswith("@"):
            return Command.A
        elif command.startswith("("):
            return Command.L
        else:
            return Command.C

    @property
    def symbol(self) -> str:
        """Returns the symbol or decimal Xxx of the current command
        @Xxx or (Xxx).
        Should be called only when commandType() is A_COMMAND or L_COMMAND.
        """
        if (
            self.current_command_type == Command.A
            or self.current_command_type == Command.L
        ):
            return self._symbol

    @property
    def dest(self) -> str:
        """Returns the dest mnemonic in current C_COMMAND (8 possibilites).
        Should be called only when command_type() is C_COMMAND.
        """
        if self.current_command_type == Command.C:
            return self._dest

    @property
    def comp(self) -> str:
        """Returns the comp mnemonic in current C_COMMAND (28 possibilites).
        Should be called only when command_type() is C_COMMAND.
        """
        if self.current_command_type == Command.C:
            return self._comp

    @property
    def jump(self) -> str:
        """Returns the jump mnemonic in current C_COMMAND (8 possibilites).
        Should be called only when command_type() is C_COMMAND.
        """
        if self.current_command_type == Command.C:
            return self._jump

    def parse_a(self) -> str:
        """Parses an A instruction (symbols not currently supported):
        A instructions are in the format @value, where value is a
        positive decimal number or symbol referring to such a number.
        For example: @70 or @LOOP
        """
        return self.current_command[1:]

    def parse_c(self) -> C_Instruction:
        """Parses a C instruction
        C instructions are in the dest=comp;jump.
        The dest or jump fields can be omitted.
        """
        dest = comp = jump = None

        try:
            equal_index = self.current_command.index("=")
            dest = self.current_command[:equal_index]
        except ValueError:
            equal_index = -1
        try:
            semi_index = self.current_command.index(";")
            jump = self.current_command[semi_index + 1 :]
            comp = self.current_command[equal_index + 1 : semi_index]
        except ValueError:
            comp = self.current_command[equal_index + 1 :]

        return dest, comp, jump

    def parse_l(self) -> str:
        return self.current_command[1:-1]

