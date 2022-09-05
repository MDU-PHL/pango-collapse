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
            "tests/data/collapse.txt",
            "-a",
            "tests/data/alias_key.json",
        ],
    )
    assert result.exit_code == 0
    expected = pd.read_csv("tests/data/expected.csv")
    output = pd.read_csv("tests/data/output.csv")
    assert expected.Lineage_full.equals(output.Lineage_full)
    assert expected.Lineage_family.equals(output.Lineage_family)
