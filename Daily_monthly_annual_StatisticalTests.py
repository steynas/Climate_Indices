# -*- coding: utf-8 -*-
"""
Created on Sun 29 Dec 2024
Input: C:/StnData/StatisticalAnalysis/Merged_StationName_stn_cdb.csv, 
monthly_StationName.csv, annual_StationName.csv
This script reads csv file containing daily/monthly/annual station (stn)
and reanalysis (cdb) data for Tmax, Tmin, RHmax, RHmin, WSmean, SR, 
Pr and ETo. It excludes missing (NaN) values and implements the 
Wilcoxon Signed-Rank Test, Kolmogorov-Smirnov Test, and Bland-Altman 
Analysis for daily.monthly.annual data comparisons.
Outputs:
- Plots are saved in C:/StnData/StatisticalAnalysis/Plots
- Statistical test results are written to StatisticalTests_{StationName}.xlsx.
@author: SteynAS@ufs.ac.za
"""

import pandas as pd
import os
import matplotlib.pyplot as plt
from scipy.stats import wilcoxon, ks_2samp

# Function for Bland-Altman Analysis
def bland_altman_plot(data, stn_var, cdb_var, variable, selected_station, timescale):
    diff = data[stn_var] - data[cdb_var]
    mean = (data[stn_var] + data[cdb_var]) / 2

    mean_diff = diff.mean()
    std_diff = diff.std()

    plt.figure(figsize=(8, 6))
    plt.scatter(mean, diff, alpha=0.6, edgecolors='k')
    plt.axhline(mean_diff, color='red', linestyle='--', label=f'Mean Diff: {mean_diff:.2f}')
    plt.axhline(mean_diff + 1.96 * std_diff, color='blue', linestyle='--', label='Upper Limit')
    plt.axhline(mean_diff - 1.96 * std_diff, color='blue', linestyle='--', label='Lower Limit')
    plt.title(f"Bland-Altman Plot ({variable}, {timescale})")
    plt.xlabel('Mean of Station and CDB Values')
    plt.ylabel('Difference (Station - CDB)')
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()

    # Save the plot
    plot_path = f"C:/StnData/StatisticalAnalysis/Plots/bland_altman_{variable}_{timescale}_{selected_station.replace(' ', '_')}.png"
    plt.savefig(plot_path)
    plt.close()
    print(f"Bland-Altman plot saved as {plot_path}.")

# Perform Kolmogorov-Smirnov Test
def kolmogorov_smirnov_test(data, stn_var, cdb_var):
    stn_data = data[stn_var].dropna()
    cdb_data = data[cdb_var].dropna()

    ks_stat, ks_p = ks_2samp(stn_data, cdb_data)
    return ks_stat, ks_p

# Perform Wilcoxon Signed-Rank Test for paired data
def wilcoxon_signed_rank_test(data, stn_var, cdb_var):
    data_cleaned = data[[stn_var, cdb_var]].dropna()

    wilcoxon_stat, wilcoxon_p = wilcoxon(data_cleaned[stn_var], data_cleaned[cdb_var])
    return wilcoxon_stat, wilcoxon_p

# Main script
stations = [
    "Polokwane", "Mbombela", "Potchefstroom", "Bloemfontein",
    "Richards Bay", "East London", "Gqeberha", "Oudtshoorn"
]

print("Please choose a weather station from the following list:")
for idx, station in enumerate(stations, 1):
    print(f"{idx}. {station}")

while True:
    try:
        station_choice = int(input("Enter the number corresponding to your choice: "))
        if 1 <= station_choice <= len(stations):
            selected_station = stations[station_choice - 1]
            print(f"You have selected: {selected_station}")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and", len(stations))
    except ValueError:
        print("Invalid input. Please enter a number.")

# File paths
base_path = "C:/StnData/StatisticalAnalysis"
annual_file = os.path.join(base_path, f"annual_{selected_station.replace(' ', '')}.csv")
monthly_file = os.path.join(base_path, f"monthly_{selected_station.replace(' ', '')}.csv")
daily_file = os.path.join(base_path, f"Merged_{selected_station.replace(' ', '')}_stn_cdb.csv")

# Load data
annual_data = pd.read_csv(annual_file, parse_dates=["date"], date_format="%Y", index_col="date")
monthly_data = pd.read_csv(monthly_file, parse_dates=["date"], date_format="%Y-%m", index_col="date")
daily_data = pd.read_csv(daily_file, parse_dates=["Date"], date_format="%Y-%m-%d", index_col="Date")

# Variables for analysis
variables = ["Tmax", "Tmin", "RHmax", "RHmin", "WSmean", "SR", "Pr", "ETo"]

# Initialize results dictionary
results = {
    "Timescale": [],
    "Variable": [],
    "Test": [],
    "Statistic": [],
    "P-Value": [],
    "5%": [],
    "10%": []
}

# Function to perform all three tests
def perform_all_tests(data, stn_var, cdb_var, variable, timescale):
    print(f"\nAnalyzing variable: {variable}")

    # Kolmogorov-Smirnov Test
    ks_stat, ks_p = kolmogorov_smirnov_test(data, stn_var, cdb_var)
    results["Timescale"].append(timescale)
    results["Variable"].append(variable)
    results["Test"].append("Kolmogorov-Smirnov Test")
    results["Statistic"].append(ks_stat)
    results["P-Value"].append(ks_p)
    results["5%"].append("*" if ks_p < 0.05 else "")
    results["10%"].append("*" if ks_p < 0.10 else "")

    # Wilcoxon Signed-Rank Test
    wilcoxon_stat, wilcoxon_p = wilcoxon_signed_rank_test(data, stn_var, cdb_var)
    results["Timescale"].append(timescale)
    results["Variable"].append(variable)
    results["Test"].append("Wilcoxon Signed-Rank Test")
    results["Statistic"].append(wilcoxon_stat)
    results["P-Value"].append(wilcoxon_p)
    results["5%"].append("*" if wilcoxon_p < 0.05 else "")
    results["10%"].append("*" if wilcoxon_p < 0.10 else "")

    # Bland-Altman Analysis
    bland_altman_plot(data, stn_var, cdb_var, variable, selected_station, timescale)

# Annual Analysis
print("\n--- Annual Analysis ---")
for variable in variables:
    stn_var = f"stn_{variable}"
    cdb_var = f"cdb_{variable}"

    if stn_var in annual_data.columns and cdb_var in annual_data.columns:
        perform_all_tests(annual_data, stn_var, cdb_var, variable, "Annual")

# Monthly Analysis
print("\n--- Monthly Analysis ---")
for variable in variables:
    stn_var = f"stn_{variable}"
    cdb_var = f"cdb_{variable}"

    if stn_var in monthly_data.columns and cdb_var in monthly_data.columns:
        perform_all_tests(monthly_data, stn_var, cdb_var, variable, "Monthly")

# Daily Analysis
print("\n--- Daily Analysis ---")
for variable in variables:
    stn_var = f"stn_{variable}"
    cdb_var = f"cdb_{variable}"

    if stn_var in daily_data.columns and cdb_var in daily_data.columns:
        perform_all_tests(daily_data, stn_var, cdb_var, variable, "Daily")

# Save results to Excel
output_file = os.path.join(base_path, f"StatisticalTests_{selected_station.replace(' ', '')}.xlsx")
results_df = pd.DataFrame(results)
results_df.to_excel(output_file, index=False)
print(f"\nStatistical test results saved to {output_file}.")
