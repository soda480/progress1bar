import logging
from colorama import Fore
from colorama import Style

logger = logging.getLogger(__name__)
BRIGHT_YELLOW = Style.BRIGHT + Fore.YELLOW


class Aliasable:
    """ Add ability to set and display an alias
        gets:
            Completable._complete
            ProgressBar._use_color
    """
    def __init__(self, clear_alias=False, **kwargs):
        logger.debug('executing constructor for Aliasable')
        self._clear_alias = clear_alias
        self._alias = None
        super().__init__(**kwargs)

    @property
    def alias(self):
        if not self._alias:
            return ''
        if self._complete and self._clear_alias:
            return ''
        if self._use_color:
            return f' {BRIGHT_YELLOW}{self._alias}{Style.RESET_ALL}'
        return f' {self._alias}'

    @alias.setter
    def alias(self, value):
        self._alias = value
