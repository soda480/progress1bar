#   -*- coding: utf-8 -*-
import time
import random
from faker import Faker
from progress1bar import ProgressBar
from mock import patch

with patch('sys.stderr.isatty', return_value=False):
    with ProgressBar(use_color=True, show_duration=True, control=False, show_complete=False) as pb:
        pb.alias = Faker().name()
        pb.total = random.randint(50, 100)
        for _ in range(pb.total):
            pb.count += 1
            # simulate work
            time.sleep(random.choice([.03, .06, .09]))