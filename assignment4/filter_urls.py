"""
Task 1.2, 1.3

Filtering URLs from HTML
"""

from __future__ import annotations

import re
from urllib.parse import urljoin, urlparse


def find_urls(
    html: str,
    base_url: str = "https://en.wikipedia.org",
    output: str | None = None,
) -> set[str]:
    """
    Find all the url links in a html text using regex

    Arguments:
        html (str): html string to parse
        base_url (str): the base url to the wikipedia.org pages
        output (Optional[str]): file to write to if wanted
    Returns:
        urls (Set[str]) : set with all the urls found in html text
    """
    anchor_tag_pattern = re.compile(r'<a\s+(?:[^>]*?\s+)?href="([^"]*)"[^>]*>', re.IGNORECASE)
    urls = set()

    anchor_tags = anchor_tag_pattern.findall(html)

    for href in anchor_tags:
        if href.startswith("#"):
            continue

        full_url = urljoin(base_url, href)

        full_url = full_url.split('#')[0]

        urls.add(full_url)

    if output:
        with open(output, 'w') as file:
            for url in urls:
                file.write(url + '\n')

    return urls


def find_articles(html: str, output: str | None = None) -> set[str]:
    """Finds all the wiki articles inside a html text. Make call to find urls, and filter
    arguments:
        - text (str) : the html text to parse
        - output (str, optional): the file to write the output to if wanted
    returns:
        - (Set[str]) : a set with urls to all the articles found
    """
    urls = find_urls(html)

    pattern = r"^https?://[a-z]+\.(wikipedia\.org)/wiki/[^:]+$"
    articles = set()

    for url in urls:
        if re.match(pattern, url):
            articles.add(url)

    if output:
        with open(output, 'w') as file:
            for article in articles:
                file.write(article + '\n')

    return articles


## Regex example
def find_img_src(html: str):
    """Find all src attributes of img tags in an HTML string

    Args:
        html (str): A string containing some HTML.

    Returns:
        src_set (set): A set of strings containing image URLs

    The set contains every found src attribute of an img tag in the given HTML.
    """
    # img_pat finds all the <img alt="..." src="..."> snippets
    # this finds <img and collects everything up to the closing '>'
    img_pat = re.compile(r"<img[^>]+>", flags=re.IGNORECASE)
    # src finds the text between quotes of the `src` attribute
    src_pat = re.compile(r'src="([^"]+)"', flags=re.IGNORECASE)
    src_set = set()
    # first, find all the img tags
    for img_tag in img_pat.findall(html):
        # then, find the src attribute of the img, if any
        match = src_pat.search(img_tag)
        if match:
            src_set.add(match.group(1))
    return src_set
