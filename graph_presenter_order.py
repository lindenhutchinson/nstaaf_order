import matplotlib.pyplot as plt
import pandas as pd
import json

# Load data from "fish_episode_info.json"
with open("fish_episode_info.json", "r", encoding="utf8") as json_file:
    data = json.load(json_file)

# Create a DataFrame to store the data
df_data = {"Presenter": [], "Fact 1": [], "Fact 2": [], "Fact 3": [], "Fact 4": []}

for episode_info in data.values():
    fact_orders = episode_info["Fact Orders"]
    for presenter in fact_orders:
        if presenter not in df_data["Presenter"]:
            df_data["Presenter"].append(presenter)
            df_data["Fact 1"].append(0)
            df_data["Fact 2"].append(0)
            df_data["Fact 3"].append(0)
            df_data["Fact 4"].append(0)

    for i, presenter in enumerate(fact_orders):
        order_column = f"Fact {i + 1}"
        df_data[order_column][df_data["Presenter"].index(presenter)] += 1

df = pd.DataFrame(df_data)

# Create a stacked bar graph
fig, ax = plt.subplots(figsize=(12, 8))

order_columns = ["Fact 1", "Fact 2", "Fact 3", "Fact 4"]
bottom = [0] * len(df)

for order_column in order_columns:
    ax.bar(df["Presenter"], df[order_column], label=order_column, bottom=bottom)
    bottom = [sum(x) for x in zip(bottom, df[order_column])]

ax.set_ylabel("Number of Times Spoken")
ax.set_title("Number of Times Each Host Gave Facts in Each Particular Order")
ax.legend(title="Order")
plt.xticks(rotation=45)
plt.tight_layout()

# plt.show()
plt.savefig('./graphs/presenter_order.png')
