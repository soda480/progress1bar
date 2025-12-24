import re
import logging

logger = logging.getLogger(__name__)
ALIAS_WIDTH = 100


class Matchable:
    """ Add ability to match count values using regular expressions
        gets:
        sets:
            ProgressBar.total
            ProgressBar.count
            Aliasable._alias
    """
    def __init__(self, regex=None, **kwargs):
        logger.debug('executing constructor for Resettable')
        if not regex:
            regex = {}
        self._regex = regex
        super().__init__(**kwargs)

    def match(self, text):
        """ call match functions and return on first success
        """
        functions = [self._match_total, self._match_alias, self._match_count]
        for function in functions:
            function(text)

    def _match_total(self, text):
        """ set total if text matches total regex
        """
        match = None
        if self._total is None:
            regex = self._regex.get('total')
            if regex:
                match = re.match(regex, text)
                if match:
                    self.total = int(match.group('value'))
        return match

    def _match_alias(self, text):
        """ set alias if text matches alias regex
        """
        match = None
        regex = self._regex.get('alias')
        if regex:
            match = re.match(regex, text)
            if match:
                value = match.group('value')
                if len(value) > ALIAS_WIDTH:
                    value = f'{value[0:ALIAS_WIDTH - 3]}...'
                self._alias = value
        return match

    def _match_count(self, text):
        """ increment count if text matches count regex
        """
        match = None
        regex = self._regex.get('count')
        if regex:
            match = re.match(regex, text)
            if match:
                self.count += 1
        return match
