#   -*- coding: utf-8 -*-
import random
import names
from progress1bar import ProgressBar

regex = {
    'total': r'^processing total of (?P<value>\d+)$',
    'count': r'^processed .*$',
    'alias': r'^processor is (?P<value>.*)$'
}
with ProgressBar(ticker=10148, regex=regex, use_color=False) as pb:
    pb.match(f'processor is {names.get_full_name()}')
    total = random.randint(500, 1000)
    pb.match(f'processing total of {total}')
    for _ in range(total):
        pb.match(f'processed {names.get_full_name()}')
