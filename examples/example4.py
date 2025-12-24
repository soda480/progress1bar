#   -*- coding: utf-8 -*-
import random
import time
from faker import Faker
from progress1bar import ProgressBar

TOTAL_ITEMS = 300
ITERATIONS = 4
kwargs = {
    'show_prefix': False,
    'show_fraction': False,
    'show_duration': True
}
print(f'Execute {ITERATIONS} iterations of varying totals:')
with ProgressBar(**kwargs) as pb:
    iterations = 0
    while True:
        if iterations == ITERATIONS:
            pb.alias = ''
            pb.complete = True
            break
        pb.alias = Faker().name()
        pb.total = random.randint(100, TOTAL_ITEMS)
        for _ in range(pb.total):
            Faker().name()
            pb.count += 1
            time.sleep(.001)
        iterations += 1
        pb.reset()
        time.sleep(.8)
