#   -*- coding: utf-8 -*-
import time
import random
import logging
import names
from progress1bar import ProgressBar

logger = logging.getLogger(__name__)

TOTAL_ITEMS = 325

def process_message(pb, message):
    pb.match(message)
    logger.debug(message)

regex = {
    'total': r'^processing total of (?P<value>\d+)$',
    'count': r'^processed .*$',
    'alias': r'^processor is (?P<value>.*)$'
}
fill = {
    'max_total': TOTAL_ITEMS
}
with ProgressBar(regex=regex, fill=fill) as pb:
    last_name = names.get_last_name()
    process_message(pb, f'processor is {last_name}')
    total = random.randint(50, TOTAL_ITEMS)
    process_message(pb, f'processing total of {total}')
    for _ in range(total):
        process_message(pb, f'processed {names.get_full_name()}')
        time.sleep(.01)
