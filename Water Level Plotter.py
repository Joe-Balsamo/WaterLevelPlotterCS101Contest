__author__ = 'jbalsamo'

from bs4 import BeautifulSoup
import urllib


def get_page(url):
    try:
        return urllib.urlopen(url).read()
    except:
        return ""


def get_next_target(page):
    start_link = page.find('<a href=')
    if start_link == -1:
        return None, 0
    start_quote = page.find('"', start_link)
    end_quote = page.find('"', start_quote + 1)
    url = page[start_quote + 1:end_quote]
    return url, end_quote


def get_all_links(page):
    links = []
    while True:
        url, endpos = get_next_target(page)
        if url:
            links.append(url)
            page = page[endpos:]
        else:
            break
    return links


def union(a, b):
    for e in b:
        if e not in a:
            a.append(e)


def add_page_to_index(index, url, content):
    words = content.split()
    for word in words:
        add_to_index(index, word, url)


def add_to_index(index, keyword, url):
    if keyword in index:
        index[keyword].append(url)
    else:
        index[keyword] = [url]


def crawl_web(seed): # returns index, graph of inlinks
    tocrawl = [seed]
    crawled = []
    graph = {}  # <url>, [list of pages it links to]
    index = {}
    #    while tocrawl:
    page = tocrawl.pop()
    if page not in crawled:
        content = get_page(page)
        soup = BeautifulSoup(content)
        blockText = soup.findAll(text="Miramar")[0].parent.parent.parent
        blockText = (blockText.get_text())
        print blockText.strip()
        add_page_to_index(index, page, content)
        outlinks = get_all_links(content)
        graph[page] = outlinks
        union(tocrawl, outlinks)
        crawled.append(page)
    return index, graph

crawl_web('http://www.sandiego.gov/water/recreation/levels.shtml')

