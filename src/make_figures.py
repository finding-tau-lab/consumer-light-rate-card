from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd

tab = pd.read_csv(Path("outputs/orders_by_zone_rate.csv"), index_col=0)
tab = tab.drop(index="All", errors="ignore")
tab.index = tab.index.astype(float).astype(int)
tab = tab.rename(columns={"9.99": "$9.99", "14.99": "$14.99"})
rates = pd.read_csv(Path("data/public/ground_40lb_list.csv")).set_index("zone")
cost = rates["list_rate"] * 0.50 + 3.60
per = pd.DataFrame({
    "$9.99": 9.99 - cost,
    "$14.99": 14.99 - cost,
}).loc[tab.index]

fig, ax = plt.subplots(figsize=(8, 4.5))
per.plot.bar(ax=ax, color=["#9a3412", "#1d4e89"])
ax.axhline(0, color="black", linewidth=0.8)
ax.set_title("$14.99 covers zone 2 (n=20). It does not cover zone 8 (n=323).")
ax.set_ylabel("Charged minus estimated cost ($ per box)")
ax.set_xlabel("UPS Ground zone from 84098")
fig.tight_layout()
fig.savefig(Path("outputs/figures/fig1_subsidy_by_zone.png"), dpi=150)
plt.close()

fig, ax = plt.subplots(figsize=(8, 4.5))
tab[["$9.99", "$14.99"]].plot.bar(ax=ax, stacked=True, color=["#9a3412", "#1d4e89"])
ax.set_title("Zones 5–8 hold the book (1,196 of 1,330)")
ax.set_ylabel("Zoned orders")
ax.set_xlabel("UPS Ground zone from 84098")
fig.tight_layout()
fig.savefig(Path("outputs/figures/fig2_volume_by_zone.png"), dpi=150)
plt.close()
print("wrote outputs/figures")