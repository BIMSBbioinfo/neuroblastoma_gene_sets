# Neuroblastoma gene sets

A curated collection of gene sets relevant to neuroblastoma research, covering cell states, developmental programs, metabolic signatures, and hallmark pathways from ~16 published sources and custom curation (~68 gene sets, ~8200 entries total).

## `gene_sets.tsv`

Main gene set table. Columns:

- `source_id`: identifier for the originating study or resource (links to `set_meta.tsv`)
- `gene_set`: name of the gene set (e.g. `MES`, `ADRN`, `Hypoxia`, `EMT_I`)
- `gene_name`: HGNC gene symbol (e.g. `ACTB`)
- `score`: optional numeric score (enrichment, log2FC, etc.); can be empty

## `set_meta.tsv`

Metadata for each source. Columns:

- `source_id`: matches `source_id` in `gene_sets.tsv`
- `url`: link to the publication or resource
- `description`: brief description of the study and what the gene sets represent
- `citation`: full citation string

## Python module

Install the repo as a package (or add it to your path), then:

```python
import neuroblastoma_gene_sets as nb_sets
```

### Get a gene set dictionary (for gseapy, decoupler, etc.)

```python
import pandas as pd

df = pd.read_csv("gene_sets.tsv", sep="\t")
signatures = nb_sets.long_to_dict(df)
# -> {"MES": ["A2M", "ABRACL", ...], "ADRN": [...], ...}
```

### Score an AnnData object

`score_signatures_z` scores each signature using z-scaled expression and writes results to `ad.obs`:

```python
# Uses built-in gene sets automatically; z-scales ad.X if no "z" layer present
ad = nb_sets.score_signatures_z(ad)
# Results appear in ad.obs as e.g. "z-MES", "z-ADRN", ...
```

Or pass custom signatures and control filtering:

```python
ad = nb_sets.score_signatures_z(
    ad,
    signatures=my_dict,   # {name: [gene, ...]}
    min_genes=10,          # skip signature if fewer genes overlap with ad.var_names
    min_z=2,               # z-score threshold to count a cell as "active"
    min_cells=5,           # skip signature if fewer than this many cells exceed min_z
)
```

`prepare_z_layer` can also be called directly to z-scale before scoring:

```python
ad = nb_sets.prepare_z_layer(ad)  # adds ad.layers["z"]
```
