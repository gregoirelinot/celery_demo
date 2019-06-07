from celery import Celery
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from urllib.parse import urljoin
import redis
import json
import random

result_redis_db = redis.Redis(host='localhost', port=6379, db=5)

app = Celery('tasks')
app.config_from_object("celeryconfig", force=True)


def extract_links(content):
    soup = BeautifulSoup(content, 'html.parser')
    links = soup.select("a[href]")
    return [link.attrs['href'] for link in links]


def is_http_or_fragment(link):
    parsed_link = urlparse(link)
    return parsed_link.scheme in ('https', 'http', '')


def is_different_link(link):
    return len(link) > 0

def is_wikipedia(link):
    p = urlparse(link)
    return p.netloc.endswith("wikipedia.org")

def filter_links(links):
    links = filter(is_http_or_fragment, links)
    return filter(is_different_link, links)


def repair_link(base):
    def _repair(link):
        if urlparse(link).netloc == '':
            link += '' if link.startswith('/') else '/'
            link = urljoin(base, link)
        return link

    return _repair


def get_domain(netloc):
    return ".".join(netloc.split('.')[-2:])


def is_same_domain(netloc_1, netloc_2):
    return get_domain(netloc_1) == get_domain(netloc_2)


def get_results(url):
    global result_redis_db
    results = result_redis_db.get(url)
    if results is None:
        return []
    else:
        return json.loads(results)


def set_results(url, links):
    global result_redis_db
    results_json = json.dumps(links)
    result_redis_db.set(url, results_json)


def store_result(base, links):
    base_results = get_results(base)
    full_results = list(set(base_results + links))
    set_results(base, full_results)


def add_job(links, depth):
    for l in links[:10]:
        crawl_url.delay(l, depth + 1)


@app.task
def crawl_url(url, depth=0):
    print("[{}] : {}".format(depth, url))
    if depth > 400:
        return
    req = requests.get(url)
    links = extract_links(req.content)
    links = filter_links(links)
    links = set(links)
    links = list(map(repair_link(url), links))
    links = list(filter(is_wikipedia,links))
    add_job(links, depth)
    store_result(url, links)
    print(links)
