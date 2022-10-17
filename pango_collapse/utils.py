from typing import List


def load_potential_parents_from_url(
        url: str
    ) -> List[str]:
    import urllib.request
    potential_parents = []
    with urllib.request.urlopen(url) as data:
        potential_parents += data.read().decode("utf-8").strip().split("\n")
    return [l.strip() for l in potential_parents if not l.startswith("#")]

def load_potential_parents_from_file(collapse_file: str) -> List[str]:
    with open(collapse_file) as f:
        potential_parents = [l.strip() for l in f.readlines() if l.strip()]
    return [l for l in potential_parents if not l.startswith("#")]