from pathlib import Path
import pandas as pd

orders = pd.read_csv(Path("data/private/orders.csv"))
orders["paid_at"] = pd.to_datetime(orders["paid_at"], errors="coerce")
orders["rate"] = orders["shipping"].round(2)

light = orders[orders["sku_class"].eq("boxinet") & orders["rate"].isin([9.99, 14.99])].copy()
print("light_us_boxinet", len(light))

paid = light[light["financial_status"].eq("paid")]
print("drop_not_paid", len(light) - len(paid))

open_ = paid[paid["cancelled_at"].isna()]
print("drop_cancelled", len(paid) - len(open_))

open_["state"] = open_["ship_state"].astype("string").str.upper()
base = open_[~open_["state"].isin(["HI", "AK", "HAWAII", "ALASKA"])]
print("drop_hi_ak", len(open_) - len(base))
print(base.groupby("rate").size().to_string())

base = base.drop(columns=["state"])
base.to_csv(Path("data/private/light_orders.csv"), index=False)
print("wrote data/private/light_orders.csv", len(base))