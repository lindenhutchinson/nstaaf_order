import re
import json
import requests
import logging
from bs4 import BeautifulSoup

logging.basicConfig(filename='scraper.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

MAIN_CAST = [
    "Ptaszynski",
    "Harkin",
    "Murray",
    "Schreiber",
]

BASE_URL = 'https://nstaaf.fandom.com'

def scrape_episode_info(ep_url):
    try:
        resp = requests.get(BASE_URL + ep_url)
        resp.raise_for_status()

        soup = BeautifulSoup(resp.content, "html.parser")

        air_date_elem = soup.find("div", {"data-source": "first_broadcast"})
        duration_elem = soup.find("div", {"data-source": "episode_length"})

        if not air_date_elem or not duration_elem:
            return None

        air_date = air_date_elem.find("div", class_="pi-data-value pi-font").text.strip()
        duration = duration_elem.find("div", class_="pi-data-value pi-font").text.strip()

        facts = soup.find(id="Facts")
        if not facts:
            logging.warning(f"No facts found for episode {ep_url}")
            return None

        facts = facts.find_next('ol') or facts.find_next('ul')
        if not facts:
            logging.warning(f"No facts list found for episode {ep_url}")
            return None

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

        if len(fact_givers) != 4:
            logging.warning(f"Episode {ep_url} does not have 4 fact givers.")
            return None
        if bad_info:
            logging.warning(f"Episode {ep_url} has bad info.")
            return None

        return {
            "Air Date": air_date,
            "Duration": duration,
            "Fact Orders": fact_givers,
            "Facts": facts
        }

    except requests.exceptions.RequestException as e:
        logging.error(f"Error while scraping episode {ep_url}: {str(e)}")
        return None

def scrape_episodes_data():
    episodes_url = "https://nstaaf.fandom.com/wiki/List_of_Episodes_of_No_Such_Thing_As_A_Fish"
    resp = requests.get(episodes_url)
    resp.raise_for_status()

    url_pat = r'href="([^"]*)" title="Episode (\d+):'
    episode_urls = re.findall(url_pat, resp.text)
    ep_len = len(episode_urls)
    episode_info = {}

    for i, ep_url in enumerate(episode_urls):
        print(f"Scraping episode {i + 1}/{ep_len}")

        episode_data = scrape_episode_info(ep_url[0])
        if episode_data:
            episode_info[ep_url[1]] = episode_data

    with open("fish_episode_info.json", "w", encoding="utf-8") as fn:
        json.dump(episode_info, fn, indent=4)

if __name__ == "__main__":
    scrape_episodes_data()
