"""
Task 1.1 - requesting HTML documents with HTTP
"""
from __future__ import annotations

import requests


def get_html(url: str, params: dict | None = None, output: str | None = None):
    """Get an HTML page and return its contents.

    Args:
        url (str):
            The URL to retrieve.
        params (dict, optional):
            URL parameters to add.
        output (str, optional):
            (optional) path where output should be saved.
    Returns:
        html (str):
            The HTML of the page, as text.
    """
    # passing the optional parameters argument to the get function
    response = None

    if params:
        response = requests.get(url, params=params)
    else: response = requests.get(url)

    response.raise_for_status()

    html_str = response.text

    if output:
        with open(output, 'w') as file:
            file.write(url + '\n')
            file.write(html_str)

    return html_str
