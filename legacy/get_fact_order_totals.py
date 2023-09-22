import json
import pandas as pd
import matplotlib.pyplot as plt

with open('fish_fact_orders_2.json', 'r') as fn:
    fact_orders_json = json.load(fn)

orders_total = [
    ["Ptaszynski",0,0,0,0],
    ["Harkin",0,0,0,0],
    ["Murray",0,0,0,0],
    ["Schreiber",0,0,0,0],
    ["Guest",0,0,0,0]
]

for ep, speakers in fact_orders_json.items():
    for i, speaker in enumerate(speakers):
        for orders in orders_total:
            if orders[0] == speaker:
                orders[i+1]+=1
                

  
df = pd.DataFrame(orders_total, columns=['Speaker', 'First', 'Second', 'Third', 'Fourth'])

df.plot(x='Speaker',
        kind='bar',
        stacked=False,
        title='NSTAAF Cast Speaking Order Totals',
        xlabel='',
        rot=0
        )

plt.xlabel('', rotation=0)
plt.show()
