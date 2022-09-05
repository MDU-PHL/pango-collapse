# Pango-collapse 

[![](https://img.shields.io/pypi/v/pango-collapse.svg)](https://pypi.org/project/pango-collapse/)
[![tests](https://github.com/MDU-PHL/pango-collapse/actions/workflows/tests.yaml/badge.svg)](https://github.com/MDU-PHL/pango-collapse/actions/workflows/tests.yaml)

CLI to collapse Pango linages for reporting

## Install 

Install from pypi with pip.

```
pip install pango-collapse
```

## Usage

`pango-collapse` takes a CSV file of SARS-CoV-2 samples (`input.csv`) with a column (default `Lineage`) indicating the pango lineage of the samples (e.g. output from pangoLEARN, nextclade, USHER, etc). `pango-collapse` will collapse lineages up to the first user defined parent lineage (specified in a text file with `--collapse-file`). If the sample lineage has no parent lineage in the use defined collapse file the lineage will be collapsed up to either `A` or `B`. `pango-collapse` will produce an output file which is a copy of the input file plus `Lineage_full` (the uncompressed lineage) and `Lineage_family` (the lineage compressed up to). 

```
# input.csv
Lineage
BA.5.2.1
BA.4.6
BE.1
```

```
# collapse.txt
BA.5
BE.1
```

```bash
pango-collapse input.csv --collapse-file collapse.txt -o output.csv 
```

```
# output.csv 
Lineage,Lineage_full,Lineage_family
BA.5.2.1,B.1.1.529.5.2.1,BA.5
BA.4.6,B.1.1.529.4.6,B
BE.1,B.1.1.529.5.3.1.1,BE.1
```