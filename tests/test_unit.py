from hasm.symboltable import Code, SymbolTable


def test_coder():
    code = Code()
    assert all([True if len(s) == 6 else False for s in code._comps().values()])
    assert all([True if len(s) == 3 else False for s in code._jumps().values()])
    assert all([True if len(s) == 3 else False for s in code._dests().values()])


def test_symboltable():
    st = SymbolTable()
    assert st.get_addr("abc") is None
    st.add_symbol("abc", 123)
    assert st.get_addr("abc") == 123
