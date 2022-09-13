from pango_collapse import Collapsor


def test_collapse():
    collapsor = Collapsor(alias_file="tests/data/alias_key.json")
    compressed_lineage = "BA.5.1"
    parent = collapsor.collapse(compressed_lineage, ("BA.5", "B"))
    assert parent == "BA.5"
