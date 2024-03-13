from typer.testing import CliRunner

from pango_collapse.main import app

runner = CliRunner(mix_stderr=False)


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
    assert expected.Lineage_expanded.equals(output.Lineage_expanded)


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
    assert expected.Lineage_expanded.equals(output.Lineage_expanded)

def test_parents():
    result = runner.invoke(app, ["tests/data/input.csv", "-p", "B.1.1.7", "-p", "B.1.351"])
    assert result.exit_code == 0
    assert "Collapsing up to the following lineages:\n - B.1.1.7\n - B.1.351\n" in result.stderr
    result = runner.invoke(app, ["tests/data/input.csv", "-p", "B.1.1.7", "-p", "B.1.351", "-c", "tests/data/omicron_collapse.txt"])
    assert result.exit_code == 0
    assert "Collapsing up to the following lineages:\n - BA.1\n - BA.2\n - BA.3\n - BA.4\n - BA.5\n - B.1.1.7\n - B.1.351\n" in result.stderr

def test_error_no_input():
    result = runner.invoke(app, ["-o", "tests/data/output.csv"])
    assert result.exit_code == 2
    assert "Missing argument 'INPUT'." in result.stderr

def test_missing_collapse_file():
    result = runner.invoke(app, ["tests/data/input.csv", "-c", "does_not_exist.txt"])
    assert result.exit_code == 1
    assert "Could not find collapse file: does_not_exist.txt" in result.stderr

def test_missing_lineage_column():
    result = runner.invoke(app, ["tests/data/input.csv", "-l", "does_not_exist"])
    assert result.exit_code == 1
    assert "Could not find lineage column 'does_not_exist'" in result.stderr

def test_url_raises_deprecation_warning():
    result = runner.invoke(app, ["tests/data/input.csv", "--url", "https://raw.githubusercontent.com/MDU-PHL/pango-collapse/main/pango_collapse/collapse.txt"])
    assert result.exit_code == 0
    #  catch deprecation warning
    assert "--url option is deprecated" in result.stderr

