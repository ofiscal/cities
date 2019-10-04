import pandas as pd

def add_pct_change(
    column : str,
    df : pd.DataFrame ) -> pd.DataFrame:
  """ PITFALL: Mutates its input.
      PITFALL: Not really percent change, but rather, that / 100 --
      e.g. if it doubles, its "percent change" is 1."""
  df["pc"] = df[column].pct_change()
  return df
