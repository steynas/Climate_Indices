# -*- coding: utf-8 -*-
"""
Created on Thu Nov 14 16:23:49 2024

@author: steynas
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import spei

# Function to calculate SPEI for different scales
def spei_package_calculation_multi_scale(precipitation, pet, scales=[3, 6, 12]):
    # Calculate climatic water balance
    water_balance = pd.Series(precipitation - pet, index=pd.date_range(start='1980-01', periods=len(precipitation), freq='ME'))
    
    # Dictionary to store SPEI results for different scales
    spei_results = {}
    
    for scale in scales:
        # Calculate SPEI using the spei package
        spei_values = spei.spei(water_balance, timescale=scale)
        
        # Ensure the output has the same length as the input
        spei_values = spei_values.reindex(water_balance.index, fill_value=np.nan)
        
        # Store results in the dictionary
        spei_results[f'SPEI-{scale}'] = spei_values
    
    # Combine results into a DataFrame
    spei_df = pd.DataFrame(spei_results)
    spei_df['Month'] = spei_df.index  # Include 'Month' as a column for plotting
    
    return spei_df

# Generate shared sample data
np.random.seed(42)
months = pd.date_range(start='1980-01', periods=240, freq='ME')
precipitation = np.random.uniform(30, 120, len(months))  # Random precipitation data (mm)
pet = np.random.uniform(20, 100, len(months))  # Random PET data (mm)

# Calculate SPEI for 3-, 6-, and 12-month scales
spei_df = spei_package_calculation_multi_scale(precipitation, pet, scales=[3, 6, 12])

# Display results for review
print(spei_df)

# Plot the SPEI for different scales
plt.figure(figsize=(14, 8))
for scale in [3, 6, 12]:
    plt.plot(spei_df['Month'], spei_df[f'SPEI-{scale}'], label=f'SPEI-{scale}')

plt.axhline(0, color='black', linestyle='--', linewidth=1)
plt.title('SPEI at 3-, 6-, and 12-Month Scales')
plt.xlabel('Month')
plt.ylabel('SPEI Value')
plt.legend()
plt.grid(True)
plt.show()
