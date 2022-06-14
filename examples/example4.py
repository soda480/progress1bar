#   -*- coding: utf-8 -*-
import names, random
from time import sleep
from progress1bar import ProgressBar

TOTAL_ITEMS = 150
TOTAL_NAMES = 11

fill = {
    'max_total': TOTAL_ITEMS,
    'max_completed': TOTAL_NAMES,
    'max_index': 100
}
print(f'This progress bar will execute {TOTAL_NAMES} iterations of varying counts and keep track of how many have been completed ...')
with ProgressBar(index=23, fill=fill) as pb:
    total_names = 0
    while True:
        pb.alias = names.get_last_name()
        pb.total = random.randint(50, TOTAL_ITEMS)
        for _ in range(pb.total):
            names.get_full_name()
            pb.count += 1
            sleep(.01)
        total_names += 1  
        if total_names == TOTAL_NAMES:
            pb.alias = ''
            break
        pb.reset()
