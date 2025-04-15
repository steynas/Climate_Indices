# -*- coding: utf-8 -*-
"""
Plot ONI evolution by water year (JASONDJFMAMJ) with staggered season labels,
highlighting the most extreme El Niño and La Niña years.

Created April 2025
@author: SteynAS@ufs.ac.za
"""

import pandas as pd
import matplotlib.pyplot as plt

# === Load ONI Data ===
oni_file_path = "C:/ENSO/ONI_classification_results.xlsx"
oni_df = pd.read_excel(oni_file_path)
oni_df["Date"] = pd.to_datetime(oni_df["DATE"], format="%Y/%m/%d %H:%M:%S")
oni_df["Year"] = oni_df["Date"].dt.year
oni_df["Month"] = oni_df["Date"].dt.month
oni_df["ANOM"] = oni_df["ANOM"].astype(float)

# Assign water years (July to June)
oni_df["WaterYear"] = oni_df.apply(
    lambda row: f"{row['Year']}/{row['Year']+1}" if row["Month"] >= 7 else f"{row['Year']-1}/{row['Year']}",
    axis=1
)

oni_df = oni_df[(oni_df["WaterYear"] >= "1982/1983") & (oni_df["WaterYear"] <= "2023/2024")]

# Identify the most extreme El Niño and La Niña years
el_nino_season = oni_df.groupby("WaterYear")["ANOM"].max().idxmax()
la_nina_season = oni_df.groupby("WaterYear")["ANOM"].min().idxmin()

# Month setup
month_order = [7, 8, 9, 10, 11, 12, 1, 2, 3, 4, 5, 6]
month_labels = ["Jul", "Aug", "Sep", "Oct", "Nov", "Dec", "Jan", "Feb", "Mar", "Apr", "May", "Jun"]
month_label_indices = {label: i for i, label in enumerate(month_labels)}
label_months = ["Sep", "Oct", "Nov", "Dec", "Jan", "Feb", "Mar"]
label_positions = {i: (label_months[i], 2) for i in range(7)}

def format_water_year(wy):
    parts = wy.split("/")
    start = int(parts[0])
    end = int(parts[1])
    return f"{start}/{str(end)[-2:]}"

# === Plot ===
fig, ax = plt.subplots(figsize=(15, 8))
cmap = plt.get_cmap("viridis")
unique_years = sorted(oni_df["WaterYear"].unique())
norm = plt.Normalize(0, len(unique_years))

for i, (water_year, group) in enumerate(oni_df.groupby("WaterYear")):
    group = group[group["Month"].isin(month_order)]
    group["MonthOrder"] = group["Month"].apply(lambda m: month_order.index(m))
    group_sorted = group.sort_values("MonthOrder")
    label_group = i % 7
    label_month, _ = label_positions[label_group]
    label_index = month_label_indices[label_month]

    if water_year == el_nino_season:
        color = "darkred"
        alpha = 1.0
        linewidth = 2.5
        fontweight = 'bold'
    elif water_year == la_nina_season:
        color = "darkblue"
        alpha = 1.0
        linewidth = 2.5
        fontweight = 'bold'
    else:
        color = cmap(norm(i))
        alpha = 0.5
        linewidth = 1
        fontweight = 'normal'

    ax.plot(
        range(len(month_labels)),
        group_sorted["ANOM"],
        color=color,
        alpha=alpha,
        linewidth=linewidth
    )

    if not group_sorted.empty and label_index < len(group_sorted):
        y_val = group_sorted["ANOM"].values[label_index]
        ax.text(
            label_index, y_val, format_water_year(water_year),
            fontsize=8, alpha=alpha, ha="center", va="center",
            fontweight=fontweight, color=color,
            bbox=dict(facecolor='white', edgecolor='none', pad=0.5)
        )

# === Final Touches ===
ax.set_ylabel("Oceanic Niño Index (ONI)")
ax.set_xlabel("Month")
ax.axhline(0, color="black", linewidth=0.8)
ax.axhline(0.5, color="black", linestyle="--", linewidth=0.8)
ax.axhline(-0.5, color="black", linestyle="--", linewidth=0.8)
ax.set_ylim(-3, 3)
ax.set_xlim(0, len(month_labels) - 1)
ax.set_xticks(range(len(month_labels)))
ax.set_xticklabels(month_labels)
ax.set_yticks([x * 0.5 for x in range(-6, 7)])  # Add tick every 0.5 from -3 to 3
ax.tick_params(axis='y', pad=8)  # Add spacing between tick marks and labels
ax.grid(True, linestyle="--", alpha=0.5)
plt.tight_layout()
plt.show()