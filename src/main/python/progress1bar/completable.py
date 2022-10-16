import datetime
import logging
from colorama import Fore
from colorama import Style

logger = logging.getLogger(__name__)
BRIGHT_YELLOW = Style.BRIGHT + Fore.YELLOW


class Completable:
    """ Add ability to set and configure values when progress bar completes
        gets:
            Durationable._start_time
            Durationable._stop_time
            Resettable._reset_count
            ProgressBar._use_color
            Fillable._fill
        sets:
            Durationable._stop_time
            Durationable._duration
            ProgressBar._total
            ProgressBar._count
            ProgressBar._modulus_count
    """
    def __init__(self, completed_message=None, show_complete=True, **kwargs):
        logger.debug('executing constructor for Completable')
        if completed_message is None:
            completed_message = 'Processing complete'
        self._completed_message = completed_message
        self._complete = False
        self._completed = 0
        self._show_complete = show_complete
        super().__init__(**kwargs)

    @property
    def complete(self):
        return self._complete

    @complete.setter
    def complete(self, value):
        self._complete = value
        if value:
            # if complete then stop and compute duration
            self._stop_time = datetime.datetime.now()
            start = self._start_time.time().strftime('%H:%M:%S')
            stop = self._stop_time.time().strftime('%H:%M:%S')
            self._duration = str(datetime.datetime.strptime(stop, '%H:%M:%S') - datetime.datetime.strptime(start, '%H:%M:%S'))
        else:
            self._duration = None
            self._total = None
            self._count = 0
            self._modulus_count = 0

    @property
    def completed(self):
        if not self._completed:
            return ''
        if not self._reset_count:
            # assures completed is displayed only if progress bar has been reset
            return ''
        fill = self._fill['completed']
        if self._use_color:
            return f' [{BRIGHT_YELLOW}{str(self._completed).zfill(fill)}{Style.RESET_ALL}]'
        return f' [{str(self._completed).zfill(fill)}]'

    @property
    def completed_message(self):
        return self._completed_message
