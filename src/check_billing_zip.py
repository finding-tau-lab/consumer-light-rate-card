from pathlib import Path
import pandas as pd

df = pd.read_csv(Path("data/raw/master_orders.csv"), low_memory=False)
name = df["Lineitem name"].fillna("")
df["is_boxinet"] = name.str.contains("Boxinet|Bassinet", case=False) & ~name.str.contains("Bundle", case=False)

orders = (
    df.groupby("Name", as_index=False)
    .agg(
        shipping=("Shipping", "first"),
        financial_status=("Financial Status", "first"),
        ship_zip=("Shipping Zip", "first"),
        bill_zip=("Billing Zip", "first"),
        boxinet=("is_boxinet", "any"),
    )
)
orders["rate"] = orders["shipping"].round(2)
light = orders[orders["boxinet"] & orders["rate"].isin([9.99, 14.99]) & orders["financial_status"].eq("paid")]

def digits(s):
    return s.astype("string").str.replace(r"^'+", "", regex=True).str.replace(r"\D", "", regex=True)

ship = digits(light["ship_zip"])
bill = digits(light["bill_zip"])
missing = ship.fillna("").str.len().eq(0)
print("light_paid", len(light))
print("missing_ship_zip", int(missing.sum()))
print("missing_ship_but_bill_zip", int((missing & bill.fillna("").str.len().ge(5)).sum()))
addr = df.groupby("Name", as_index=False).agg(
    street=("Shipping Street", "first"),
    addr1=("Shipping Address1", "first"),
)
light = light.merge(addr, on="Name", how="left")
blob = light["street"].astype("string") + " " + light["addr1"].astype("string")
found = blob.str.contains(r"\d{5}", na=False)
print("missing_ship_zip_with_5digit_in_street", int((missing & found).sum()))