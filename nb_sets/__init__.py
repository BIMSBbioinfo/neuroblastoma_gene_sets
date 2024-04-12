import pandas as pd
import os

path = os.path.dirname(__file__)

__doc__ = open(f"{path}/../README.md").read()

def as_dict():

    df = pd.read_csv(f"{path}/../gene_sets.tsv", sep="\t")
    return dict([(name, idx.to_list()) for name, idx in df.set_index('gene_name').groupby('gene_set').groups.items()])


d = as_dict()
meta = pd.read_csv(f"{path}/../set_meta.tsv", sep='\t')

