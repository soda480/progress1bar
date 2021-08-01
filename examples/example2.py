#   -*- coding: utf-8 -*-
import time, names
from progress1bar import ProgressBar

print('Processing names...')
completed_message = 'Done processing all names'
fill = {'max_index': 1, 'max_total': 9}
with ProgressBar(index=0, total=9, completed_message=completed_message, fill=fill, clear_alias=True) as pb:
    for _ in range(pb.total):
        pb.alias = names.get_full_name()
        pb.count += 1
        # simulate work
        time.sleep(.5)
