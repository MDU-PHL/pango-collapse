from pathlib import Path
from typing import Optional
import typer
from .collapsor import Collapsor

app = typer.Typer()


@app.command()
def main(
    input: Path = typer.Argument(
        ...,
        help="Path in input CSV with with Lineage column.",
        dir_okay=False,
        exists=True,
    ),
    output: Path = typer.Option(
        ...,
        "-o",
        "--output",
        help="Path in output CSV with with Lineage column.",
        dir_okay=False,
    ),
    collapse_file: Optional[Path] = typer.Option(
        None,
        "-c",
        "--collapse-file",
        help="Path to file with lineages on each line to collapse up to.",
    ),
    lineage_column: Optional[str] = typer.Option(
        "Lineage",
        help="Column to extract from input file for lineage",
    ),
    alias_file: Optional[Path] = typer.Option(
        None,
        "-a",
        "--alias-file",
        help="Path to Pango Alias file for pango_aliasor. Will download latest file if not supplied.",
    ),
):
    """
    Collapse Pango linages up to user defined lineages.
    """
    import pandas as pd

    collapsor = Collapsor(alias_file=alias_file)

    df = pd.read_csv(input, low_memory=False)
    df["Lineage_full"] = df[lineage_column].apply(
        lambda lineage: collapsor.uncompress(lineage) if pd.notna(lineage) else None
    )
    potential_parents = ["A", "B"]
    if collapse_file:
        with open(collapse_file) as f:
            potential_parents += [
                l.strip() for l in f.readlines() if not l.startswith("#")
            ]
    df["Lineage_family"] = df.Lineage_full.apply(
        lambda uncompressed_lineage: collapsor.collapse(
            uncompressed_lineage, tuple(potential_parents)
        )
        if uncompressed_lineage
        else None
    )
    df.to_csv(output, index=False)
