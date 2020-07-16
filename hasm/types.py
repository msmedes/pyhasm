from typing import Dict, Tuple, Optional
from enum import Enum

CodeTable = Dict[str, str]
SymTable = Dict[str, int]

C_Instruction = Tuple[Optional[str], str, Optional[str]]


class Command(Enum):
    A = 1
    C = 2
    L = 3
