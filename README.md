# progress1bar #
[![build](https://github.com/soda480/progress1bar/actions/workflows/main.yml/badge.svg)](https://github.com/soda480/progress1bar/actions/workflows/main.yml)
[![codecov](https://codecov.io/gh/soda480/progress1bar/branch/main/graph/badge.svg?token=6zIZLnSJ0T)](https://codecov.io/gh/soda480/progress1bar)
[![Code Grade](https://api.codiga.io/project/25921/status/svg)](https://app.codiga.io/public/project/25921/progress1bar/dashboard)
[![complexity](https://img.shields.io/badge/complexity-Simple:%205-brightgreen)](https://radon.readthedocs.io/en/latest/api.html#module-radon.complexity)
[![vulnerabilities](https://img.shields.io/badge/vulnerabilities-None-brightgreen)](https://pypi.org/project/bandit/)
[![PyPI version](https://badge.fury.io/py/progress1bar.svg)](https://badge.fury.io/py/progress1bar)
[![python](https://img.shields.io/badge/python-3.9-teal)](https://www.python.org/downloads/)

A simple ANSI-based progress bar.

## Installation
```bash
pip install progress1bar
```

### `ProgressBar`

```
ProgressBar(total=None, fill=None, regex=None, completed_message=None, clear_alias=False)
```

<details><summary>Documentation</summary>

> `total` - An integer for the total number of items the progress bar will show that need to be completed.

> `fill` - A dictionary whose key values are integers that dictate the number of leading zeros the progress bar should add to the `total` and `completed` values; this is optional and should be used to format the progress bar appearance. The supported key values are `max_total` and `max_completed`.

> `regex` - A dictionary whose key values are regular expressions for `total`, `count` and `alias`. The regular expressions will be checked against the log messages intercepted from the executing function, if matched the value will be used to assign the attribute for the respective progress bar. The `total` and `count` key values are required, the `alias` key value is optional.

> `completed_message` - A string to designate the message the progress bar should display when complete. Default is 'Processing complete'

> `clear_alias` - A boolean to designate if the progress bar should clear the alias when complete.

**Attributes**

> `count` - An integer attribute to increment that designates the current count. When count reaches total the progress bar will show complete.

> `alias` - A string attribute to set the alias of the progress bar.

**Functions**

> **reset()**
>> Reset the progress bar so that it can be used again. It will maintain and show the number of times the progress bar has been used.

</details>


### Examples

Various [examples](https://github.com/soda480/progress1bar/tree/master/examples) are included to demonstrate the progress1bar package. To run the examples, build the Docker image and run the Docker container using the instructions described in the [Development](#development) section.

#### [example1](https://github.com/soda480/progress1bar/tree/master/examples/example1.py)

The `ProgressBar` class is used to display function execution as a progress bar. Use it as a context manager, and simply set the `.total` and `.count` attributes accordingly. Here is an example:

<details><summary>Code</summary>

```Python
import time
from progress1bar import ProgressBar

with ProgressBar(total=250) as pb:
    for _ in range(pb.total):
        pb.count += 1
        # simulate work
        time.sleep(.01)
```

</details>

![example](https://raw.githubusercontent.com/soda480/progress1bar/master/docs/images/example1.gif)

#### [example2](https://github.com/soda480/progress1bar/tree/master/examples/example2.py)

Configure `ProgressBar` to display the item that is currently being processd by setting the `alias` attribute, specify fill dictionary parameter to ensure the progress bar digits are displayed uniformly:

<details><summary>Code</summary>

```Python
import names
from progress1bar import ProgressBar

print('Processing names...')
completed_message = 'Done processing all names'
fill = {'max_total': 999}
with ProgressBar(total=500, completed_message=completed_message, fill=fill, clear_alias=True) as pb:
    for _ in range(pb.total):
        pb.alias = names.get_full_name()
        # simulate work
        pb.count += 1
```

</details>

![example](https://raw.githubusercontent.com/soda480/progress1bar/master/docs/images/example2.gif)

#### [example3](https://github.com/soda480/progress1bar/tree/master/examples/example3.py)

Configure `ProgressBar` to use regular expressions to determine the `total`, `count` and `alias` attributes:

<details><summary>Code</summary>

```Python
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
```

</details>

![example](https://raw.githubusercontent.com/soda480/progress1bar/master/docs/images/example3.gif)

#### [example4](https://github.com/soda480/progress1bar/tree/master/examples/example4.py)

Configure `ProgressBar` to show and reuse progress for several iterations:

<details><summary>Code</summary>

```Python
import time
import random
import names
from progress1bar import ProgressBar

TOTAL_ITEMS = 150
TOTAL_NAMES = 7

fill = {
    'max_total': TOTAL_ITEMS,
    'max_completed': TOTAL_NAMES
}
print(f'This progress bar will execute {TOTAL_NAMES} iterations of varying counts and keep track of how many have been completed ...')
with ProgressBar(fill=fill) as pb:
    total_names = 0
    while True:
        pb.alias = names.get_last_name()
        pb.total = random.randint(50, TOTAL_ITEMS)
        for _ in range(pb.total):
            names.get_full_name()
            pb.count += 1
            time.sleep(.01)
        total_names += 1  
        if total_names == TOTAL_NAMES:
            pb.alias = ''
            break
        pb.reset()
```

</details>

![example](https://raw.githubusercontent.com/soda480/progress1bar/master/docs/images/example4.gif)

## Development ##

Clone the repository and ensure the latest version of Docker is installed on your development server.

Build the Docker image:
```sh
docker image build \
-t \
progress1bar:latest .
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
pyb -X
```
