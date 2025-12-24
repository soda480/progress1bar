import logging

logger = logging.getLogger(__name__)


class Prefixable:
    """ Add ability to configure a prefix
        gets:
        sets:
    """
    def __init__(self, show_prefix=True, **kwargs):
        logger.debug('executing constructor for Prefixable')
        self._show_prefix = show_prefix
        self._prefix = 'Processing'
        super().__init__(**kwargs)

    @property
    def prefix(self):
        if not self._show_prefix:
            return ''
        return f'{self._prefix} '
