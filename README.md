[![ci](https://github.com/soda480/progress1bar/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/soda480/progress1bar/actions/workflows/ci.yml)
![Coverage](https://raw.githubusercontent.com/soda480/threaded-order/main/badges/coverage.svg)
[![PyPI version](https://badge.fury.io/py/progress1bar.svg)](https://badge.fury.io/py/progress1bar)

# progress1bar

A lightweight, ANSI-based progress bar for terminal output — configurable, readable, and easy to drop into loops or long-running jobs.

## Installation
```bash
pip install progress1bar
```

## Quick start

Use ProgressBar as a context manager. Set `total`, then increment `count`.

```Python
import time
from progress1bar import ProgressBar

with ProgressBar(total=250) as pb:
    for _ in range(pb.total):
        pb.count += 1
        time.sleep(0.01)  # simulate work
```

![example](https://raw.githubusercontent.com/soda480/progress1bar/main/docs/images/example1.gif)

## Showing what’s being processed (`alias`)

If you want the bar to show the “current item”, set `alias` as you go.  You can also set a custom ticker.

```Python
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
```

![example](https://raw.githubusercontent.com/soda480/progress1bar/main/docs/images/example2.gif)

## Configuration

```Python
ProgressBar(
    total=None,
    fill=None,
    regex=None,
    completed_message=None,
    clear_alias=False,
    show_fraction=True,
    show_percentage=True,
    show_duration=False,
    show_complete=True,
    ticker=None,
    use_color=True,
    show_bar=True)
```

| Option              | Type   | What it does                                      | Default                 |
| ------------------- | ------ | ------------------------------------------------- | ----------------------- |
| `total`             | `int`  | Total units of work to complete                   | `None`                  |
| `completed_message` | `str`  | Message shown when complete                       | `"Processing complete"` |
| `show_fraction`     | `bool` | Show `count/total`                                | `True`                  |
| `show_percentage`   | `bool` | Show percent complete                             | `True`                  |
| `show_duration`     | `bool` | Print elapsed time after completion               | `False`                 |
| `show_complete`     | `bool` | Show completion message                           | `True`                  |
| `use_color`         | `bool` | ANSI color output                                 | `True`                  |
| `show_bar`          | `bool` | Render ticker characters (the “bar” itself)       | `True`                  |
| `ticker`            | `int`  | Unicode code point to use as the ticker character | `9632` (`■`)            |

### Number formatting (`fill`)

`fill` lets you pad the displayed total / count with leading zeros for a consistent look.

```Python
fill = {"max_total": 4, "max_completed": 4}
```

### Regex-driven updates (`regex`)

If you’d rather drive the progress bar by feeding it messages (instead of setting attributes directly), you can supply regex patterns for total, count, and optionally alias. When a message matches, the captured value is applied.

```Python
import random
from faker import Faker
from progress1bar import ProgressBar

kwargs = {
    "ticker": 9733,  # ★
    "regex": {
        "total": r"^processing total of (?P<value>\d+)$",
        "count": r"^processed .*$",
        "alias": r"^processor is (?P<value>.*)$",
    },
    "use_color": False,
}

with ProgressBar(**kwargs) as pb:
    pb.match(f"processor is {Faker().name()}")
    total = random.randint(500, 750)
    pb.match(f"processing total of {total}")
    for _ in range(total):
        pb.match(f"processed {Faker().name()}")
```

### Reuse the same progress bar (`reset()`)

If you want to reuse one ProgressBar instance across multiple runs (and keep track of repeated usage), call:

```Python
pb.reset()
```

![example](https://raw.githubusercontent.com/soda480/progress1bar/main/docs/images/example4.gif)

### More Examples

The repo includes multiple runnable examples (including variations like “no bar, just percentage/fraction”, custom tickers, regex matching, and multiple iterations with resets).

## Development

Clone the repository and ensure the latest version of Docker is installed on your development server.

Build the Docker image:
```sh
docker image build \
-t progress1bar:latest .
```

Run the Docker container:
```sh
docker container run \
--rm \
-it \
-v $PWD:/code \
progress1bar:latest \
bash
```

Execute the build:
```sh
make dev
```
