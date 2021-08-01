#   -*- coding: utf-8 -*-
import names, random, time
from progress1bar import ProgressBar

with ProgressBar() as pb:
    pb.alias = names.get_full_name()
    pb.total = random.randint(50, 100)
    for _ in range(pb.total):
        pb.count += 1
        # simulate work
        time.sleep(.09)