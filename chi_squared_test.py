import json
import pandas as pd
from scipy.stats import chi2_contingency

# Load data from the JSON file
with open("fish_episode_info.json", "r", encoding="utf8") as json_file:
    data = json.load(json_file)

# Create a DataFrame to store the data
df_data = {"Episode": [], "Order": [], "Speaker": []}

for episode, episode_info in data.items():
    for order, speaker in enumerate(episode_info["Fact Orders"], start=1):
        if speaker != 'Guest':
            
            df_data["Episode"].append(episode)
            df_data["Order"].append(order)
            df_data["Speaker"].append(speaker)

df = pd.DataFrame(df_data)

# Create a contingency table
contingency_table = pd.crosstab(df['Speaker'], df['Order'])

# Perform the Chi-Square Test of Independence
chi2, p, _, _ = chi2_contingency(contingency_table)

# Print the results
print(f"Chi-Square Statistic: {chi2}")
print(f"P-value: {p}")

# Interpret the results
alpha = 0.05
if p < alpha:
    print("There is a statistically significant association between speakers and speaking order.")
else:
    print("There is no statistically significant association between speakers and speaking order.")
