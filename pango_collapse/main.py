from pathlib import Path
from typing import List, Optional
from urllib.error import URLError
import typer
import sys
from .utils import load_potential_parents_from_file, load_potential_parents_from_url
from .collapsor import Collapsor
from rich import print
import pandas as pd

app = typer.Typer()


def get_version():
    """
    Retrieves the version of the pango-collapse package.

    Returns:
      str: The version of the pango-collapse package.

    Side Effects:
      This function imports the importlib.metadata module.

    Examples:
      >>> get_version()
      '1.0.0'
    """
    import importlib.metadata
    return importlib.metadata.version("pango-collapse")

def version_callback(value: bool):
    """
    Prints the version of the pango-collapse package and exits the program if the value is True.

    Args:
      value (bool): A flag to determine whether to print the version and exit the program.

    Raises:
      typer.Exit: This exception is raised to exit the program.

    Side Effects:
      This function prints to the console and may exit the program.

    Examples:
      >>> version_callback(True)
      pango-collapse 1.0.0
      >>> version_callback(False)
      # No output and the program continues to run.
    """
    if value:
        version = get_version()
        print(f"pango-collapse {version}")
        raise typer.Exit()


@app.command(context_settings={"help_option_names": ["-h", "--help"]})
def main(
    input: typer.FileText = typer.Argument(
        ... if sys.stdin.isatty() else sys.stdin,
        help="Path to input CSV/TSV with Lineage column.",
        dir_okay=False,
        exists=True,
        show_default=False,
    ),
    output: Path = typer.Option(
        None,
        "-o",
        "--output",
        help="Path to output CSV/TSV with Lineage column. If not supplied will print to stdout.",
        dir_okay=False,
        show_default=False,
    ),
    collapse_file: Optional[str] = typer.Option(
        None,
        "-c",
        "--collapse-file",
        help="Path or URL to collapse file with parental lineages (one per line) to collapse up to. Defaults to collapse file shipped with this version of pango-collapse.",
        show_default=False,
    ),
    parents: Optional[List[str]] = typer.Option(
        None,
        "-p",
        "--parent",
        help="Parental lineage to collapse up to. Can be used multiple times to collapse to multiple lineages. If --collapse-file is supplied parents will be appended to the file.",
        show_default=False,
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
        show_default=False,
        dir_okay=False,
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
        help="Load the latest collapse from from https://raw.githubusercontent.com/MDU-PHL/pango-collapse/main/pango_collapse/collapse.txt.",
    ),
    tsv: bool = typer.Option(
        False,
        "--tsv",
        help="Input file is in TSV format. If not supplied will try to infer from file extension.",
        show_default=False,
    ),
    collapse_file_url: Optional[str] = typer.Option(
        None,
        "--url",
        hidden=True,
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

    collapsor = Collapsor(alias_file=alias_file)

    if tsv:
        sep = "\t"
    else:
        sep = "\t" if input.name.endswith(".tsv") else ","

    try:
        if input.name == "<stdin>":
            df = pd.read_csv(input, low_memory=False, sep=sep)
        else:
            df = pd.read_csv(input, low_memory=False, sep=sep)
    except pd.errors.ParserError:
        print(f"[red]Could not parse input file using '{sep}' delimiter. Please check the file format and delimiter.[red]", file=sys.stderr)
        raise typer.Exit(code=1)

    if lineage_column not in df.columns:
        if input.name == "<stdin>":
            input = "input file"
        print(f"[red]Could not find lineage column '{lineage_column}' in {input}[red]. Use --lineage to specify the pango lineage column name.", file=sys.stderr)
        raise typer.Exit(code=1)
    
    collapse_file_supplied = True
    if collapse_file is None :
        collapse_file_supplied = False
        collapse_file = str(Path(__file__).parent.resolve() / "collapse.txt")

    if not collapse_file.startswith("http") and not Path(collapse_file).exists():
        print(f"[red]Could not find collapse file: {collapse_file}[red]", file=sys.stderr)
        raise typer.Exit(code=1)
    
    if collapse_file_url:
        # deprecated
        print(
            "[yellow bold]The --url option is deprecated and will be removed in a future version. Please use --collapse-file instead.[yellow]",
            file=sys.stderr,
        )
        collapse_file = collapse_file_url
    
    if latest:
        if collapse_file_url is None:
            collapse_file_url = "https://raw.githubusercontent.com/MDU-PHL/pango-collapse/main/pango_collapse/collapse.txt"
        collapse_file = collapse_file_url
    
    if collapse_file.startswith("http"):
        print(f"Loading collapse file from {collapse_file}\n", file=sys.stderr)
        try:
            potential_parents = load_potential_parents_from_url(url=collapse_file)
        except URLError:
            print(f"[red]Could not download collapse file from {collapse_file}[red]", file=sys.stderr)
            raise typer.Exit(code=1)
    else:
        collapse_file = Path(collapse_file)
        potential_parents = load_potential_parents_from_file(collapse_file=collapse_file)
    
    if parents and collapse_file_supplied:
        potential_parents += parents
        potential_parents = list(dict.fromkeys(potential_parents))  # remove duplicates
    elif parents and not collapse_file_supplied:
        potential_parents = parents

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

