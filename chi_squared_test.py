import pandas as pd
from scipy.stats import chi2_contingency
from data import load_episode_data

data = load_episode_data()

df_data = {"Episode": [], "Order": [], "Speaker": []}

for episode, episode_info in data.items():
    for order, speaker in enumerate(episode_info["Fact Orders"], start=1):
        if speaker != 'Guest':
            df_data["Episode"].append(episode)
            df_data["Order"].append(order)
            df_data["Speaker"].append(speaker)

df = pd.DataFrame(df_data)

contingency_table = pd.crosstab(df['Speaker'], df['Order'])

chi2, p, _, _ = chi2_contingency(contingency_table)

print(f"Chi-Square Statistic: {chi2}")
print(f"P-value: {p}")

alpha = 0.05
if p < alpha:
    print("There is a statistically significant association between speakers and speaking order.")
else:
    print("There is no statistically significant association between speakers and speaking order.")
