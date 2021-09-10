import re
import sys
import logging

import cursor
from colorama import Style
from colorama import Fore
from colorama import Back
from colorama import Cursor
from colorama import init as colorama_init

logger = logging.getLogger(__name__)

TICKER = chr(9632)  # ■
PROGRESS_WIDTH = 50
ALIAS_WIDTH = 100
FILL = 2
CLEAR_EOL = '\033[K'


class ProgressBar(object):
    """ Progress Bar implementation
    """

    def __init__(self, index=None, total=None, fill=None, regex=None, completed_message=None, aware=True, clear_alias=False):
        """ class constructor
        """
        logger.debug('executing ProgressBar constructor')
        colorama_init()

        self.aware = aware
        self.fill = ProgressBar._get_fill(fill)

        if not regex:
            regex = {}
        self.regex = regex

        self.completed_message = completed_message
        self._complete = False
        self._completed = 0
        self.show_completed = False
        self.duration = None

        self.index = index
        self._modulus_count = 0
        self._reset = 0
        self.clear_alias = clear_alias
        self.alias = ''
        # avoid __setattr__
        self.__dict__['count'] = 0
        self.__dict__['total'] = total
        if total:
            # print progress bar if total specified in constructor
            self._print(False)

    def __str__(self):
        """ return string interpretation of class instance
        """
        bright_yellow = Style.BRIGHT + Fore.YELLOW + Back.BLACK
        index = ''
        if self.index is not None:
            index_fill = self.fill['index']
            _index = f"{bright_yellow}{str(self.index).zfill(index_fill)}{Style.RESET_ALL}"
            index = f'{_index}: '
        alias = f"{bright_yellow}{self.alias}{Style.RESET_ALL}"
        progress = self._get_progress()
        completed = ''
        if self._completed and self.show_completed:
            completed_fill = self.fill['completed']
            completed = f'{bright_yellow}[{str(self._completed).zfill(completed_fill)}] '
        return f"{index}{progress} {completed}{alias}"

    def __setattr__(self, name, value):
        """ set class instance attributes
        """
        def _check(name, value):
            """ check function
            """
            if name in ['total', 'count']:
                if name == 'count':
                    self._modulus_count = round(round(self.count / self.total, 2) * PROGRESS_WIDTH)
                else:
                    if value == 0:
                        # if total is zero then set complete
                        self._complete = True
                self._print(name == 'count')

        if name == 'count' and self.total is None:
            return
        super(ProgressBar, self).__setattr__(name, value)
        _check(name, value)

    def __enter__(self):
        """ on entry - hide cursor if aware and stderr is attached to tty
        """
        if self.aware and sys.stderr.isatty():
            cursor.hide()
        return self

    def __exit__(self, *args):
        """ on exit - show cursor if aware and stderr is attached to tty and print progress bar
        """
        if self.clear_alias:
            self.alias = ''
        self._print(True)
        if self.aware and sys.stderr.isatty():
            cursor.show()

    def _print(self, clear):
        """ print progress bar on certain conditions
            sys.stderr is attached to a tty and if progress bar is aware
            clear line prior to printing if clear is set or if progress bar has been reset
        """
        if not self.aware or not sys.stderr.isatty():
            return
        if clear or self._reset:
            print(f'{Cursor.UP(1)}{CLEAR_EOL}', end='', file=sys.stderr)
        print(self, file=sys.stderr)
        sys.stderr.flush()

    def reset(self):
        """ reset progress bar
        """
        logger.debug('resetting progress bar')
        self.alias = ''
        self.__dict__['total'] = None
        self._complete = False
        self._modulus_count = 0
        # reset sets show_completed - typically only want to show completed when progress bars are reused and reset
        self.show_completed = True
        # avoid __setattr__ for setting count value
        self.__dict__['count'] = 0
        self._reset += 1

    def match(self, text):
        """ call match functions and return on first success
        """
        functions = [self._match_total, self._match_alias, self._match_count]
        for function in functions:
            if function(text):
                break

    def _match_total(self, text):
        """ set total if text matches total regex
        """
        match = None
        if self.total is None:
            regex = self.regex.get('total')
            if regex:
                match = re.match(regex, text)
                if match:
                    self.total = int(match.group('value'))
        return match

    def _match_alias(self, text):
        """ set alias if text matches alias regex
        """
        match = None
        regex = self.regex.get('alias')
        if regex:
            match = re.match(regex, text)
            if match:
                value = match.group('value')
                if len(value) > ALIAS_WIDTH:
                    value = f'{value[0:ALIAS_WIDTH - 3]}...'
                self.alias = value
        return match

    def _match_count(self, text):
        """ increment count if text matches count regex
        """
        match = None
        regex = self.regex.get('count')
        if regex:
            match = re.match(regex, text)
            if match:
                self.count += 1
        return match

    def _get_complete(self):
        """ return completed message
        """
        progress = 'Processing complete'
        if self.completed_message:
            progress = self.completed_message
        if self.duration:
            progress = f'{progress} - {self.duration}'
        return progress

    def _get_progress(self):
        """ return progress text
        """
        if self._complete:
            progress = self._get_complete()
        else:
            total_fill = self.fill['total']
            if self.total:
                _percentage = str(round((self.count / self.total) * 100))
                fraction = f'{str(self.count).zfill(total_fill)}/{str(self.total).zfill(total_fill)}'
                if self.count == self.total:
                    self._complete = True
                    self._completed += 1
            else:
                _percentage = '0'
                fraction = '#' * total_fill + '/' + '#' * total_fill

            bar = TICKER * self._modulus_count
            padding = ' ' * (PROGRESS_WIDTH - self._modulus_count)
            percentage = _percentage.rjust(3)
            progress = f"Processing |{bar}{padding}| {Style.BRIGHT}{percentage}%{Style.RESET_ALL} {fraction}"
        return progress

    @staticmethod
    def _get_fill(data):
        """ return fill dictionary derived from data values
        """
        fill = {}
        if not data:
            fill['total'] = FILL
            fill['index'] = FILL
            fill['completed'] = FILL
        else:
            fill['total'] = len(str(data.get('max_total', FILL * '-')))
            fill['index'] = len(str(data.get('max_index', FILL * '-')))
            fill['completed'] = len(str(data.get('max_completed', FILL * '-')))
        return fill
