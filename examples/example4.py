#   -*- coding: utf-8 -*-
import time
import random
import names
from progress1bar import ProgressBar

TOTAL_ITEMS = 150
TOTAL_NAMES = 7

fill = {
    'max_total': TOTAL_ITEMS,
    'max_completed': TOTAL_NAMES
}
print(f'This progress bar will execute {TOTAL_NAMES} iterations of varying counts and keep track of how many have been completed ...')
with ProgressBar(fill=fill) as pb:
    total_names = 0
    while True:
        pb.alias = names.get_last_name()
        pb.total = random.randint(50, TOTAL_ITEMS)
        for _ in range(pb.total):
            names.get_full_name()
            pb.count += 1
            time.sleep(.01)
        total_names += 1  
        if total_names == TOTAL_NAMES:
            pb.alias = ''
            break
        pb.reset()
