import logging

logger = logging.getLogger(__name__)


class Durationable:
    """ Add ability to compute and track execution duration
        gets:
        sets:
    """
    def __init__(self, show_duration=False, **kwargs):
        logger.debug('executing constructor for Durationable')
        self._show_duration = show_duration
        self._start_time = None
        self._stop_time = None
        self._duration = None
        super().__init__(**kwargs)

    @property
    def duration(self):
        if not self._show_duration:
            return ''
        if not self._duration:
            return ''
        return f' - {self._duration}'

    @duration.setter
    def duration(self, value):
        self._duration = value
