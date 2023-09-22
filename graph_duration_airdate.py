import matplotlib.pyplot as plt
from datetime import datetime
import json

# Load data from "fish_episode_info.json"
with open("fish_episode_info.json", "r", encoding="utf8") as json_file:
    data = json.load(json_file)

# Extract episode air dates and durations
episode_air_dates = [datetime.strptime(episode["Air Date"], "%d %B %Y") for episode in data.values()]
episode_durations = [int(episode["Duration"].split(":")[0]) for episode in data.values()]

# Create a scatter plot
plt.figure(figsize=(12, 8))
plt.scatter(episode_air_dates, episode_durations, c=episode_durations, cmap='viridis', s=100, alpha=0.7)
plt.xlabel("Episode Air Date")
plt.ylabel("Episode Duration (minutes)")
plt.title("Episode Duration vs. Air Date")
plt.colorbar(label="Episode Duration (minutes)")
plt.grid(True, linestyle='--', alpha=0.7)

# Beautify x-axis by rotating date labels
plt.xticks(rotation=45)

# plt.show()
plt.savefig('./graphs/duration_airdate.png')