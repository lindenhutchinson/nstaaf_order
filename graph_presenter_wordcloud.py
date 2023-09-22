import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import json
import re
# Load the JSON data
with open('fish_episode_info.json', 'r') as file:
    data = json.load(file)

# Create a DataFrame from the JSON data
df = pd.DataFrame.from_dict(data, orient='index')

# Initialize a dictionary to store presenter preferences
presenter_preferences = {}

# Loop through each episode and analyze presenter preferences
for index, row in df.iterrows():
    fact_orders = row['Fact Orders']
    for presenter, facts in zip(fact_orders, row['Facts']):
        # Split facts into words and remove punctuation
        facts = re.sub(r'((\[\d\])? \(.+\))$', '', facts)
        words = ''.join(c if c.isalnum() or c.isspace() else ' ' for c in facts).split()
        
        if presenter not in presenter_preferences:
            presenter_preferences[presenter] = []
        presenter_preferences[presenter].extend(words)

# Create word clouds for each presenter
for presenter, words in presenter_preferences.items():
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(' '.join(words))
    
    plt.figure(figsize=(8, 4))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.title(f"{presenter}")
    plt.axis('off')
    # plt.show()
    plt.savefig(f'./graphs/wordcloud_{presenter.lower()}.png')
    