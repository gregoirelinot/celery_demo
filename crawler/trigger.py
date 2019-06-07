from .spider import *
import re
from urllib.parse import *


# crawl_url.delay("https://en.wikipedia.org/wiki/Transmission_Control_Protocol").get()
# crawl_url.delay("https://en.wikipedia.org/wiki/Transmission_Control_Protocol").get()


def get_subject(wiki_url):
    subjs = re.findall(r"\/wiki\/([^\/]+)", unquote_plus(wiki_url))
    if len(subjs) > 0:
        return subjs[0]


def web_map_to_file(filename):
    with open(filename, "w") as f:
        for k in result_redis_db.scan_iter("*"):
            k = k.decode("utf-8")
            lks = list(set(map(lambda x: get_domain(urlparse(x).netloc), get_results(k))))
            f.write(",".join(([get_domain(urlparse(k).netloc)] + lks)) + "\n")


def wiki_to_file(filename):
    with open(filename, "w") as f:
        for k in result_redis_db.scan_iter("*"):
            k = k.decode("utf-8")
            lks = list(set(filter(lambda x: x is not None, map(lambda x: get_subject(x), get_results(k)))))
            subject = get_subject(k)
            if subject is not None and ":" not in subject:
                line = [subject] + lks
                f.write(",".join(line) + "\n")
