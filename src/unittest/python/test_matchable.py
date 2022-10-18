import unittest
from mock import patch
from mock import Mock
from progress1bar.matchable import Matchable
from progress1bar.matchable import ALIAS_WIDTH


class TestMatchable(unittest.TestCase):

    @patch('progress1bar.matchable.Matchable._match_count', return_value=True)
    @patch('progress1bar.matchable.Matchable._match_alias', return_value=False)
    @patch('progress1bar.matchable.Matchable._match_total', return_value=False)
    def test__match_Should_CallMatchFunctions_When_Called(self, match_total_patch, match_alias_patch, match_count_patch, *patches):
        matchable = Matchable()
        text = '--some-text--'
        matchable.match(text)
        match_total_patch.assert_called_once_with(text)
        match_alias_patch.assert_called_once_with(text)
        match_count_patch.assert_called_once_with(text)

    def test__match_total_Should_ReturnMatchAndSetExpected_When_TotalIsNoneAndMatch(self, *patches):
        matchable = Matchable(regex={'total': r'^total is: (?P<value>\d+)$'})
        matchable._total = None
        text = 'total is: 100'
        result = matchable._match_total(text)
        self.assertEqual(matchable.total, 100)
        self.assertIsNotNone(result)

    def test__match_total_Should_ReturnNone_When_TotalIsSet(self, *patches):
        matchable = Matchable(regex={'total': r'^total is: (?P<value>\d+)$'})
        text = 'total is: 100'
        matchable._total = 50
        result = matchable._match_total(text)
        self.assertIsNone(result)

    def test__match_total_Should_ReturnNone_When_TotalIsNoneAndNoRegex(self, *patches):
        matchable = Matchable()
        matchable._total = None
        text = 'total is: 100'
        result = matchable._match_total(text)
        self.assertIsNone(result)

    def test__match_total_Should_ReturnNone_When_TotalIsNoneAndNoMatch(self, *patches):
        matchable = Matchable(regex={'total': r'^total is: (?P<value>\d+)$'})
        matchable._total = None
        text = 'count is: 100'
        result = matchable._match_total(text)
        self.assertIsNone(result)

    def test__match_alias_Should_ReturnMatchAndSetExpected_When_RegexMatchGreaterThanWidth(self, *patches):
        matchable = Matchable(regex={'alias': r'^id is: (?P<value>.*)$'})
        long_id = 'a' * (ALIAS_WIDTH + 10)
        text = f'id is: {long_id}'
        result = matchable._match_alias(text)
        self.assertEqual(matchable._alias, f'{long_id[0:ALIAS_WIDTH - 3]}...')
        self.assertIsNotNone(result)

    def test__match_alias_Should_ReturnMatchAndSetExpected_When_RegexMatch(self, *patches):
        matchable = Matchable(regex={'alias': r'^id is: (?P<value>.*)$'})
        text = 'id is: abc123'
        result = matchable._match_alias(text)
        self.assertEqual(matchable._alias, 'abc123')
        self.assertIsNotNone(result)

    def test__match_alias_Should_ReturnNone_When_NoRegex(self, *patches):
        matchable = Matchable()
        text = 'id is: abc'
        result = matchable._match_alias(text)
        self.assertIsNone(result)

    def test__match_alias_Should_ReturnNone_When_NoRegexMatch(self, *patches):
        matchable = Matchable(regex={'alias': r'^id is: (?P<value>.*)$'})
        text = 'total is: 100'
        result = matchable._match_alias(text)
        self.assertIsNone(result)

    def test__match_count_ShouldReturnMatchAndSetExpected_When_RegexMatch(self, *patches):
        matchable = Matchable(regex={'count': r'processed item'})
        matchable.count = 0
        matchable.total = 100
        text = 'processed item'
        result = matchable._match_count(text)
        self.assertEqual(matchable.count, 1)
        self.assertIsNotNone(result)

    def test__match_count_ShouldReturnNone_When_NoRegex(self, *patches):
        matchable = Matchable()
        matchable.count = 0
        matchable.total = 100
        text = 'processed item'
        result = matchable._match_count(text)
        self.assertEqual(matchable.count, 0)
        self.assertIsNone(result)

    def test__match_count_ShouldReturnNone_When_NoRegexMatch(self, *patches):
        matchable = Matchable(regex={'count': r'processed widget'})
        matchable.total = 100
        matchable.count = 10
        text = 'processed item'
        result = matchable._match_count(text)
        self.assertEqual(matchable.count, 10)
        self.assertIsNone(result)
