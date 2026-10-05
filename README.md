# Consumer Light rate vs a 40 lb UPS Ground parcel

$9.99 Light was not an expectable loss on this book. The May 2019 move to $14.99 cut the per-box hole by about $5 and did not close zones 6–8, which held the volume.

## What this is / is not

Consumer parcel card only. Paid US orders for the loss-leader bassinet carton, UPS Ground, origin 84098. Sheet-only orders went USPS and are out. Enterprise healthcare shipped freight and is out.

Order-level files are local only and are not in this repo. Shareable outputs are zone aggregates. Cost is published 40 lb Ground daily list times a discount, plus a residential line. Not an invoice. No claim that the subsidy was eliminated.

## 60-second tour

1. `docs/decision.md` — the decision and the discount bounds.
2. `outputs/figures/fig1_subsidy_by_zone.png` — charged minus estimated cost, by zone.
3. `outputs/figures/fig2_volume_by_zone.png` — where the orders sat.
4. `outputs/orders_by_zone_rate.csv` — the counts behind both figures.

## How to run

From the project root, with the venv on:

```powershell
python src\make_figures.py
