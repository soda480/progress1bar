#   -*- coding: utf-8 -*-
import time
from progress1bar import ProgressBar

with ProgressBar(total=250) as pb:
    for _ in range(pb.total):
        pb.count += 1
        # simulate work
        time.sleep(.01)
