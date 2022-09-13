# Pango-collapse 

[![](https://img.shields.io/pypi/v/pango-collapse.svg)](https://pypi.org/project/pango-collapse/)
[![tests](https://github.com/MDU-PHL/pango-collapse/actions/workflows/tests.yaml/badge.svg)](https://github.com/MDU-PHL/pango-collapse/actions/workflows/tests.yaml)

CLI to collapse Pango linages for reporting

[![](images/collapse.gif)](https://mdu-phl.github.io/pango-watch/tree/)

## Install 

Install from pypi with pip.

```
pip install pango-collapse
```

## Usage

`pango-collapse` takes a CSV file of SARS-CoV-2 samples (`input.csv`) with a column (default `Lineage`) indicating the pango lineage of the samples (e.g. output from pangoLEARN, nextclade, USHER, etc). 

```
# input.csv
Lineage
BA.5.2.1
BA.4.6
BE.1
```

`pango-collapse` will collapse lineages up to the first user defined parent lineage (specified in a text file with `--collapse-file`). If the sample lineage has no parent lineage in the user defined collapse file the compressed lineage will be returned. Collapsed up to either `A` or `B` by add A and B to the collapse file. By default (i.e. if no collapse file is specified) `pango-collapse` uses the collapse file found [here](https://github.com/MDU-PHL/pango-collapse/blob/main/pango_collapse/collapse.txt). This file is dependant on the version of `pango-collapse`, use `--latest` to use the latest version on the collapse file at run time. 

```
# collapse.txt
BA.5
BE.1
```

`pango-collapse` will produce an output file which is a copy of the input file plus `Lineage_full` (the uncompressed lineage) and `Lineage_family` (the lineage compressed up to) columns. 


```bash
pango-collapse input.csv --collapse-file collapse.txt -o output.csv 
```

```
# output.csv 
Lineage,Lineage_full,Lineage_family
BA.5.2.1,B.1.1.529.5.2.1,BA.5
BA.4.6,B.1.1.529.4.6,BA.4.6
BE.1,B.1.1.529.5.3.1.1,BE.1
```

## Nextclade example

This example shows how to use some of the `pango-collapse` features by collapsing the Pango Lineages in the output from [Nextclade](https://clades.nextstrain.org/).

Produce a nextclade.tsv file from a `nextclade` analysis (there is an example file in [`tests/data`](https://github.com/MDU-PHL/pango-collapse/tree/main/tests/data). 

We are only interested in the major sub-lineages of omicron i.e. BA.1-BA.5. We can therefor make a collapse file with the following:

```
# omicron
BA.1
BA.2
BA.3
BA.4
BA.5
```

> Note: BA is an alias of B.1.1.529, however, as we have not included B.1.1.529 in our collapse file any samples designated B.1.1.529 will not be compressed.

Run the following command to collapse the omicron sub-lineages:

```
pango-collapse nextclade.tsv -o nextclade_collapsed_omicron.tsv -l Nextclade_pango --strict 
```

The `-l` (`--lineage-column`) flag tells `pango-collapse` to look for the compressed linage in the `Nextclade_pango` column in the nextclade.tsv file.

The `--strict` tells `pango-collapse` to use strict mode i.e. only report lineages in the collapse file. If the lineage cannot be collapsed then no value is returned in the collapse column. 

We can visualise the results in pandas:

```
import pandas as pd
df = pd.read_csv("nextclade_output.tsv", sep="\t")
df.Lineage_family.fillna('Other', inplace=True)
df.Lineage_family.value_counts().plot(kind='bar')
```

![](images/nextclade_omicron.jpg)