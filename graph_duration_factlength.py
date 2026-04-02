import matplotlib.pyplot as plt
import pandas as pd
from data import load_episode_data

episode_info_data = load_episode_data()

average_fact_lengths = []
episode_durations = []

for episode, info in episode_info_data.items():
    facts = info["Facts"]
    total_words = sum(len(fact.split()) for fact in facts)
    average_fact_length = total_words / len(facts)
    average_fact_lengths.append(average_fact_length)
    episode_durations.append(info["Duration"])

data = {
    "Episode": list(episode_info_data.keys()),
    "Episode Duration (minutes)": episode_durations,
    "Average Fact Length (words)": average_fact_lengths,
}

df = pd.DataFrame(data)

plt.figure(figsize=(12, 8))
plt.plot(df["Episode"], df["Episode Duration (minutes)"], label="Episode Duration", marker='o', color='b')
plt.plot(df["Episode"], df["Average Fact Length (words)"], label="Average Fact Length", marker='o', color='g')
plt.xlabel("Episode")
plt.ylabel("Duration (minutes) / Average Fact Length (words)")
plt.xticks(df["Episode"][::50], rotation=45)
plt.yticks(df["Episode Duration (minutes)"][::60])
plt.grid(False)
plt.legend()
plt.title("Episode Duration vs. Average Fact Length")
plt.tight_layout()
plt.savefig('./graphs/duration_factlength.png')
