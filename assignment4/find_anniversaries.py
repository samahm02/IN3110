"""
Task 3

Collecting anniversaries from Wikipedia
"""
from __future__ import annotations

from pathlib import Path

import pandas as pd

from bs4 import BeautifulSoup

import re

import requests

# Month names to submit for, from Wikipedia:Selected anniversaries namespace
months_in_namespace = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
]


def extract_anniversaries(html: str, month: str) -> list[str]:
    """Extract all the passages from the html which contain an anniversary, and save their plain text in a list.
        For the pages in the given namespace, all the relevant passages start with a month href
         <p>
            <b>
                <a href="/wiki/April_1" title="April 1">April 1</a>
            </b>
            :
            ...
        </p>

    Parameters:
        - html (str): The html to parse
        - month (str): The month in interest, the page name of the Wikipedia:Selected anniversaries namespace

    Returns:
        - ann_list (list[str]): A list of the highlighted anniversaries for a given month
                                The format of each element in the list is:
                                '{Month} {day}: Event 1 (maybe some parentheses); Event 2; Event 3, something, something\n'
                                {Month} can be any month in the namespace and {day} is a number 1-31
    """
    # Parse the HTML using BeautifulSoup.
    soup = BeautifulSoup(html, 'html.parser')

    # Get all the paragraphs.
    paragraphs = soup.find_all("p")

    # Filter the passages to keep only the highlighted anniversaries.
    ann_list = []
    for paragraph in paragraphs:
        anchor = paragraph.a
        if anchor and f'/{month}_' in anchor.get('href'):
            # Extract the date
            date = anchor.get_text().strip()
            
            # Check if paragraph starts with the date
            if paragraph.get_text().startswith(date):
                # Get the event text by removing the date
                events_text = paragraph.get_text().replace(date, '').strip()
                
                # Combine the date and events, remove trailing punctuation if any
                ann_text = f"{date}{events_text}".rstrip(": ")
                
                ann_list.append(ann_text)

    return ann_list
    


def anniversary_list_to_df(ann_list: list[str]) -> pd.DataFrame:
    """Transform the list of anniversaries into a pandas dataframe.

    Parameters:
        ann_list (list[str]): A list of the highlighted anniversaries for a given month
                                The format of each element in the list is:
                                '{Month} {day}: Event 1 (maybe some parenthesis); Event 2; Event 3, something, something\n'
                                {Month} can be any month in months list and {day} is a number 1-31
    Returns:
        df (pd.Dataframe): A (dense) dataframe with columns ["Date"] and ["Event"] where each row represents a single event
    """
    # Initialize lists to store date and event data
    dates = []
    events = []

    for anniversary in ann_list:
        parts = anniversary.split(":", 1)
        if len(parts) == 2:
            date, event_str = parts
            date = date.strip()
            event_str = event_str.strip()
            event_list = re.split(r';(?![^()]*\))', event_str)

            for event in event_list:
                event = event.strip()
                if event:
                    dates.append(date)
                    events.append(event)

    df = pd.DataFrame({"Date": dates, "Event": events})
    return df


def anniversary_table(
    namespace_url: str, month_list: list[str], work_dir: str | Path
) -> None:
    """Given the namespace_url and a month_list, create a markdown table of highlighted anniversaries for all of the months in list,
        from Wikipedia:Selected anniversaries namespace

    Parameters:
        - namespace_url (str):  Full url to the "Wikipedia:Selected_anniversaries/" namespace
        - month_list (list[str]) - List of months of interest, referring to the page names of the namespace
        - work_dir (str | Path) - (Absolute) path to your working directory

    Returns:
        None
    """
    work_dir = Path(work_dir)
    output_dir = work_dir / "tables_of_anniversaries"
    output_dir.mkdir(parents=True, exist_ok=True)

    for month in month_list:
        page_url = f"{namespace_url}{month}"

        # Extract the html from the URL
        response = requests.get(page_url)
        html = response.text

        # Get the list of anniversaries
        ann_list = extract_anniversaries(html, month)

        # Render to a dataframe
        df = anniversary_list_to_df(ann_list)

        if not df.empty:
            # Convert to an .md table
            table = df.to_markdown()
            # Save the output
            output_file = output_dir / f"anniversaries_{month.lower()}.md"
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(table)
        else:
            # Debugging statement
            print(f"DataFrame is empty for {month}")


if __name__ == "__main__":
    work_dir = Path.cwd()  # Use the current working directory
    namespace_url = "https://en.wikipedia.org/wiki/Wikipedia:Selected_anniversaries/"
    
    tables_dir = work_dir / "tables_of_anniversaries"
    tables_dir.mkdir(parents=True, exist_ok=True)

    for month in months_in_namespace:
        anniversary_table(namespace_url, [month], work_dir)