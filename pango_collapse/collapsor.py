from typing import List
from pango_aliasor.aliasor import Aliasor


class Collapsor(Aliasor):
    def __init__(self, alias_file=None):
        super().__init__(alias_file=alias_file)

    def collapse(self, uncompressed_lineage: str, potential_parents: List[str]):
        if "Recombinant" in potential_parents and uncompressed_lineage.startswith("X"):
            # special case for Recombinant
            return "Recombinant"
        compressed_lineage = self.compress(uncompressed_lineage)
        if compressed_lineage in potential_parents:
            return compressed_lineage
        parts = uncompressed_lineage.split(".")
        compressed_parent_lineage = uncompressed_lineage
        for i in range(1, len(parts)):
            compressed_parent_lineage = self.compress(".".join(parts[:-i]))
            if compressed_parent_lineage in potential_parents:
                return compressed_parent_lineage
        return uncompressed_lineage
