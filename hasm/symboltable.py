from typing import Optional

from hasm.types import CodeTable, SymTable


class Code:
    __COMP: CodeTable = {
        "0": "101010",
        "1": "111111",
        "-1": "111010",
        "D": "001100",
        "A": "110000",
        "M": "110000",
        "!D": "001101",
        "!A": "110001",
        "!M": "110001",
        "-D": "001111",
        "-A": "110011",
        "-M": "110011",
        "D+1": "011111",
        "A+1": "110111",
        "M+1": "110111",
        "D-1": "001110",
        "A-1": "110010",
        "M-1": "110010",
        "D+A": "000010",
        "D+M": "000010",
        "D-A": "010011",
        "D-M": "010011",
        "A-D": "000111",
        "M-D": "000111",
        "D&A": "000000",
        "D&M": "000000",
        "D|A": "010101",
        "D|M": "010101",
    }

    __DEST: CodeTable = {
        "null": "000",
        "M": "001",
        "D": "010",
        "MD": "011",
        "A": "100",
        "AM": "101",
        "AD": "110",
        "AMD": "111",
    }

    __JUMP: CodeTable = {
        "null": "000",
        "JGT": "001",
        "JEQ": "010",
        "JGE": "011",
        "JLT": "100",
        "JNE": "101",
        "JLE": "110",
        "JMP": "111",
    }

    def comp(self, val: str) -> Optional[str]:
        return self.__COMP.get(val)

    def jump(self, val: str) -> Optional[str]:
        return self.__JUMP.get(val)

    def dest(self, val: str) -> Optional[str]:
        return self.__DEST.get(val)

    def _comps(self):
        return self.__COMP

    def _jumps(self):
        return self.__JUMP

    def _dests(self):
        return self.__DEST


class SymbolTable:

    __SYM: SymTable = {
        "SP": 0,
        "LCL": 1,
        "ARG": 2,
        "THIS": 3,
        "THAT": 4,
        "r0": 0,
        "R0": 0,
        "r1": 1,
        "R1": 1,
        "r2": 2,
        "R2": 2,
        "r3": 3,
        "R3": 3,
        "r4": 4,
        "R4": 4,
        "r5": 5,
        "R5": 5,
        "r6": 6,
        "R6": 6,
        "r7": 7,
        "R7": 7,
        "r8": 8,
        "R8": 8,
        "r9": 9,
        "R9": 9,
        "r10": 10,
        "R10": 10,
        "r11": 11,
        "R11": 11,
        "r12": 12,
        "R12": 12,
        "r13": 13,
        "R13": 13,
        "r14": 14,
        "R14": 14,
        "r15": 15,
        "R15": 15,
        "SCREEN": 16834,
        "KBD": 24576,
    }

    def __init__(self):
        self.__counter = 16

    def add_symbol(self, symbol: str, addr: int):
        self.__SYM[symbol] = addr

    def add_variable(self, symbol: str):
        self.__SYM[symbol] = self.__counter
        self.__counter += 1

    def get_addr(self, symbol: str) -> Optional[int]:
        return self.__SYM.get(symbol)

