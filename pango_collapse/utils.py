from typing import List
from urllib.error import URLError


def load_potential_parents_from_url(
        url: str
    ) -> List[str]:
    import urllib.request
    potential_parents = []
    try:
        with urllib.request.urlopen(url) as data:
            potential_parents += data.read().decode("utf-8").strip().split("\n")
    except URLError:
        raise URLError(f"Could not download collapse file from {url}.")
    return [line.strip() for line in potential_parents if not line.startswith("#")]

def load_potential_parents_from_file(collapse_file: str) -> List[str]:
    with open(collapse_file) as f:
        potential_parents = [l.strip() for l in f.readlines() if l.strip()]
    return [line for line in potential_parents if not line.startswith("#")]