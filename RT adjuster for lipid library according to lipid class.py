#Author: Anastasia Kontiza
#Date: 4/10/2024

import pandas as pd

# Load the file as a text file
file_path = "" # Replace with your file path
data = pd.read_csv(file_path, sep='\t')  # or sep=',' if it's comma-separated

# Define the name patterns to apply shifts for
name_patterns = ['DG', 'PC', 'PE', 'SM', 'TG', 'Cer', 'PI', 'PS', 'PG']

# Ask the user for RT shift for each name pattern
shifts = {}
for pattern in name_patterns:
    shifts[pattern] = float(input(f"Enter the RT shift for names with '{pattern}': "))

# Apply the shifts to the corresponding rows based on the pattern
for key, shift in shifts.items():
    data.loc[data['Name'].str.contains(key), 'RT'] += shift

# Save the modified data as a text file
output_file_path = 'modified_file.txt'
data.to_csv(output_file_path, sep='\t', index=False)

print(f"Modified file saved as {output_file_path}")