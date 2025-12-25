import time
from faker import Faker
from colorama import Fore
from colorama import Style
from progress1bar import ProgressBar

kwargs = {
    'total': 75,
    'show_complete': False,
    'clear_alias': True,
    'show_duration': False,
    'ticker': Style.BRIGHT + Fore.RED + chr(9644) + Style.RESET_ALL,
}
with ProgressBar(**kwargs) as pb:
    for _ in range(pb.total):
        pb.alias = Faker().name()
        time.sleep(.08)  # simulate work
        pb.count += 1