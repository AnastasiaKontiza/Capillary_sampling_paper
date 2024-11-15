# Author: Anastasia Kontiza
# Date: 16/10/2024


import matplotlib.pyplot as plt
from matplotlib_venn import venn2

# Define the values for the sets
only_set1 = 29  # The blue area (Yokogawa tips)
only_set2 = 35  # The red area (Humanix tips)
common_area = 151  # The overlapping area

# Create a Venn diagram with labels
plt.figure(figsize=(6,6))
venn = venn2(subsets=(only_set1, only_set2, common_area), set_labels=('Yokogawa tips', 'Humanix tips'))

# Customize the colors for the areas
venn.get_label_by_id('10').set_text(only_set1)  # Set 1 only (left)
venn.get_label_by_id('01').set_text(only_set2)  # Set 2 only (right)
venn.get_label_by_id('11').set_text(common_area)  # Overlap

# Set the colors for the circles
venn.get_patch_by_id('10').set_color('blue')  # Set 1 only (left)
venn.get_patch_by_id('01').set_color('red')  # Set 2 only (right)
venn.get_patch_by_id('11').set_color('purple')  # Overlapping area (mix of blue and red)

# Show the diagram
plt.title('Venn Diagram: Yokogawa Tips vs Humanix Tips 100%')
plt.show()
