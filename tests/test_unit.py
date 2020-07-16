import os

from hasm.symboltable import SymbolTable
from hasm.code import Code
from hasm.parser import Parser
from hasm.types import Command


def test_coder():
    code = Code()
    assert all([True if len(s) == 7 else False for s in code._comps().values()])
    assert all([True if len(s) == 3 else False for s in code._jumps().values()])
    assert all([True if len(s) == 3 else False for s in code._dests().values()])


def test_symboltable():
    st = SymbolTable()
    assert st.get_addr("abc") is None
    st.add_entry("abc", 123)
    assert st.get_addr("abc") == 123


def test_parse_process():
    expected = ["@10", "M=1", "M=0", "(LOOP)"]
    parser = Parser("./tests/test_files/processtest.asm")
    assert parser.file == expected


def test_parse_c_instructions():
    expected = [
        ("D", "D-A", None),
        (None, "D", "JGT"),
        ("M", "M+1", None),
        ("M", "M-1", "JGT"),
    ]
    parser = Parser("./tests/test_files/c_instructions.asm")
    assert len(parser.file) == 4
    count = 0
    while parser.has_more_commands():
        assert parser.line_number == count
        parser.advance()
        assert parser.current_command_type == Command.C
        assert (parser._dest, parser._comp, parser._jump) == expected[count]
        count += 1

