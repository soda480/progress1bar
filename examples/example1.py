#   -*- coding: utf-8 -*-
import time
from progress1bar import ProgressBar

with ProgressBar(total=250, show_prefix=False, show_fraction=True) as pb:
    for _ in range(pb.total):
        pb.count += 1
        # simulate work
        time.sleep(.01)
