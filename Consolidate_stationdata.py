# -*- coding: utf-8 -*-
"""
Created on Fri Sep  6 09:00:20 2024

This scripts takes two Excel files that contain daily station data
for different periods (may contain different columns, i.e. variables)
and consolidate them into a single file written to the same directory
Just change the name of the input and output file & path
input1 = GlenCollege_1984_1999.xlsx
input2 = GlenCollege_1999_2023.xlsx
output = Glen_Combined_1984_2023.xlsx
@author: SteynAS
"""

import os
import pandas as pd

# Define the directory and file names
directory = r'C:\StnData'
file_name_1 = 'GlenCollege_1984_1999.xlsx'
file_name_2 = 'GlenCollege_1999_2023.xlsx'
outfile_name = 'Glen_Combined_1984_2023.xlsx'

# Paths to the files
file_path_1 = os.path.join(directory, file_name_1)
file_path_2 = os.path.join(directory, file_name_2)
output_file_path = os.path.join(directory, outfile_name)

# Load the Excel files into separate DataFrames
df1 = pd.read_excel(file_path_1)
df2 = pd.read_excel(file_path_2)

# Standardize column names to avoid issues due to extra spaces or inconsistent naming
df1.columns = df1.columns.str.strip()
df2.columns = df2.columns.str.strip()

# Rename columns in df2 to match df1 where possible
df2.rename(columns={
    'Rs': 'Rs est.',
}, inplace=True)

# Combine 'Year', 'Month', and 'Day' into a single 'Date' column for both DataFrames
df1['Date'] = pd.to_datetime(df1[['Year', 'Month', 'Day']])
df2['Date'] = pd.to_datetime(df2[['Year', 'Month', 'Day']])

# Consolidate columns by filling missing values from the potential duplicate columns
# Here, we assume the columns have similar meanings and data ranges.

# Consolidate 'Rs est.' and 'Rs est..1'
if 'Rs est..1' in df1.columns:
    df1['Rs est.'] = df1['Rs est.'].combine_first(df1['Rs est..1'])

# Consolidate 'Ra' and 'Ra.1'
if 'Ra.1' in df1.columns:
    df1['Ra'] = df1['Ra'].combine_first(df1['Ra.1'])

# Consolidate '(δ)' and '(δ).1'
if '(δ).1' in df1.columns:
    df1['(δ)'] = df1['(δ)'].combine_first(df1['(δ).1'])

# Consolidate '(ωs)' and '(ωs).1'
if '(ωs).1' in df1.columns:
    df1['(ωs)'] = df1['(ωs)'].combine_first(df1['(ωs).1'])

# Consolidate '(dr)' and '(dr).1'
if '(dr).1' in df1.columns:
    df1['(dr)'] = df1['(dr)'].combine_first(df1['(dr).1'])

# Drop the now redundant columns after consolidation
df1.drop(columns=['Rs est..1', 'Ra.1', '(δ).1', '(ωs).1', '(dr).1'], errors='ignore', inplace=True)

# Concatenate the two DataFrames, preserving all columns
combined_df = pd.concat([df1, df2], ignore_index=True)

# Display the new shape and column names after dropping duplicates
print("\nShape of the cleaned dataset:", combined_df.shape)
print("\nColumn names after consolidating duplicates:")
print(combined_df.columns)

# Display the first few rows of the cleaned DataFrame to confirm the results
print("\nFirst 5 rows of the cleaned dataset:")
print(combined_df.head())

# Save the cleaned DataFrame to a new Excel file if needed
combined_df.to_excel(output_file_path, index=False)
print(f"\nCombined data saved to: {output_file_path}")
