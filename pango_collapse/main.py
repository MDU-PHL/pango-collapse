from pathlib import Path
from typing import Optional
import typer
import sys
from .utils import load_potential_parents_from_file, load_potential_parents_from_url
from .collapsor import Collapsor
from rich import print

app = typer.Typer()


def get_version():
    import pkg_resources

    return pkg_resources.get_distribution("pango-collapse").version


def version_callback(value: bool):
    if value:
        version = get_version()
        print(f"pango-collapse {version}", file=sys.stderr)
        raise typer.Exit()


@app.command(context_settings={"help_option_names": ["-h", "--help"]})
def main(
    input: Path = typer.Argument(
        ...,
        help="Path to input CSV/TSV with Lineage column.",
        dir_okay=False,
        exists=True,
    ),
    output: Path = typer.Option(
        None,
        "-o",
        "--output",
        help="Path to output CSV/TSV with Lineage column. If not supplied will print to stdout.",
        dir_okay=False,
    ),
    collapse_file: Optional[Path] = typer.Option(
        f"{Path(__file__).parent.resolve()}/collapse.txt",
        "-c",
        "--collapse-file",
        help="Path to collapse file with lineages (one per line) to collapse up to. Defaults to collapse file shipped with this version of pango-collapse.",
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
    expand_column: Optional[str] = typer.Option(
        "Lineage_expanded",
        "-e",
        "--expand-column",
        help="Column to use for the expanded output.",
    ),
    alias_file: Optional[Path] = typer.Option(
        None,
        "-a",
        "--alias-file",
        help="Path to Pango Alias file for pango_aliasor. Will download latest file if not supplied.",
    ),
    strict: Optional[bool] = typer.Option(
        False,
        "-s",
        "--strict",
        help="If a lineage is not in the collapse file return None instead of the compressed lineage.",
    ),
    latest: Optional[bool] = typer.Option(
        False,
        "-u",
        "--latest",
        help="Load the collapse from from a url (--url).",
    ),
    collapse_file_url: Optional[str] = typer.Option(
        None,
        "--url",
        help="Url to use when loading the collapse file with --latest. https://raw.githubusercontent.com/MDU-PHL/pango-collapse/main/pango_collapse/collapse.txt",
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
    version = get_version()
    print(f"\n[bold green]pango-collapse {version}[bold green]\n", file=sys.stderr)
    import pandas as pd

    collapsor = Collapsor(alias_file=alias_file)

    sep = "\t" if input.suffix == ".tsv" else ","

    df = pd.read_csv(input, low_memory=False, sep=sep)
    if lineage_column not in df.columns:
        print(f"[red]Could not find lineage column: {lineage_column}[red]", file=sys.stderr)
        raise typer.Exit(code=1)

    if latest or collapse_file_url is not None:
        if collapse_file_url is None:
            collapse_file_url = "https://raw.githubusercontent.com/MDU-PHL/pango-collapse/main/pango_collapse/collapse.txt"
        print(f"Loading collapse file from {collapse_file_url}\n", file=sys.stderr)
        potential_parents = load_potential_parents_from_url(url=collapse_file_url)
    else:
        if not collapse_file.exists():
            print(f"[red]Could not find collapse file: {collapse_file}[red]", file=sys.stderr)
            raise typer.Exit(code=1)
        potential_parents = load_potential_parents_from_file(collapse_file=collapse_file)
    print("[yellow]Collapsing up to the following lineages:[yellow]", file=sys.stderr)
    print(" -", "\n - ".join(potential_parents), file=sys.stderr)
    
    df[full_column] = collapsor.uncompress_column(df[lineage_column])
    df[expand_column] = collapsor.expand_column(df[full_column])
    df[collapse_column] = collapsor.collapse_column(df[lineage_column], potential_parents=potential_parents, strict=strict)
    
    if output:
        sep = "\t" if output.suffix == ".tsv" else ","
        df.to_csv(output, index=False, sep=sep)
    else:
        df.to_csv(sys.stdout, index=False, sep=sep)

