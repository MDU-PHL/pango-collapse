from pathlib import Path
from typing import Optional
import typer
from .collapsor import Collapsor

app = typer.Typer()


def version_callback(value: bool):
    if value:
        import pkg_resources

        version = pkg_resources.get_distribution("pango-collapse").version
        print(f"pango-collapse {version}")
        raise typer.Exit()


@app.command(context_settings={"help_option_names": ["-h", "--help"]})
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
        f"{Path(__file__).parent.resolve()}/collapse.txt",
        "-c",
        "--collapse-file",
        help="Path to file with lineages on each line to collapse up to.",
    ),
    lineage_column: Optional[str] = typer.Option(
        "Lineage",
        "-l",
        "--lineage-column",
        help="Column to extract from input file for lineage.",
    ),
    full_column: Optional[str] = typer.Option(
        "Lineage_full",
        "-f",
        "--full-column",
        help="Column to use for the uncompressed output.",
    ),
    collapse_column: Optional[str] = typer.Option(
        "Lineage_family",
        "-k",
        "--collapse-column",
        help="Column to use for the collapsed output.",
    ),
    alias_file: Optional[Path] = typer.Option(
        None,
        "-a",
        "--alias-file",
        help="Path to Pango Alias file for pango_aliasor. Will download latest file if not supplied.",
    ),
    collapse_full: Optional[bool] = typer.Option(
        True,
        help="Collapse sublineages all the way up to A or B if they don't have parents in the collapse file.",
    ),
    version: Optional[bool] = typer.Option(
        None,
        "-v",
        "--version",
        callback=version_callback,
        is_eager=True,
        help="Print the current version number and exit.",
    ),
):
    """
    Collapse Pango sublineages up to user defined parent lineages.
    """
    import pandas as pd

    collapsor = Collapsor(alias_file=alias_file)

    df = pd.read_csv(input, low_memory=False)
    df[full_column] = df[lineage_column].apply(
        lambda lineage: collapsor.uncompress(lineage) if pd.notna(lineage) else None
    )
    potential_parents = []
    if collapse_full:
        potential_parents = ["A", "B"]
    if collapse_file:
        with open(collapse_file) as f:
            potential_parents += [
                l.strip() for l in f.readlines() if not l.startswith("#")
            ]
    df[collapse_column] = df[full_column].apply(
        lambda uncompressed_lineage: collapsor.collapse(
            uncompressed_lineage, tuple(potential_parents)
        )
        if uncompressed_lineage
        else None
    )
    df.to_csv(output, index=False)
