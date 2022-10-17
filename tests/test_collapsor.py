from pango_collapse import Collapsor

collapsor = Collapsor(alias_file="tests/data/alias_key.json")

def test_collapse():
    compressed_lineage = "BA.5.1"
    parent = collapsor.collapse(compressed_lineage, ("BA.5", "B"))
    assert parent == "BA.5"

def test_collapse_column():
    assert ['B', 'B'] == collapsor.collapse_column(("BA.5", "BA.2"), ["B"])

def test_uncompress_column():
    assert ['B.1.1.529.5', 'B'] == collapsor.uncompress_column(("BA.5", "B"))