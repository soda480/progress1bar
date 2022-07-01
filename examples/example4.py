#   -*- coding: utf-8 -*-
import random
import time
import names
from progress1bar import ProgressBar

TOTAL_ITEMS = 800
ITERATIONS = 4

fill = {
    'max_total': TOTAL_ITEMS,
    'max_completed': ITERATIONS
}
print(f'This progress bar will execute {ITERATIONS} iterations of varying totals:')
with ProgressBar(fill=fill) as pb:
    iterations = 0
    while True:
        if iterations == ITERATIONS:
            pb.alias = ''
            pb.complete = True
            break
        pb.alias = names.get_full_name()
        pb.total = random.randint(500, TOTAL_ITEMS)
        for _ in range(pb.total):
            names.get_full_name()
            pb.count += 1
        iterations += 1
        pb.reset()
        time.sleep(.4)
