from pango_collapse.utils import load_potential_parents_from_url, load_potential_parents_from_file


def test_load_potential_parents_from_url():
    potential_parents=load_potential_parents_from_url("https://raw.githubusercontent.com/MDU-PHL/pango-collapse/main/tests/data/omicron_collapse.txt")
    expected = ["BA.1",
    "BA.2",
    "BA.3",
    "BA.4",
    "BA.5"]
    assert expected == potential_parents

def test_load_potential_parents_from_file():
    potential_parents=load_potential_parents_from_file("tests/data/omicron_collapse.txt")
    expected = ["BA.1",
    "BA.2",
    "BA.3",
    "BA.4",
    "BA.5"]
    assert expected == potential_parents