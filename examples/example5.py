#   -*- coding: utf-8 -*-
import time
import random
import names
from progress1bar import ProgressBar

with ProgressBar(use_color=False) as pb:
    pb.alias = names.get_full_name()
    pb.total = random.randint(50, 100)
    for _ in range(pb.total):
        pb.count += 1
        # simulate work
        time.sleep(random.choice([.03, .06, .09]))