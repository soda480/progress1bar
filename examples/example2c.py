#   -*- coding: utf-8 -*-
from faker import Faker
from progress1bar import ProgressBar
from unittest.mock import patch

kwargs = {
    'total': 575,
    'clear_alias': True,
    'show_complete': False,
    'show_prefix': False,
    'show_duration': True,
    'show_bar': False,
    'use_color': True
}
with patch('sys.stderr.isatty', return_value=False):
    with ProgressBar(**kwargs) as pb:
        for _ in range(pb.total):
            pb.alias = Faker().sentence()
            # simulate work
            pb.count += 1
