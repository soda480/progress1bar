#   -*- coding: utf-8 -*-
import names
from progress1bar import ProgressBar

print('Processing names...')
completed_message = 'Done processing all names'
fill = {'max_index': 9, 'max_total': 999}
with ProgressBar(index=1, total=500, completed_message=completed_message, fill=fill, clear_alias=True) as pb:
    for _ in range(pb.total):
        pb.alias = names.get_full_name()
        # simulate work
        pb.count += 1