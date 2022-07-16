from bs4 import BeautifulSoup
import requests
import re
import json
import os

MAIN_CAST = [
    "Ptaszynski",
    "Harkin",
    "Murray",
    "Schreiber",
]

BASE_URL = 'https://nstaaf.fandom.com'
url = "https://nstaaf.fandom.com/wiki/List_of_Episodes_of_No_Such_Thing_As_A_Fish"

resp = requests.get(url)
url_pat = r'href="([^"]*)" title="Episode (\d+):'
episode_urls = re.findall(url_pat, resp.text)

fact_orders = {}

for i, ep_url in enumerate(episode_urls):
    resp = requests.get(BASE_URL + ep_url[0])
    soup = BeautifulSoup(resp.content, "lxml")
    fact_h = soup.find(id="Facts")

    if not fact_h:
        continue

    facts = fact_h.find_next('ol')
    if not facts:
        facts = fact_h.find_next('ul')

    if not facts:
        continue

    facts = [f.get_text() for f in facts.find_all('li')]
    fact_givers = []
    bad_info = False
    for fact in facts:
        giver = re.findall(r'\(([\w ]+)\)', fact)
        if giver:
            name = giver[0].split(' ')[-1]
            if name in MAIN_CAST:
                fact_givers.append(name)
            else:
                fact_givers.append('Guest')
        else:
            bad_info = True

    if len(fact_givers) != 4 or bad_info:
        continue

    fact_orders.update({ep_url[1]:fact_givers})


with open("fish_fact_orders.json", "w+", encoding="utf8") as fn:
    json.dump(fact_orders, fn)