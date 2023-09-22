import matplotlib.pyplot as plt
import pandas as pd
import json
from matplotlib.ticker import MaxNLocator

# Load data from "fish_episode_info.json"
with open("fish_episode_info.json", "r", encoding="utf8") as json_file:
    data = json.load(json_file)

# Create a DataFrame to store the data
df_data = {"Month": [], "Order": [], "Count": []}

# Define the order of months
month_order = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
]
month_order = [m[:3] for m in month_order]

for episode_info in data.values():
    air_date = episode_info["Air Date"]
    month = air_date.split(' ')[1][:3]
    month = month.capitalize()

    for order, presenter in enumerate(episode_info["Fact Orders"], start=1):
        df_data["Month"].append(f"{month}")
        df_data["Order"].append(order)
        df_data["Count"].append(presenter)

df = pd.DataFrame(df_data)

# Get unique participants
participants = df["Count"].unique()

# Calculate number of rows and columns based on the number of participants
num_participants = len(participants)
num_columns = 2 if num_participants > 1 else 1  # Adjust the number of columns
num_rows = (num_participants + num_columns - 1) // num_columns

# Create subplots based on the number of participants
fig, axs = plt.subplots(num_rows, num_columns, figsize=(15, 10))
axs = axs.flatten()  # Flatten the array for indexing

for idx, participant in enumerate(participants):
    ax = axs[idx]
    for order in range(1, 5):
        order_counts = df[df["Order"] == order]
        counts_per_month = order_counts[order_counts["Count"] == participant].groupby("Month").size()

        # Reorder the counts to start with January and finish with December
        counts_per_month = counts_per_month.reindex(month_order, fill_value=0)

        ax.plot(counts_per_month.index, counts_per_month.values, marker='o', linestyle='-', label=f"Order {order}")

    ax.set_title(f"{participant}")
    ax.set_ylabel("Count")
    ax.legend()

    # Display y-axis labels as integers only
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))

plt.xlabel("Month")
plt.xticks(range(12), month_order, rotation=45)  # Set x-axis ticks for each month

# Remove any unused subplots
for i in range(num_participants, num_columns * num_rows):
    fig.delaxes(axs[i])

# Adjust spacing for the subplots
plt.tight_layout(h_pad=2)

# plt.show()
plt.savefig('./graphs/order_time.png')
