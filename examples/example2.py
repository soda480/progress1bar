#   -*- coding: utf-8 -*-
import time
import names
from progress1bar import ProgressBar

print('Processing names...')
completed_message = 'Processed names'
with ProgressBar(total=75, completed_message=completed_message, clear_alias=True, show_fraction=False, show_prefix=False) as pb:
    for _ in range(pb.total):
        pb.alias = names.get_full_name()
        # simulate work
        time.sleep(.08)
        pb.count += 1