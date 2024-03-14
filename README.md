# Neuroblastom gene sets

Let's collect lists of genes here that we

  * encounter in publications
  * identify as markers
  * find relevant in our study of NB

I initially thought JSON would be good, but now I am of the opinion that tables would be better:

## `gene_sets.tsv`

Columns:

  * (human) gene_name: stuff like ACTB. Easy to add other species names as new colunms.
  * gene_id: ENSG00XXXX (optional)
  * group: can be cell states such as "Monocyte", but also pathways such as "E2F targets" or "heat shock" 
  * score: (optional) can be NaN, but could also be enrichment (for marker genes), or log2FC (for DEGs)

A second table can be maintained to keep overview of the groups

## `set_meta.tsv`

  * group: same as above
  * kind: "pathway", "module", "literature", "marker", "DEG"
  * description: for example "upregulated upon MYCN knock-down" or whatever
  * citation: PMID or doi where applicable
