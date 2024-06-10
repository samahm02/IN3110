"""
Task 4

collecting olympic statistics from wikipedia
"""

from __future__ import annotations

from pathlib import Path

from requesting_urls import get_html

from collections import defaultdict
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import re

# Countries to submit statistics for
scandinavian_countries = ["Norway", "Sweden", "Denmark"]

# Summer sports to submit statistics for
summer_sports = ["Sailing", "Athletics", "Handball", "Football", "Cycling", "Archery"]


def report_scandi_stats(url: str, sports_list: list[str], work_dir: str | Path) -> None:
    """
    Given the url, extract and display following statistics for the Scandinavian countries:

      -  Total number of gold medals for for summer and winter Olympics
      -  Total number of gold, silver and bronze medals in the selected summer sports from sport_list
      -  The best country in number of gold medals in each of the selected summer sports from sport_list

    Display the first two as bar charts, and the last as an md. table and save in a separate directory.

    Parameters:
        url (str) : url to the 'All-time Olympic Games medal table' wiki page
        sports_list (list[str]) : list of summer Olympic games sports to display statistics for
        work_dir (str | Path) : (absolute) path to your current working directory

    Returns:
        None
    """
    work_dir = Path(work_dir)

    dest_dir = work_dir / "olympic_games_results"
    dest_dir.mkdir(parents=True, exist_ok=True)

    country_dict = get_scandi_stats(url)
    
    plot_scandi_stats(country_dict, dest_dir)
    
    best_in_sport = []

    for sport in sports_list:
        sport_results = {}
        for country, data in country_dict.items():
            country_url = data["url"]
            sport_medal_data = get_sport_stats(country_url, sport)
            sport_results[country] = sport_medal_data
        
        plot_sport_medal_stats(sport_results, sport, dest_dir)
        
        best_country = find_best_country_in_sport(sport_results)
        best_in_sport.append({"Sport": sport, "Best Country": best_country})

    with open(dest_dir / "best_of_sport_by_Gold.md", "w") as md_file:
        md_file.write("Best Scandinavian country in Summer Olympic sports, based on most number of Gold medals\n")
        md_file.write("| Sport     | Best country   |\n")
        md_file.write("|:----------|:---------------|\n")
        for item in best_in_sport:
            line = f"| {item['Sport']:<10} | {item['Best Country']:<15} |\n"
            md_file.write(line)




def get_scandi_stats(
    url: str,
) -> dict[str, dict[str, str | dict[str, int]]]:
    """Given the url, extract the urls for the Scandinavian countries,
       as well as number of gold medals acquired in summer and winter Olympic games
       from 'List of NOCs with medals' table.

    Parameters:
      url (str): url to the 'All-time Olympic Games medal table' wiki page

    Returns:
      country_dict: dictionary of the form:
        {
            "country": {
                "url": "https://...",
                "medals": {
                    "Summer": 0,
                    "Winter": 0,
                },
            },
        }

        with the tree keys "Norway", "Denmark", "Sweden".
    """
    html = get_html(url)
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find('table', class_='wikitable')
    base_url = "https://en.wikipedia.org"

    country_dict = {}


    rows = table.find_all('tr')
    for row in rows[2:]:
        cols = row.find_all(["th", "td"])

        country_text = cols[0].text.strip()
        country_name = country_text.split('(')[0].strip()

        if country_name in scandinavian_countries:
            country_url = base_url + cols[0].find('a')['href']
            summer_gold = int(cols[2].text.strip())
            winter_gold = int(cols[7].text.strip())

            country_data = {
                "url": country_url,
                "medals": {
                    "Summer": summer_gold,
                    "Winter": winter_gold
                }
            }
            country_dict[country_name] = country_data

    return country_dict


def get_sport_stats(country_url: str, sport: str) -> dict[str, int]:
    """Given the url to country specific performance page, get the number of gold, silver, and bronze medals
      the given country has acquired in the requested sport in summer Olympic games.

    Parameters:
        - country_url (str) : url to the country specific Olympic performance wiki page
        - sport (str) : name of the summer Olympic sport in interest. Should be used to filter rows in the table.

    Returns:
        - medals (dict[str, int]) : dictionary of number of medal acquired in the given sport by the country
                          Format:
                          {"Gold" : x, "Silver" : y, "Bronze" : z}
    """
    html = get_html(country_url)
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find('table', class_='wikitable sortable plainrowheaders jquery-tablesorter')

    medals = {
        "Gold": 0,
        "Silver": 0,
        "Bronze": 0,
    }

    rows = table.find_all('tr')

    for row in rows[1:]:
        cols = row.find_all(["th", "td"])
        if len(cols) > 1:
            sport_name = cols[0].text.strip()
            if re.match(sport, sport_name, re.IGNORECASE):
                medals["Gold"] = int(cols[1].text.strip())
                medals["Silver"] = int(cols[2].text.strip())
                medals["Bronze"] = int(cols[3].text.strip())
                return medals

    return medals


def find_best_country_in_sport(
    results: dict[str, dict[str, int]], medal: str = "Gold"
) -> str:
    """Given a dictionary with medal stats in a given sport for the Scandinavian countries, return the country
        that has received the most of the given `medal`.

    Parameters:
        - results (dict) : a dictionary of country specific medal results in a given sport. The format is:
                        {"Norway" : {"Gold" : 1, "Silver" : 2, "Bronze" : 3},
                         "Sweden" : {"Gold" : 1, ....},
                         "Denmark" : ...
                        }
        - medal (str) : medal type to compare for. Valid parameters: ["Gold" | "Silver" |"Bronze"]. Should be used as a key
                          to the medal dictionary.
    Returns:
        - best (str) : name of the country(ies) leading in number of gold medals in the given sport
                       If one country leads only, return its name, like for instance 'Norway'
                       If two countries lead return their names separated with '/' like 'Norway/Sweden'
                       If all or none of the countries lead, return string 'None'
    """
    valid_medals = {"Gold", "Silver", "Bronze"}
    if medal not in valid_medals:
        raise ValueError(f"{medal} is an invalid parameter for ranking, must be in {valid_medals}")

    max_medal_count = -1
    best_countries = []

    for country, medal_stats in results.items():
        medal_count = medal_stats[medal]
        if medal_count > max_medal_count:
            max_medal_count = medal_count
            best_countries = [country]
        elif medal_count == max_medal_count:
            best_countries.append(country)
   
    if not best_countries or best_countries == list(results.keys()):
        return "None"
    elif len(best_countries) == 1:
        return best_countries[0]
    else:
        return "/".join(best_countries)


# Define your own plotting functions and optional helper functions


def plot_scandi_stats(
    country_dict: dict[str, dict[str, str | dict[str, int]]],
    output_parent: str | Path | None = None,
) -> None:
    """Plot the number of gold medals in summer and winter games for each of the scandi countries as bars.

    Parameters:
      results (dict[str, dict[str, int]]) : a nested dictionary of country names and the corresponding number of summer and winter
                            gold medals from 'List of NOCs with medals' table.
                            Format:
                            {"country_name": {"Summer" : x, "Winter" : y}}
      output_parent (str | Path) : parent file path to save the plot in
    Returns:
      None
    """
    countries = []
    summer_medals = []
    winter_medals = []

    for country, data in country_dict.items():
        countries.append(country)
        summer_medals.append(data["medals"]["Summer"])
        winter_medals.append(data["medals"]["Winter"])

    fig, ax = plt.subplots()
    bar_width = 0.35
    index = range(len(countries))
    
    bars1 = ax.bar(index, summer_medals, bar_width, label='Summer', color='b')
    bars2 = ax.bar([i + bar_width for i in index], winter_medals, bar_width, label='Winter', color='r')
    
    ax.set_xlabel('Country')
    ax.set_ylabel('Gold Medals')
    ax.set_title('Gold Medals by Summer and Winter Olympics')
    ax.set_xticks([i + bar_width / 2 for i in index])
    ax.set_xticklabels(countries)
    ax.legend()
    
    plt.tight_layout()
    plt.savefig(output_parent / "total_medal_ranking.png")
    plt.close()


def plot_sport_medal_stats(results: dict[str, dict[str, int]], sport: str, output_parent: str | Path) -> None:
    """
    Plot the number of gold, silver, and bronze medals in a specific sport for each of the scandi countries as bars.

    Parameters:
      results (dict[str, dict[str, int]]) : a nested dictionary of country names and the corresponding number of 
                            gold, silver, and bronze medals in a specific sport.
                            Format:
                            {"country_name": {"Gold" : x, "Silver" : y, "Bronze": z}}
      sport (str): The sport in question.
      output_parent (str | Path) : parent file path to save the plot in
    Returns:
      None
    """

    countries = list(results.keys())
    gold_counts = [results[country]["Gold"] for country in countries]
    silver_counts = [results[country]["Silver"] for country in countries]
    bronze_counts = [results[country]["Bronze"] for country in countries]
    
    x = range(len(countries))
    bar_width = 0.3
    r1 = [i - bar_width for i in x]
    r2 = x
    r3 = [i + bar_width for i in x]
    
    plt.figure(figsize=(10, 6))
    plt.bar(r1, gold_counts, width=bar_width, color='gold', label='Gold')
    plt.bar(r2, silver_counts, width=bar_width, color='silver', label='Silver')
    plt.bar(r3, bronze_counts, width=bar_width, color='#cd7f32', label='Bronze')
   
    plt.xlabel('Country')
    plt.xticks([r + bar_width for r in range(len(countries))], countries)
    plt.ylabel('Medal Count')
    plt.title(f'Medal Distribution for {sport}')
    plt.legend()
   
    output_file = output_parent / f"{sport}_medal_ranking.png"
    plt.tight_layout()
    plt.savefig(output_file)
    plt.close()


# run the whole thing if called as a script, for quick testing
if __name__ == "__main__":
    url = "https://en.wikipedia.org/wiki/All-time_Olympic_Games_medal_table"
    work_dir = Path(__file__).parent.absolute()

    report_scandi_stats(url, summer_sports, work_dir)