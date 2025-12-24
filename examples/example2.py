import time
from faker import Faker
from colorama import Fore
from colorama import Style
from progress1bar import ProgressBar

kwargs = {
    'total': 75,
    'completed_message': 'Processed names complete',
    'clear_alias': True,
    'show_fraction': False,
    'show_prefix': False,
    'show_duration': True,
    'use_color': True,
    'ticker': Style.BRIGHT + Fore.CYAN + chr(9644) + Style.RESET_ALL,
}
with ProgressBar(**kwargs) as pb:
    for _ in range(pb.total):
        pb.alias = Faker().name()
        # simulate work
        time.sleep(.08)
        pb.count += 1