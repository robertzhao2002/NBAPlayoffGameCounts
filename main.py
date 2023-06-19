from collections import defaultdict
from bs4 import BeautifulSoup
import requests
import matplotlib.pyplot as plt


def get_suffix(year):
    year = int(year)
    if 1947 <= year <= 1950:
        return "BAA_{}.html".format(year)
    else:
        return "NBA_{}.html".format(year)


URL_PREFIX = "https://www.basketball-reference.com/playoffs/"
USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0"
)
HEADERS = {"user-agent": USER_AGENT}

year = input()
URL = URL_PREFIX + get_suffix(year)
print(URL)

resp = requests.get(URL, headers=HEADERS)
soup = BeautifulSoup(resp.content, "html.parser")
series_row = soup.find_all("table", {"id": "all_playoffs"})[0].find_all(
    "tr", {"class": None}
)

series_frequency = defaultdict(int)

for t in series_row:
    series_score_element = t.find_all("td")
    if len(series_score_element) == 3:
        if series_score_element[1].find_all("a") != None:
            score_list = series_score_element[1].text[-5:-2].split("-")
            winner_games = int(score_list[0])
            loser_games = int(score_list[1])
            # print(winner_games, loser_games)
            series_frequency[str(winner_games + loser_games)] += 1
            if loser_games == 0:
                series_frequency["sweeps"] += 1
            if winner_games - loser_games == 1:
                series_frequency["max games"] += 1

print(series_frequency)
sorted_game_counts = sorted(series_frequency.keys())
sorted_values = [series_frequency[key] for key in sorted_game_counts]

plt.bar(sorted_game_counts, sorted_values)
plt.title("{} NBA Playoffs".format(year))
plt.show()
