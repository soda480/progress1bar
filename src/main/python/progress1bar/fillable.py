import logging

logger = logging.getLogger(__name__)
FILL = 2


class Fillable:
    """ Add ability to fill the count and max values
        gets:
        sets:
    """
    def __init__(self, fill=None, **kwargs):
        logger.debug('executing constructor for Resettable')
        if not fill:
            fill = {}
        self._fill = self._get_fill(fill)
        super().__init__(**kwargs)

    def _get_fill(self, data):
        """ return fill dictionary derived from data values
        """
        fill = {
            'total': None,
            'completed': 2
        }
        if data:
            fill['completed'] = len(str(data.get('max_completed', FILL * '-')))
            fill['total'] = len(str(data.get('max_total', FILL * '-')))
        return fill

    def set_fill_total(self, value):
        self._fill['total'] = len(str(value))
