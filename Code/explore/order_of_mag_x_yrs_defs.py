import pandas as pd

def add_pct_change(
    column : str,
    df : pd.DataFrame ) -> pd.DataFrame:
  """ PITFALL: Mutates its input.
      PITFALL: Not really percent change -- rather, 100 times that."""
  df["pc"] = df[column].pct_change()
  return df
