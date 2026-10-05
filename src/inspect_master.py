from pathlib import Path
import pandas as pd

df = pd.read_csv(Path("data/raw/master_orders.csv"), low_memory=False)
name = df["Lineitem name"].fillna("")
df["is_boxinet"] = name.str.contains("Boxinet|Bassinet", case=False) & ~name.str.contains("Bundle", case=False)
df["is_sheet"] = name.str.contains("Sheet", case=False)
df["is_bundle"] = name.str.contains("Bundle", case=False)

orders = (
    df.groupby("Name", as_index=False)
    .agg(
        shipping=("Shipping", "first"),
        paid_at=("Paid at", "first"),
        financial_status=("Financial Status", "first"),
        cancelled_at=("Cancelled at", "first"),
        ship_zip=("Shipping Zip", "first"),
        ship_state=("Shipping Province", "first"),
        ship_country=("Shipping Country", "first"),
        source=("Source", "first"),
        boxinet=("is_boxinet", "any"),
        sheet=("is_sheet", "any"),
        bundle=("is_bundle", "any"),
    )
)

def sku_class(r):
    if r.boxinet:
        return "boxinet"
    if r.sheet and not r.bundle:
        return "sheet_only"
    if r.bundle:
        return "bundle"
    return "other"

orders["sku_class"] = orders.apply(sku_class, axis=1)
orders["paid_at"] = pd.to_datetime(orders["paid_at"], errors="coerce")
orders["ship_zip"] = (
    orders["ship_zip"].astype("string")
    .str.replace(r"^'+", "", regex=True)
    .str.replace(r"\D", "", regex=True)
    .str.slice(0, 5)
    .str.zfill(5)
)
orders["ship_zip3"] = orders["ship_zip"].str.slice(0, 3)
orders = orders.sort_values("paid_at").reset_index(drop=True)
orders.insert(0, "order_id", [f"F{i:05d}" for i in range(1, len(orders) + 1)])
orders = orders.drop(columns=["Name", "boxinet", "sheet", "bundle"])

out = Path("data/private/orders.csv")
orders.to_csv(out, index=False)

light = orders[orders["sku_class"].eq("boxinet") & orders["shipping"].isin([9.99, 14.99])]
print("wrote", out)
print("cols", list(orders.columns))
print(light.groupby("shipping")["paid_at"].agg(["count", "min", "max"]).to_string())

light = orders[orders["sku_class"].eq("boxinet")].copy()
light["rate"] = light["shipping"].round(2)
light = light[light["rate"].isin([9.99, 14.99])]
print("--- rounded match ---")
print(light.groupby("rate").size().to_string())
print("--- financial status ---")
print(light["financial_status"].value_counts(dropna=False).to_string())
print("cancelled", light["cancelled_at"].notna().sum())
print("--- country ---")
print(light["ship_country"].value_counts(dropna=False).head(10).to_string())