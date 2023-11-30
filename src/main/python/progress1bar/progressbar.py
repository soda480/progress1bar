import sys
import logging
import datetime
import cursor
from colorama import Cursor
from colorama import init as colorama_init
from .prefixable import Prefixable
from .aliasable import Aliasable
from .durationable import Durationable
from .completable import Completable
from .resettable import Resettable
from .fillable import Fillable
from .matchable import Matchable

logger = logging.getLogger(__name__)
TICKER = 9632
PROGRESS_WIDTH = 50
CLEAR_EOL = '\033[K'


class ProgressBar(Prefixable, Aliasable, Durationable, Completable, Resettable, Fillable, Matchable):
    """ display progress bar
    """
    def __init__(self, total=None, show_percentage=True, show_fraction=True, use_color=True, control=False, ticker=None, show_bar=True, **kwargs):
        logger.debug('executing constructor for ProgressBar')
        self._previous = None
        super().__init__(**kwargs)
        colorama_init()
        self._show_bar = show_bar
        self._show_percentage = show_percentage
        self._show_fraction = show_fraction
        self._modulus_count = 0
        self._count = 0
        self._use_color = use_color
        self._control = control
        if not ticker:
            ticker = TICKER
        if not (32 < ticker < 65533):
            raise ValueError('ticker value not in supported range')
        self._ticker = chr(ticker)
        # execute total setter
        self.total = total

    def __enter__(self):
        if not self._control and sys.stderr.isatty():
            cursor.hide()
        return self

    def __exit__(self, *args):
        # force print on exit if not being controlled externally
        self._print(True, force=not self._control)
        if not self._control and sys.stderr.isatty():
            cursor.show()

    def __str__(self):
        if self._complete and self._show_complete:
            return f'{self.completed_message}{self.duration}{self.completed}{self.alias}'
        return f'{self.prefix}{self.bar}{self.percentage}{self.fraction}{self.completed}{self.alias}{self.duration}'

    @property
    def bar(self):
        if not self._show_bar:
            return ''
        tickers = self._ticker * self._modulus_count
        padding = ' ' * (PROGRESS_WIDTH - self._modulus_count)
        return f"|{tickers}{padding}|"

    @property
    def percentage(self):
        if not self._show_percentage:
            return ''
        if self._total:
            return f'{str(round((self._count / self._total) * 100)).rjust(3)}%'
        return '0'.rjust(3) + '%'

    @property
    def fraction(self):
        if not self._show_fraction:
            return ''
        if self._total:
            # Fillable._fill
            fill = self._fill['total']
            return f' {str(self._count).zfill(fill)}/{str(self._total).zfill(fill)}'
        return ' ##/##'

    @property
    def total(self):
        return self._total

    @total.setter
    def total(self, value):
        self._total = value
        if value:
            if not self._fill['total']:
                self.set_fill_total(value)
            # Resettable._reset_count
            if not self._reset_count:
                # ensures start_time is started once not after reset
                # access private attribute Durationable._start_time
                self._start_time = datetime.datetime.now()
            # print progress bar only if total was assigned an actual value
            self._print(False)

    @property
    def count(self):
        return self._count

    @count.setter
    def count(self, value):
        if not self._total:
            return
        self._count = value
        self._modulus_count = round(round(self._count / self._total, 2) * PROGRESS_WIDTH)
        if self._count == self._total:
            self.complete = True
            self._completed += 1
        self._print(True)

    def _print(self, clear, force=False):
        if not force:
            # not force printing
            if (self._control or not sys.stderr.isatty()):
                # printing of progress bar is controlled externally
                # is not attached to terminal
                return
            if (str(self) == self._previous):
                # logger.debug('not printing because current is same as previous')
                return

        if clear or self._reset_count:
            # line is explictly cleared
            # progress bar reset enabled - ensures next progress bar is printed
            # on same line as previous
            print(f'{Cursor.UP(1)}{CLEAR_EOL}', end='', file=sys.stderr)
        print(self, file=sys.stderr)
        sys.stderr.flush()
        self._previous = str(self)
