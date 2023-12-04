#   -*- coding: utf-8 -*-
from faker import Faker
from progress1bar import ProgressBar

kwargs = {
    'total': 575,
    'clear_alias': True,
    'show_complete': False,
    'show_prefix': False,
    'show_duration': True,
    'show_bar': False
}
with ProgressBar(**kwargs) as pb:
    for _ in range(pb.total):
        pb.alias = Faker().sentence()
        # simulate work
        pb.count += 1
