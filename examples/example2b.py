import time
from faker import Faker
from progress1bar import ProgressBar

kwargs = {
    'total': 575,
    'clear_alias': True,
    'show_prefix': False,
    'show_complete': False,
    'show_duration': True,
    'show_bar': False
}
with ProgressBar(**kwargs) as pb:
    for _ in range(pb.total):
        pb.alias = Faker().sentence()
        time.sleep(.008)  # simulate work
        pb.count += 1
