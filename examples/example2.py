#   -*- coding: utf-8 -*-
import time
from faker import Faker
from progress1bar import ProgressBar

completed_message = 'Processed names complete'
with ProgressBar(total=75, completed_message=completed_message, clear_alias=True, show_fraction=False, show_prefix=False, show_duration=True) as pb:
    for _ in range(pb.total):
        pb.alias = Faker().name()
        # simulate work
        time.sleep(.08)
        pb.count += 1