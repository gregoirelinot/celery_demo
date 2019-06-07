from tasks import *

from celery import *

print(add.delay(1, 1).get())
