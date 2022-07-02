# progress1bar #
[![build](https://github.com/soda480/progress1bar/actions/workflows/main.yml/badge.svg)](https://github.com/soda480/progress1bar/actions/workflows/main.yml)
[![codecov](https://codecov.io/gh/soda480/progress1bar/branch/main/graph/badge.svg?token=6zIZLnSJ0T)](https://codecov.io/gh/soda480/progress1bar)
[![Code Grade](https://api.codiga.io/project/25921/status/svg)](https://app.codiga.io/public/project/25921/progress1bar/dashboard)
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
ProgressBar(total=None, fill=None, regex=None, completed_message=None, clear_alias=False, show_prefix=True, show_fraction=True, show_percentage=True)
```

<details><summary>Documentation</summary>

> `total` - An integer for the total number of items the progress bar will show that need to be completed.

> `fill` - A dictionary whose key values are integers that dictate the number of leading zeros the progress bar should add to the `total` and `completed` values; this is optional and should be used to format the progress bar appearance. The supported key values are `max_total` and `max_completed`.

> `regex` - A dictionary whose key values are regular expressions for `total`, `count` and `alias`. The regular expressions will be checked against the log messages intercepted from the executing function, if matched the value will be used to assign the attribute for the respective progress bar. The `total` and `count` key values are required, the `alias` key value is optional.

> `completed_message` - A string to designate the message the progress bar should display when complete. Default is 'Processing complete'

> `clear_alias` - A boolean to designate if the progress bar should clear the alias when complete.

> `show_prefix` - A boolean to designate if the prefix of `Processing ` should be printed prefixing the progress bar.

> `show_fraction` - A boolean to designate if the fraction should be printed with the progress bar.

> `show_percentage` - A boolean to designate if the percentage should be printed with the progress bar.

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

with ProgressBar(total=250, show_prefix=False, show_fraction=True) as pb:
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
import time
import names
from progress1bar import ProgressBar

print('Processing names...')
completed_message = 'Processed names'
with ProgressBar(total=75, completed_message=completed_message, clear_alias=True, show_fraction=False, show_prefix=False) as pb:
    for _ in range(pb.total):
        pb.alias = names.get_full_name()
        # simulate work
        time.sleep(.08)
        pb.count += 1
```

</details>

![example](https://raw.githubusercontent.com/soda480/progress1bar/master/docs/images/example2.gif)

#### [example3](https://github.com/soda480/progress1bar/tree/master/examples/example3.py)

Configure `ProgressBar` to use regular expressions to determine the `total`, `count` and `alias` attributes:

<details><summary>Code</summary>

```Python
import random
import names
from progress1bar import ProgressBar

regex = {
    'total': r'^processing total of (?P<value>\d+)$',
    'count': r'^processed .*$',
    'alias': r'^processor is (?P<value>.*)$'
}
with ProgressBar(regex=regex) as pb:
    pb.match(f'processor is {names.get_full_name()}')
    total = random.randint(500, 1000)
    pb.match(f'processing total of {total}')
    for _ in range(total):
        pb.match(f'processed {names.get_full_name()}')
```

</details>

![example](https://raw.githubusercontent.com/soda480/progress1bar/master/docs/images/example3.gif)

#### [example4](https://github.com/soda480/progress1bar/tree/master/examples/example4.py)

Configure `ProgressBar` to show and reuse progress for several iterations:

<details><summary>Code</summary>

```Python
import random
import time
import names
from progress1bar import ProgressBar

TOTAL_ITEMS = 800
ITERATIONS = 4

print(f'Execute {ITERATIONS} iterations of varying totals:')
with ProgressBar(show_prefix=False, show_fraction=False) as pb:
    iterations = 0
    while True:
        if iterations == ITERATIONS:
            pb.alias = ''
            pb.complete = True
            break
        pb.alias = names.get_full_name()
        pb.total = random.randint(500, TOTAL_ITEMS)
        for _ in range(pb.total):
            names.get_full_name()
            pb.count += 1
        iterations += 1
        pb.reset()
        time.sleep(.4)
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
