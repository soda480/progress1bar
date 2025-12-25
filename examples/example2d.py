#   -*- coding: utf-8 -*-
import random
from faker import Faker
from progress1bar import ProgressBar

kwargs = {
    'clear_alias': True,
    'show_complete': False,
    'show_duration': True,
    'show_bar': False,
    'regex': {
        'total': r'^processing total of (?P<value>\d+) items$',
        'count': r'^processed .*$',
        'alias': r'^processed (?P<value>.*)$'
    }
}
with ProgressBar(**kwargs) as pb:
    total = random.randint(500, 750)
    pb.match(f'processing total of {total} items')
    for _ in range(total):
        # simulate work
        pb.match(f'processed {Faker().sentence()}')
