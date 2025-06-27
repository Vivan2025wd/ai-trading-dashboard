# backend/ml_engine/module_utils.py

"""
Utility functions for ML engine (placeholder for now).
Add data processing helpers, feature scaling, etc. here.
"""

def normalize_series(series):
    """Normalize a pandas Series between 0 and 1."""
    min_val = series.min()
    max_val = series.max()
    if max_val - min_val == 0:
        return series * 0  # avoid division by zero
    return (series - min_val) / (max_val - min_val)
