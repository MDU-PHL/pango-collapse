from typer.testing import CliRunner

from pango_collapse.main import app

runner = CliRunner()


def test_help():
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "Usage" in result.stdout


def test_cli():
    import pandas as pd

    result = runner.invoke(
        app,
        [
            "tests/data/input.csv",
            "-o",
            "tests/data/output.csv",
            "-c",
            "tests/data/test_collapse.txt",
            "-a",
            "tests/data/alias_key.json",
        ],
    )
    assert result.exit_code == 0
    expected = pd.read_csv("tests/data/expected.csv")
    output = pd.read_csv("tests/data/output.csv")
    assert expected.Lineage_full.equals(output.Lineage_full)
    assert expected.Lineage_family.equals(output.Lineage_family)


def test_nextclade():
    import pandas as pd

    result = runner.invoke(
        app,
        [
            "tests/data/nextclade.tsv",
            "-o",
            "tests/data/nextclade_output.tsv",
            "-c",
            "tests/data/omicron_collapse.txt",
            "-a",
            "tests/data/alias_key.json",
            "-l",
            "Nextclade_pango",
            "--strict"
        ],
    )
    assert result.exit_code == 0
    expected = pd.read_csv("tests/data/nextclade_output_expected.tsv", sep="\t")
    output = pd.read_csv("tests/data/nextclade_output.tsv", sep="\t")
    assert expected.Lineage_full.equals(output.Lineage_full)
    assert expected.Lineage_family.equals(output.Lineage_family)
