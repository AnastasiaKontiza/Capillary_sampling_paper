# Author: Anastasia Kontiza
# Date: 21/10/2024

import pandas as pd
from scipy.stats import mannwhitneyu

# Function to replace zero values with half of the minimum non-zero value for each sample group
def replace_zeros_with_half_min(df, group_columns):
    for col in group_columns:
        # Get the non-zero minimum value for the column
        non_zero_min = df[col][df[col] > 0].min()
        if pd.notna(non_zero_min):
            # Replace 0 values with half of the minimum non-zero value
            df[col] = df[col].replace(0, non_zero_min / 2)
    return df

# Load the Excel file
file_path = "Replace with your file path"  
data = pd.read_excel(file_path, sheet_name='Sheet1')

# List of group columns
name_of_first_group_columns = ['insert column names']
name_of_second_group_columns = ['insert column names']

# Apply the replacement function to both groups
data = replace_zeros_with_half_min(data, name_of_first_group_columns)
data = replace_zeros_with_half_min(data, name_of_second_group_columns)

# Initialize an empty list to store results
results = []

# Loop through each row (each lipid)
for index, row in data.iterrows():
    lipid_name = row['Metabolite name']
    
    # Extract group values
    y3x_group = pd.to_numeric(row[name_of_first_group_columns], errors='coerce').dropna().values
    dy_group = pd.to_numeric(row[name_of_second_group_columns], errors='coerce').dropna().values
    
    # Perform Mann-Whitney U test if both groups have sufficient data
    if len(name_of_first_group_columns) > 0 and len(name_of_second_group_columns) > 0:
        stat, p_value = mannwhitneyu(name_of_first_group_columns, name_of_second_group_columns)
        results.append([lipid_name, stat, p_value])

# Convert results into a DataFrame
results_df = pd.DataFrame(results, columns=['Metabolite name', 'Mann-Whitney U Statistic', 'P-value'])

# Save the results to an Excel file
output_file = 'mann_whitney_test_results_with_zero_replacement.xlsx'  # Output file name
results_df.to_excel(output_file, index=False)

print(f"Results saved to {output_file}")
