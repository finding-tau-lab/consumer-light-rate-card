from pathlib import Path
import pandas as pd

path = Path("data/raw/ups_zone_84098.csv")
df = pd.read_csv(path, header=None)
print("shape", df.shape)
print("--- first 15 rows ---")
print(df.head(15).to_string())