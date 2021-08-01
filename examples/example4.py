#   -*- coding: utf-8 -*-
import names, random
from progress1bar import ProgressBar

TOTAL_ITEMS = 325
TOTAL_NAMES = 5

fill = {
    'max_total': TOTAL_ITEMS,
    'max_completed': TOTAL_NAMES
}
with ProgressBar(fill=fill) as pb:
    total_names = 0
    while True:
        pb.alias = names.get_last_name()
        pb.total = random.randint(50, TOTAL_ITEMS)
        for _ in range(pb.total):
            names.get_full_name()
            pb.count += 1
        total_names += 1  
        if total_names == TOTAL_NAMES:
            pb.alias = ''
            break
        pb.reset()
