import numpy as np
import pandas as pd


def get_partial_index(idx, inv_map: dict) -> pd.Index:
    """Get a partial index based on an inverse mapping."""
    if idx in inv_map:
        return inv_map[idx]
    if isinstance(next(iter(inv_map.keys())), str):
        return np.nan
    for key in inv_map.keys():
        if all([idx[i] == key[i] for i in range(len(key))]):
            return inv_map[key]
