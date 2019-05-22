from tasks import *

from celery import *


def gen():
    return " ".join(str(i) for i in range(10))

print(chord([splitAndCoundWord.s(gen()) for c in range(10)])(combineResults.s()).get())
