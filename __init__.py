"""
Neuroblastoma Gene Expression Signatures

This module contains a few helper functions to go from long format tables (as are used to store the signatures) to dictionaries,
to query the available, built-in signatures, and to score single-cell adata objects for signature activity in two different ways
"""


def long_to_dict(df):
    signatures = dict(
        df[["gene_set", "gene_name"]].set_index("gene_name").groupby("gene_set").groups
    )
    return signatures


def prepare_z_layer(ad, layer="z"):
    import scanpy as sc

    print(f"z-scaling ad.X to new layer '{layer}'")

    ad.layers["z"] = ad.X.copy()
    sc.pp.scale(ad, layer=layer)

    return ad


def score_signatures_z(
    ad,
    signatures=None,
    layer="z",
    obs_prefix="z-",
    min_genes=10,
    min_z=2,
    min_cells=5,
    auto_scale=True,
):
    import numpy as np

    if not "z" in ad.layers and auto_scale:
        prepare_z_layer(ad)

    if signatures is None:
        print(f"loading built-in signatures")
        import os
        import pandas as pd

        path = os.path.dirname(__file__)
        df = pd.read_csv(os.path.join(path, "gene_sets.tsv"), sep="\t")
        signatures = long_to_dict(df)

    for sig_name, genes in signatures.items():
        print(f"scoring {sig_name}")

        genes = [g for g in genes if g in ad.var_names]
        _ad = ad[:, genes]
        if layer:
            X = _ad.layers[layer]
        else:
            X = _ad.X

        Z = X.sum(axis=1) / np.sqrt(len(genes))
        n_sig = (np.abs(Z) >= min_z).sum()
        if n_sig >= min_cells:
            print(f"found {n_sig} cells. Keeping signature in .obs")
            ad.obs[f"z-{sig_name}"] = Z

    return ad
