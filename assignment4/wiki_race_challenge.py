"""
Bonus task
"""
from __future__ import annotations
from collections import deque

from filter_urls import find_articles
from requesting_urls import get_html



from threading import Thread, Lock

lock = Lock()

def threaded_find_links(current_url, path, stack, visited):
    global lock
    print(f"Checking: {current_url}")

    if current_url == finish:
        return path
    if current_url not in visited:
        with lock:
            visited.add(current_url)
            
        html_content = get_html(current_url)
        article_links = find_articles(html_content)
        
        en_wikipedia_links = [link for link in article_links if link.startswith("https://en.wikipedia.org/wiki/")]
        
        with lock:
            for link in en_wikipedia_links:
                if link not in visited:
                    stack.append((link, path + [link]))

def find_path(start: str, finish: str) -> list[str]:
    """Find the shortest path from `start` to `finish`

    Arguments:
      start (str): wikipedia article URL to start from
      finish (str): wikipedia article URL to stop at

    Returns:
      urls (list[str]):
        List of URLs representing the path from `start` to `finish`.
        The first item should be `start`.
        The last item should be `finish`.
        All items of the list should be URLs for wikipedia articles.
        Each article should have a direct link to the next article in the list.
    """
    visited = set()
    stack = [(start, [start])]
    
    while stack:
        threads = []

        for _ in range(10):
            if stack:
                current_url, path = stack.pop()
                t = Thread(target=threaded_find_links, args=(current_url, path, stack, visited))
                t.start()
                threads.append(t)
                
        for t in threads:
            t.join()

        if any([url == finish for url, _ in stack]):
            for url, path in stack:
                if url == finish:
                    return path

    return []



if __name__ == "__main__":
    start = "https://en.wikipedia.org/wiki/Python_(programming_language)"
    finish = "https://en.wikipedia.org/wiki/Peace"
    path = find_path(start, finish)
    print(f"Got from {start} to {finish} in {len(path)-1} links")
    print(path)