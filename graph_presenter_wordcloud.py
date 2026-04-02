import matplotlib.pyplot as plt
from wordcloud import WordCloud
import pandas as pd
import re
from data import load_episode_data

data = load_episode_data()

df = pd.DataFrame.from_dict(data, orient='index')

presenter_preferences = {}

for index, row in df.iterrows():
    fact_orders = row['Fact Orders']
    for presenter, facts in zip(fact_orders, row['Facts']):
        facts = re.sub(r'((\[\d\])? \(.+\))$', '', facts)
        words = ''.join(c if c.isalnum() or c.isspace() else ' ' for c in facts).split()

        if presenter not in presenter_preferences:
            presenter_preferences[presenter] = []
        presenter_preferences[presenter].extend(words)

for presenter, words in presenter_preferences.items():
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(' '.join(words))

    plt.figure(figsize=(8, 4))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.title(f"{presenter}")
    plt.axis('off')
    plt.savefig(f'./graphs/wordcloud_{presenter.lower()}.png')
