import matplotlib.pyplot as plt
import json
import pandas as pd

# Load data from "fish_episode_info.json"
with open("fish_episode_info.json", "r", encoding="utf8") as json_file:
    episode_info_data = json.load(json_file)

# Calculate the average fact length for each episode
average_fact_lengths = []
episode_durations = []

for episode, info in episode_info_data.items():
    facts = info["Facts"]
    total_words = sum(len(fact.split()) for fact in facts)
    average_fact_length = total_words / len(facts)
    average_fact_lengths.append(average_fact_length)
    episode_durations.append(info["Duration"])

# Create a DataFrame to store the data
data = {
    "Episode": list(episode_info_data.keys()),
    "Episode Duration (minutes)": episode_durations,
    "Average Fact Length (words)": average_fact_lengths,
}

df = pd.DataFrame(data)

# Create a line chart
plt.figure(figsize=(12, 8))

# Plot episode duration and average fact length on the same y-axis
plt.plot(df["Episode"], df["Episode Duration (minutes)"], label="Episode Duration", marker='o', color='b')
plt.plot(df["Episode"], df["Average Fact Length (words)"], label="Average Fact Length", marker='o', color='g')

plt.xlabel("Episode")
plt.ylabel("Duration (minutes) / Average Fact Length (words)")
plt.xticks(rotation=45)
plt.xticks(df["Episode"][::50])  # Show every nth episode label
plt.yticks(df["Episode Duration (minutes)"][::60])
plt.grid(False)

plt.legend()
plt.title("Episode Duration vs. Average Fact Length")
plt.tight_layout()
# plt.show()
plt.savefig('./graphs/duration_factlength.png')
