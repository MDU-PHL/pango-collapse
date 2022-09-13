from typing import List
from pango_aliasor.aliasor import Aliasor


class Collapsor(Aliasor):
    def __init__(self, alias_file=None):
        super().__init__(alias_file=alias_file)

    def collapse(
        self, compressed_lineage: str, potential_parents: List[str], strict=False
    ):
            
        if compressed_lineage in potential_parents:
            return compressed_lineage
        
        uncompressed_lineage = self.uncompress(compressed_lineage)

        parts = uncompressed_lineage.split(".")

        for i in range(1, len(parts)):
            compressed_parent_lineage = self.compress(".".join(parts[:-i]))
            if compressed_parent_lineage in potential_parents:
                return compressed_parent_lineage
        
        if compressed_lineage.startswith("X") and "Recombinant" in potential_parents:
            # special case for Recombinant
            return "Recombinant"

        if strict:
            return None

        return compressed_lineage
