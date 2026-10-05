from pathlib import Path
import pandas as pd

tab = pd.read_csv(Path("outputs/orders_by_zone_rate.csv"), index_col=0)
tab = tab.drop(index="All", errors="ignore").drop(columns="All", errors="ignore")
tab.index = tab.index.astype(float).astype(int)
rates = pd.read_csv(Path("data/public/ground_40lb_list.csv"))
m = tab.reset_index().rename(columns={"index": "zone"}).merge(rates, on="zone")

resi = 3.60
for discount in (0.70, 0.50, 0.30, 0.20):
    cost = m["list_rate"] * discount + resi
    hole_999 = ((9.99 - cost) * m["9.99"]).sum()
    hole_1499 = ((14.99 - cost) * m["14.99"]).sum()
    print(
        f"pay_{int(discount*100)}_pct_of_list",
        "per_box_999", round(hole_999 / m["9.99"].sum(), 2),
        "per_box_1499", round(hole_1499 / m["14.99"].sum(), 2),
    )