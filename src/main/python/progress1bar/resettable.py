import logging

logger = logging.getLogger(__name__)


class Resettable:
    """ Add ability to reset progress bar
        gets:
        sets:
            Aliasable._alias
            Completable.complete
    """
    def __init__(self, **kwargs):
        logger.debug('executing constructor for Resettable')
        self._reset_count = 0
        super().__init__(**kwargs)

    def reset(self, clear_alias=True):
        self._reset_count += 1
        if clear_alias:
            self._alias = None
        self.complete = False
