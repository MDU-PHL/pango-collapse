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

def test_collapse_recombinants():
    assert ["Recombinant", "Recombinant", "XBF.7"] == collapsor.collapse_column(
        ['XBB.1.5.13', 'EL.1', "XBF.7.1"], 
        ["Recombinant", "XBF.7"]
    )

def test_recombinant_sublineage():
    compressed_lineage = 'EL.1'
    assert "XBB.1" == collapsor.collapse(compressed_lineage, ["XBB.1"])