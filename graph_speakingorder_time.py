import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.ticker import MaxNLocator
from data import load_episode_data

data = load_episode_data()

df_data = {"Month": [], "Order": [], "Presenter": []}

month_order = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
               "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

for episode_info in data.values():
    air_date = episode_info["Air Date"]
    month = air_date.split(' ')[1][:3].capitalize()

    for order, presenter in enumerate(episode_info["Fact Orders"], start=1):
        df_data["Month"].append(month)
        df_data["Order"].append(order)
        df_data["Presenter"].append(presenter)

df = pd.DataFrame(df_data)

participants = df["Presenter"].unique()

num_participants = len(participants)
num_columns = 2 if num_participants > 1 else 1
num_rows = (num_participants + num_columns - 1) // num_columns

fig, axs = plt.subplots(num_rows, num_columns, figsize=(15, 10))
axs = axs.flatten()

for idx, participant in enumerate(participants):
    ax = axs[idx]
    for order in range(1, 5):
        order_counts = df[df["Order"] == order]
        counts_per_month = order_counts[order_counts["Presenter"] == participant].groupby("Month").size()
        counts_per_month = counts_per_month.reindex(month_order, fill_value=0)
        ax.plot(counts_per_month.index, counts_per_month.values, marker='o', linestyle='-', label=f"Order {order}")

    ax.set_title(f"{participant}")
    ax.set_ylabel("Count")
    ax.legend()
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))

plt.xlabel("Month")
plt.xticks(range(12), month_order, rotation=45)

for i in range(num_participants, num_columns * num_rows):
    fig.delaxes(axs[i])

plt.tight_layout(h_pad=2)
plt.savefig('./graphs/order_time.png')
