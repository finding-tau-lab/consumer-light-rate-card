from pathlib import Path
import pandas as pd

raw = pd.read_csv(Path("data/raw/ups_zone_84098.csv"), header=None, skiprows=9)
zones = raw.iloc[:, [0, 1]].copy()
zones.columns = ["zip3", "zone"]
zones["zip3"] = (
    zones["zip3"].astype("string")
    .str.replace(r"\.0$", "", regex=True)
    .str.replace(r"\D", "", regex=True)
    .str.zfill(3)
)
zones["zone"] = pd.to_numeric(zones["zone"], errors="coerce")
zones = zones.dropna(subset=["zone"]).drop_duplicates("zip3")
print("zip3_rows", len(zones))

light = pd.read_csv(Path("data/private/light_orders.csv"), dtype={"ship_zip3": "string"})
light["ship_zip3"] = (
    light["ship_zip3"].astype("string")
    .str.replace(r"\.0$", "", regex=True)
    .str.replace(r"\D", "", regex=True)
    .str.zfill(3)
)
merged = light.merge(zones, left_on="ship_zip3", right_on="zip3", how="left")
print("orders", len(merged))
print("unmatched", int(merged["zone"].isna().sum()))
miss = merged.loc[merged["zone"].isna(), "ship_zip3"]
print("unmatched_orders", int(miss.shape[0]))
print("unmatched_zip3", int(miss.nunique()))
print(miss.value_counts().head(20).to_string())
print("null_zip3", int(merged["ship_zip3"].isna().sum()))
blank = merged.loc[merged["zone"].isna()]
print(blank["ship_state"].value_counts(dropna=False).head(10).to_string())
print(blank["ship_zip"].head(8).tolist())
zoned = merged[merged["zone"].between(2, 8)].copy()
zoned["rate"] = zoned["shipping"].round(2)
tab = pd.crosstab(zoned["zone"], zoned["rate"], margins=True)
print(tab.to_string())
tab.to_csv(Path("outputs/orders_by_zone_rate.csv"))
print("wrote outputs/orders_by_zone_rate.csv", len(zoned))