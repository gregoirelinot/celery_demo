from celery import Celery
from collections import defaultdict

app = Celery('tasks')
app.config_from_object("celeryconfig", force=True)


@app.task
def splitAndCoundWord(doc):
    splitDoc = doc.replace("\n", "").split(" ")
    res = defaultdict(int)
    for word in splitDoc:
        res[word] += 1
    return res


@app.task
def combineResults(res):
    total = defaultdict(int)
    for r in res:
        for k in r:
            total[k] += r[k]
    return total
