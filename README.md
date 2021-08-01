# progress1bar #
[![complexity](https://img.shields.io/badge/complexity-Simple:%205-brightgreen)](https://radon.readthedocs.io/en/latest/api.html#module-radon.complexity)
[![vulnerabilities](https://img.shields.io/badge/vulnerabilities-None-brightgreen)](https://pypi.org/project/bandit/)
[![python](https://img.shields.io/badge/python-3.9-teal)](https://www.python.org/downloads/)

A simple ANSI-based progress bar.

## Installation ##
```bash
pip install progress1bar
```

### `ProgressBar`

Use the `ProgressBar` class to display your function's execution as a progress bar. Use it as a context manager, and simply set the `.total` and `.count` attributes accordingly. Here is an example:
```python
import random, time
from mp4ansi import ProgressBar

with ProgressBar() as pb:
    pb.alias = 'Super 80s'
    pb.total = random.randint(50, 100)
    for _ in range(pb.total):
        pb.count += 1
        # simulate work
        time.sleep(.09)
```
Executing the code above ([example1](https://github.com/soda480/progress1bar/tree/master/examples/example1.py)) results in the following:
![example](https://raw.githubusercontent.com/soda480/progress1bar/master/docs/images/example1.gif)

## Examples ##

Various [examples](https://github.com/soda480/progress1bar/tree/master/examples) are included to demonstrate the progress1bar package. To run the examples, build the Docker image and run the Docker container using the instructions described in the [Development](#development) section.

Configure `ProgressBar` to display the item that is currently being processd by setting `alias` attribute:
```python
import time, names
from progress1bar import ProgressBar

print('Processing names...')
completed_message = 'Done processing all names'
fill = {'max_index': 1, 'max_total': 9}
with ProgressBar(index=0, total=9, completed_message=completed_message, fill=fill, clear_alias=True) as pb:
    for _ in range(pb.total):
        pb.alias = names.get_full_name()
        pb.count += 1
        # simulate work
        time.sleep(.5)
```
Executing the code above ([example2](https://github.com/soda480/progress1bar/tree/master/examples/example2.py)) results in the following:
![example](https://raw.githubusercontent.com/soda480/progress1bar/master/docs/images/example2.gif)

Configure `ProgressBar` to use regular expressions to determine the total, cound and alias from logged messages:
```python
import names, random, logging
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
```
Executing the code above ([example3](https://github.com/soda480/progress1bar/tree/master/examples/example3.py)) results in the following:
![example](https://raw.githubusercontent.com/soda480/progress1bar/master/docs/images/example3.gif)

Configure `ProgressBar` to show progress for several iterations:
```python
import names, random
from progress1bar import ProgressBar

TOTAL_ITEMS = 325
TOTAL_NAMES = 5

fill = {
    'max_total': TOTAL_ITEMS,
    'max_completed': TOTAL_NAMES
}
with ProgressBar(fill=fill) as pb:
    total_names = 0
    while True:
        pb.alias = names.get_last_name()
        pb.total = random.randint(50, TOTAL_ITEMS)
        for _ in range(pb.total):
            names.get_full_name()
            pb.count += 1
        total_names += 1  
        if total_names == TOTAL_NAMES:
            pb.alias = ''
            break
        pb.reset()
```
Executing the code above ([example4](https://github.com/soda480/progress1bar/tree/master/examples/example4.py)) results in the following:
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
-v $PWD:/progress1bar \
progress1bar:latest \
/bin/sh
```

Execute the build:
```sh
pyb -X
```