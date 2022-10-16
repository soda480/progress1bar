#   -*- coding: utf-8 -*-
import random
from faker import Faker
from progress1bar import ProgressBar

regex = {
    'total': r'^processing total of (?P<value>\d+)$',
    'count': r'^processed .*$',
    'alias': r'^processor is (?P<value>.*)$'
}
with ProgressBar(ticker=9733, regex=regex, use_color=False, show_duration=True) as pb:
    pb.match(f'processor is {Faker().name()}')
    total = random.randint(500, 750)
    pb.match(f'processing total of {total}')
    for _ in range(total):
        pb.match(f'processed {Faker().name()}')
