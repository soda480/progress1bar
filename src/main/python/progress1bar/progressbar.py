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

PROGRESS_WIDTH = 50
ALIAS_WIDTH = 100
FILL = 2
CLEAR_EOL = '\033[K'


class ProgressBar(object):
    """ Progress Bar implementation
    """

    def __init__(self, **kwargs):
        """ class constructor
        """
        logger.debug('executing ProgressBar constructor')
        colorama_init()
        defaults = {
            'regex': {},
            'completed_message': 'Processing complete',
            'clear_alias': False,
            'control': False,
            'show_prefix': True,
            'show_fraction': True,
            'show_percentage': True
        }
        for (attribute, default) in defaults.items():
            setattr(self, attribute, kwargs.get(attribute, default))
        ticker = kwargs.get('ticker', 9632)
        if not (32 < ticker < 65533):
            raise ValueError('ticker value not in supported range')
        self._ticker = chr(ticker)
        # self.complete boolean to track if progress bar has completed
        self.complete = False
        # self._completed int to track the number of progress bar completions
        # it's typically just 1 but can be multiple when using .reset()
        self._completed = 0
        # include support for durations
        self.duration = None
        self._modulus_count = 0
        # self._reset int keeps track of the number of times the progress bar has been reset
        self._reset = 0
        self.alias = ''
        # avoid __setattr__
        self.__dict__['count'] = 0
        total = kwargs.get('total')
        self.__dict__['total'] = total
        # execute after total is set
        self._fill = self._get_fill(kwargs.get('fill', {}))
        if total:
            # print progress bar if total specified in constructor
            self._print(False)

    def __str__(self):
        """ return string interpretation of class instance
        """
        bright_yellow = Style.BRIGHT + Fore.YELLOW + Back.BLACK

        # determine alias
        alias = f" {bright_yellow}{self.alias}{Style.RESET_ALL}"

        # determine progress
        progress = self._get_progress().strip()

        # determine completed
        completed = ''
        if self._completed and self._reset:
            completed_fill = self._fill['completed']
            completed = f' {bright_yellow}[{str(self._completed).zfill(completed_fill)}]'

        return f"{progress}{completed}{alias}"

    def __setattr__(self, name, value):
        """ set class instance attributes
        """
        if name == 'count' and self.total is None:
            return
        super(ProgressBar, self).__setattr__(name, value)
        if name in ['total', 'count']:
            if name == 'count':
                self._modulus_count = round(round(self.count / self.total, 2) * PROGRESS_WIDTH)
            else:
                if not self._fill['total']:
                    # only set fill for total if is is not set
                    self._fill['total'] = len(str(value))
            self._print(name == 'count')

    def __enter__(self):
        """ on entry - hide cursor if show and stderr is attached to tty
        """
        if not self.control and sys.stderr.isatty():
            cursor.hide()
        return self

    def __exit__(self, *args):
        """ on exit - show cursor if show and stderr is attached to tty and print progress bar
        """
        if self.clear_alias:
            self.alias = ''
        self._print(True)
        if not self.control and sys.stderr.isatty():
            cursor.show()

    def _print(self, clear):
        """ print progress bar on certain conditions
            sys.stderr is attached to a tty and if progress bar is not being controlled externally
            clear line prior to printing if clear is set or if progress bar has been reset
        """
        if self.control or not sys.stderr.isatty():
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
        self.complete = False
        self._modulus_count = 0
        # avoid __setattr__ for setting count value
        self.__dict__['count'] = 0
        self._reset += 1

    def match(self, text):
        """ call match functions and return on first success
        """
        functions = [self._match_total, self._match_alias, self._match_count]
        for function in functions:
            match = function(text)
            if match:
                return match

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

    def _get_percent_fraction(self):
        """ return tuple consisting of percentage and fraction for instance of non-completed progress bar
        """
        if self.total:
            total_fill = self._fill['total']
            percentage = str(round((self.count / self.total) * 100)).rjust(3)
            fraction = f'{str(self.count).zfill(total_fill)}/{str(self.total).zfill(total_fill)}'
            if self.count == self.total:
                self.complete = True
                self._completed += 1
        else:
            percentage = '0'.rjust(3)
            fraction = '#' * FILL + '/' + '#' * FILL
        return percentage, fraction

    def _get_progress(self):
        """ return progress text
        """
        if self.complete:
            progress = self._get_complete()
        else:
            _percentage, _fraction = self._get_percent_fraction()
            prefix = ''
            if self.show_prefix:
                prefix = 'Processing '
            fraction = ''
            if self.show_fraction:
                fraction = _fraction
            percentage = ''
            if self.show_percentage:
                percentage = f'{Style.BRIGHT}{_percentage}%{Style.RESET_ALL} '
            bar = self._ticker * self._modulus_count
            padding = ' ' * (PROGRESS_WIDTH - self._modulus_count)
            progress = f"{prefix}|{bar}{padding}|{percentage}{fraction}"
        return progress

    def _get_fill(self, data):
        """ return fill dictionary derived from data values
        """
        fill = {
            'total': None,
            'completed': None
        }
        if not data:
            fill['completed'] = FILL
        else:
            fill['completed'] = len(str(data.get('max_completed', FILL * '-')))
            fill['total'] = len(str(data.get('max_total', FILL * '-')))
        if self.total and not fill['total']:
            fill['total'] = len(str(self.total))
        return fill
