# progress1bar
[![build](https://github.com/soda480/progress1bar/actions/workflows/main.yml/badge.svg)](https://github.com/soda480/progress1bar/actions/workflows/main.yml)
[![coverage](https://img.shields.io/badge/coverage-100%25-brightgreen)](https://pybuilder.io/)
[![vulnerabilities](https://img.shields.io/badge/vulnerabilities-None-brightgreen)](https://pypi.org/project/bandit/)
[![PyPI version](https://badge.fury.io/py/progress1bar.svg)](https://badge.fury.io/py/progress1bar)
[![python](https://img.shields.io/badge/python-3.7%20%7C%203.8%20%7C%203.9%20%7C%203.10-teal)](https://www.python.org/downloads/)

A customizable ANSI-based progress bar.

## Installation
```bash
pip install progress1bar
```

### `ProgressBar`

```
ProgressBar(
    total=None,
    fill=None,
    regex=None,
    completed_message=None,
    clear_alias=False,
    show_prefix=True,
    show_fraction=True,
    show_percentage=True,
    show_duration=False,
    show_complete=True,
    ticker=None,
    use_color=True,
    show_bar=True)
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

> `show_duration` - A boolean to designate if the duration should be printed after progress bar execution.

> `show_complete` - A boolean to designate if the completed message is to be displayed upon progress bar completion.

> `ticker` - A integer representing unicode character to print as the progress bar ticker. Refer to [unicode chart](https://www.ssec.wisc.edu/~tomw/java/unicode.html) for values. Default is 9632 (black square ■).

> `use_color` - A boolean to designate if the progress bar should be displayed with color. Default is `True`.

**Attributes**

> `count` - An integer attribute to increment that designates the current count. When count reaches total the progress bar will show complete.

> `alias` - A string attribute to set the alias of the progress bar.

> `show_bar` - A boolean to designate if the progress bar tickers should be printed.

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

Configure `ProgressBar` to display an alias for the item that is currently being processd by setting the `alias` parameter, specify fill dictionary parameter to ensure the progress bar digits are displayed uniformly:

<details><summary>Code</summary>

```Python
import time
from faker import Faker
from progress1bar import ProgressBar

completed_message = 'Processed names complete'
with ProgressBar(total=75, completed_message=completed_message, clear_alias=True, show_fraction=False, show_prefix=False, show_duration=True) as pb:
    for _ in range(pb.total):
        pb.alias = Faker().name()
        # simulate work
        time.sleep(.08)
        pb.count += 1
```

</details>

![example](https://raw.githubusercontent.com/soda480/progress1bar/master/docs/images/example2.gif)

#### [example3](https://github.com/soda480/progress1bar/tree/master/examples/example3.py)

Configure `ProgressBar` with a custom ticker, show duration, do not use color, and use regular expressions to determine the `total`, `count` and `alias` attributes:

<details><summary>Code</summary>

```Python
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
```

</details>

![example](https://raw.githubusercontent.com/soda480/progress1bar/master/docs/images/example3.gif)

#### [example4](https://github.com/soda480/progress1bar/tree/master/examples/example4.py)

Configure `ProgressBar` to show and reuse progress for several iterations:

<details><summary>Code</summary>

```Python
import random
import time
from faker import Faker
from progress1bar import ProgressBar

TOTAL_ITEMS = 300
ITERATIONS = 4

print(f'Execute {ITERATIONS} iterations of varying totals:')
with ProgressBar(show_prefix=False, show_fraction=False, show_duration=True) as pb:
    iterations = 0
    while True:
        if iterations == ITERATIONS:
            pb.alias = ''
            pb.complete = True
            break
        pb.alias = Faker().name()
        pb.total = random.randint(100, TOTAL_ITEMS)
        for _ in range(pb.total):
            Faker().name()
            pb.count += 1
        iterations += 1
        pb.reset()
        time.sleep(.4)
```

</details>

![example](https://raw.githubusercontent.com/soda480/progress1bar/master/docs/images/example4.gif)

### Programs using `progress1bar`

* [pypbars](https://pypi.org/project/pypbars/)
* [mppbar](https://pypi.org/project/mppbar/)

## Development ##

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
pyb -X
```
