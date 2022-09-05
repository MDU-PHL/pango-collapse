from pango_collapse import Collapsor


def test_find_parent():
    collapsor = Collapsor(alias_file="tests/data/alias_key.json")
    uncompressed_lineage = "B.1.1.529.5"
    parent = collapsor.collapse(uncompressed_lineage, ("BA.5", "B"))
    assert parent == "BA.5"
