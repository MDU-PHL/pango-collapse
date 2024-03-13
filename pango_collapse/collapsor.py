from typing import List
from urllib.error import URLError
from pango_aliasor.aliasor import Aliasor
import pandas as pd


class Collapsor(Aliasor):
    """
    A class that inherits from Aliasor and provides methods to collapse, uncompress, and expand lineages.

    Args:
      alias_file (str, optional): Path to the alias file. Defaults to None.

    Raises:
      URLError: If the alias file cannot be downloaded.

    Side Effects:
      If the alias file cannot be downloaded, a warning is issued and a default alias file is used.
    """
    def __init__(self, alias_file=None):
        """
        Initializes the Collapsor class.

        Args:
          alias_file (str, optional): Path to the alias file. Defaults to None.

        Raises:
          URLError: If the alias file cannot be downloaded.

        Side Effects:
          If the alias file cannot be downloaded, a warning is issued and a default alias file is used.
        """
        try:
            super().__init__(alias_file=alias_file)
        except URLError:
            from warnings import warn
            from pathlib import Path
            warn("""\n\nCould not download the alias_key file!\n\nUsing default the alias_key file which may be out of date. This may result in lineages that cannot be collapsed.\n\nThe alias_key is should be kept up to date because it contains the hierarchical information about lineages designations.\n\nTo specify a custom alias file use the `--alias-file` option.\n""")
            alias_file = Path(__file__).parent / "alias_key.json"
            super().__init__(alias_file=alias_file)



    def collapse(
        self, compressed_lineage: str, potential_parents: List[str], strict=False
    ):
        """
        Collapses a lineage.

        Args:
          compressed_lineage (str): The lineage to collapse.
          potential_parents (List[str]): A list of potential parent lineages.
          strict (bool, optional): If True, returns None if the lineage cannot be collapsed. Defaults to False.

        Returns:
          str: The collapsed lineage.

        Examples:
          >>> collapse('B.1.1.7', ['B.1', 'B.1.1'], strict=False)
          'B.1.1'
        """
        if compressed_lineage in potential_parents:
            return compressed_lineage

        uncompressed_lineage = self.uncompress(compressed_lineage)

        parts = uncompressed_lineage.split(".")

        for i in range(1, len(parts)):
            compressed_parent_lineage = self.compress(".".join(parts[:-i]))
            if compressed_parent_lineage in potential_parents:
                return compressed_parent_lineage

        if uncompressed_lineage.startswith("X") and "Recombinant" in potential_parents:
            # special case for Recombinant
            return "Recombinant"

        if strict:
            return None

        return compressed_lineage

    def collapse_column(
        self, array_of_uncompress_lineages, potential_parents, strict=False
    ):
        """
        Collapses a column of lineages.

        Args:
          array_of_uncompress_lineages (List[str]): The lineages to collapse.
          potential_parents (List[str]): A list of potential parent lineages.
          strict (bool, optional): If True, returns None for lineages that cannot be collapsed. Defaults to False.

        Returns:
          List[str]: The collapsed lineages.
        """
        return [
            self.collapse(compressed_lineage, potential_parents, strict=strict)
            if pd.notna(compressed_lineage)
            else None
            for compressed_lineage in array_of_uncompress_lineages
        ]

    def uncompress_column(self, array_of_compressed_lineages):
        """
        Uncompresses a column of lineages.

        Args:
          array_of_compressed_lineages (List[str]): The lineages to uncompress.

        Returns:
          List[str]: The uncompressed lineages.
        """
        return [
            self.uncompress(lineage) if pd.notna(lineage) else None
            for lineage in array_of_compressed_lineages
        ]

    def expand(self, lineage, delimiter=":"):
        """
        Expands a lineage.

        Args:
          lineage (str): The lineage to expand.
          delimiter (str, optional): The delimiter to use in the expanded lineage. Defaults to ":".

        Returns:
          str: The expanded lineage.

        Examples:
          >>> expand('B.1.1.7', delimiter=':')
          'B:1:1:7'
        """
        uncompressed_lineage = self.uncompress(lineage)

        parts = uncompressed_lineage.split(".")
        levels = len(parts) - 1  # (remove starting B/A)
        indirections = (levels) % 3 if (levels) % 3 != 0 else 3

        expanded_lineage = [self.compress(uncompressed_lineage)]
        for i in range(indirections, levels, 3):
            compressed_parent_lineage = self.compress(".".join(parts[:-i]))
            expanded_lineage.append(compressed_parent_lineage)

        return delimiter.join(expanded_lineage[::-1])

    def expand_column(self, array_of_lineages, delimiter=":"):
        """
        Expands a column of lineages.

        Args:
          array_of_lineages (List[str]): The lineages to expand.
          delimiter (str, optional): The delimiter to use in the expanded lineages. Defaults to ":".

        Returns:
          List[str]: The expanded lineages.
        """
        return [
            self.expand(lineage, delimiter=delimiter) if pd.notna(lineage) else None
            for lineage in array_of_lineages
        ]
