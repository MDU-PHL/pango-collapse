from typing import List
from urllib.error import URLError


def load_potential_parents_from_url(
        url: str
    ) -> List[str]:
    """
    Loads potential parents from a given URL.

    Args:
      url (str): The URL to load potential parents from.

    Returns:
      List[str]: A list of potential parents.

    Raises:
      URLError: If the URL cannot be reached or the data cannot be downloaded.

    Side Effects:
      This function may raise an exception and halt the program if the URL is not reachable or the data cannot be downloaded.

    Examples:
      >>> load_potential_parents_from_url("http://example.com/parents.txt")
      ['parent1', 'parent2', 'parent3']
    """
    import urllib.request
    potential_parents = []
    try:
        with urllib.request.urlopen(str(url)) as data:
            potential_parents += data.read().decode("utf-8").strip().split("\n")
    except URLError:
        raise URLError(f"Could not download collapse file from {url}.")
    return [line.strip() for line in potential_parents if not line.startswith("#")]

def load_potential_parents_from_file(collapse_file: str) -> List[str]:
    """
    Loads potential parents from a given file.

    Args:
      collapse_file (str): The file to load potential parents from.

    Returns:
      List[str]: A list of potential parents.

    Side Effects:
      This function may raise an exception and halt the program if the file cannot be opened or read.

    Examples:
      >>> load_potential_parents_from_file("parents.txt")
      ['parent1', 'parent2', 'parent3']
    """
    with open(collapse_file) as f:
        potential_parents = [line.strip() for line in f.readlines() if line.strip()]
    return [line for line in potential_parents if not line.startswith("#")]