import string
import unittest
from mock import patch
from mock import Mock
from progress1bar import ProgressBar
from progress1bar.progressbar import FILL
from progress1bar.progressbar import ALIAS_WIDTH


class TestProgressBar(unittest.TestCase):

    def remove_non_printable(self, item):
        """ remove non printable characters from item and return
        """
        return ''.join(char for char in item if char not in string.printable)

    def test__init_Should_RaiseValueError_When_TickerNotInRange(self, *patches):
        with self.assertRaises(ValueError):
            ProgressBar(ticker=32)
        with self.assertRaises(ValueError):
            ProgressBar(ticker=65534)

    @patch('progress1bar.progressbar.sys.stderr.isatty', return_value=False)
    @patch('progress1bar.progressbar.colorama_init')
    @patch('progress1bar.progressbar.ProgressBar._get_fill')
    def test__init_Should_SetDefaults_When_Called(self, get_fill_patch, *patches):
        pbar = ProgressBar()
        self.assertEqual(pbar.regex, {})
        self.assertEqual(pbar.completed_message, 'Processing complete')
        self.assertEqual(pbar.complete, False)
        self.assertEqual(pbar._completed, 0)
        self.assertIsNone(pbar.duration)
        self.assertEqual(pbar.alias, '')
        self.assertIsNone(pbar.total)
        self.assertEqual(pbar._modulus_count, 0)
        self.assertEqual(pbar._reset, 0)
        self.assertEqual(pbar._fill, get_fill_patch.return_value)

    @patch('progress1bar.progressbar.sys.stderr.isatty', return_value=False)
    @patch('progress1bar.progressbar.colorama_init')
    def test__init_Should_SetDefaults_When_AttributesPassed(self, *patches):
        pbar = ProgressBar(total=100, regex={'key', 'value'}, completed_message='--completed-message--')
        self.assertEqual(pbar.regex, {'key', 'value'})
        self.assertEqual(pbar.completed_message, '--completed-message--')
        self.assertEqual(pbar.complete, False)
        self.assertEqual(pbar._completed, 0)
        self.assertIsNone(pbar.duration)
        self.assertEqual(pbar.alias, '')
        self.assertEqual(pbar.total, 100)
        self.assertEqual(pbar._modulus_count, 0)
        self.assertEqual(pbar._reset, 0)

    @patch('progress1bar.progressbar.sys.stderr.isatty', return_value=False)
    @patch('progress1bar.progressbar.colorama_init')
    @patch('progress1bar.progressbar.ProgressBar._get_progress')
    def test__str_Should_ReturnExpected_When_Index(self, get_progress_patch, *patches):
        get_progress_patch.return_value = 'progress'
        pbar = ProgressBar()
        result = str(pbar)
        self.assertEqual(result, 'progress \x1b[1m\x1b[33m\x1b[0m')

    @patch('progress1bar.progressbar.sys.stderr.isatty', return_value=False)
    @patch('progress1bar.progressbar.colorama_init')
    @patch('progress1bar.progressbar.ProgressBar._get_progress')
    def test__str_Should_ReturnExpected_When_NoIndex(self, get_progress_patch, *patches):
        get_progress_patch.return_value = 'progress'
        pbar = ProgressBar()
        result = str(pbar)
        self.assertEqual(result, 'progress \x1b[1m\x1b[33m\x1b[0m')

    @patch('progress1bar.progressbar.sys.stderr.isatty', return_value=False)
    @patch('progress1bar.progressbar.colorama_init')
    @patch('progress1bar.progressbar.ProgressBar._get_progress')
    def test__str_Should_ReturnExpected_When_ShowCompleted(self, get_progress_patch, *patches):
        get_progress_patch.return_value = 'Processing complete'
        pbar = ProgressBar()
        pbar._completed = 12
        pbar._reset = 2
        str(pbar)
        # self.assertEqual(result, '\x1b[1m\x1b[33m\x1b[40m00\x1b[0m: Processing c[62 chars]b[0m')

    @patch('progress1bar.progressbar.sys.stderr.isatty', return_value=False)
    @patch('progress1bar.progressbar.colorama_init')
    def test__setattr_Should_SetExpected_When_CountAndTotal(self, *patches):
        pbar = ProgressBar()
        pbar.total = 100
        pbar.count = 10
        self.assertEqual(pbar._modulus_count, 5)

    @patch('progress1bar.progressbar.sys.stderr.isatty', return_value=False)
    @patch('progress1bar.progressbar.colorama_init')
    def test__setattr_Should_SetExpected_When_TotalIsNone(self, *patches):
        pbar = ProgressBar()
        pbar.count = 10
        self.assertEqual(pbar._modulus_count, 0)

    @unittest.skip('i dont think this is needed')
    @patch('progress1bar.progressbar.sys.stderr.isatty', return_value=False)
    @patch('progress1bar.progressbar.colorama_init')
    def test__setattr_Should_SetExpected_When_TotalIsZero(self, *patches):
        pbar = ProgressBar()
        pbar.total = 0
        self.assertEqual(pbar.complete, True)

    @patch('progress1bar.progressbar.sys.stderr.isatty', return_value=False)
    @patch('progress1bar.progressbar.colorama_init')
    @patch('progress1bar.progressbar.ProgressBar._match_count', return_value=True)
    @patch('progress1bar.progressbar.ProgressBar._match_alias', return_value=False)
    @patch('progress1bar.progressbar.ProgressBar._match_total', return_value=False)
    def test__match_Should_CallExpected_When_Called(self, match_total_patch, match_alias_patch, match_count_patch, *patches):
        pbar = ProgressBar()
        text = '--some-text--'
        pbar.match(text)
        match_total_patch.assert_called_once_with(text)
        match_alias_patch.assert_called_once_with(text)
        match_count_patch.assert_called_once_with(text)

    @patch('progress1bar.progressbar.sys.stderr.isatty', return_value=False)
    @patch('progress1bar.progressbar.colorama_init')
    @patch('progress1bar.progressbar.ProgressBar._match_count', return_value=False)
    @patch('progress1bar.progressbar.ProgressBar._match_alias', return_value=False)
    @patch('progress1bar.progressbar.ProgressBar._match_total', return_value=False)
    def test__match_Should_CallExpected_When_CalledNoMatch(self, match_total_patch, match_alias_patch, match_count_patch, *patches):
        pbar = ProgressBar()
        text = '--some-text--'
        pbar.match(text)
        match_total_patch.assert_called_once_with(text)
        match_alias_patch.assert_called_once_with(text)
        match_count_patch.assert_called_once_with(text)

    @patch('progress1bar.progressbar.sys.stderr.isatty', return_value=False)
    @patch('progress1bar.progressbar.colorama_init')
    def test__match_total_Should_ReturnMatchAndSetExpected_When_TotalIsNoneAndMatch(self, *patches):
        pbar = ProgressBar(regex={'total': r'^total is: (?P<value>\d+)$'})
        text = 'total is: 100'
        result = pbar._match_total(text)
        self.assertEqual(pbar.total, 100)
        self.assertIsNotNone(result)

    @patch('progress1bar.progressbar.sys.stderr.isatty', return_value=False)
    @patch('progress1bar.progressbar.colorama_init')
    def test__match_total_Should_ReturnNone_When_TotalIsSet(self, *patches):
        pbar = ProgressBar(regex={'total': r'^total is: (?P<value>\d+)$'})
        text = 'total is: 100'
        pbar.total = 50
        result = pbar._match_total(text)
        self.assertIsNone(result)

    @patch('progress1bar.progressbar.sys.stderr.isatty', return_value=False)
    @patch('progress1bar.progressbar.colorama_init')
    def test__match_total_Should_ReturnNone_When_TotalIsNoneAndNoRegex(self, *patches):
        pbar = ProgressBar()
        text = 'total is: 100'
        result = pbar._match_total(text)
        self.assertIsNone(result)

    @patch('progress1bar.progressbar.sys.stderr.isatty', return_value=False)
    @patch('progress1bar.progressbar.colorama_init')
    def test__match_total_Should_ReturnNone_When_TotalIsNoneAndNoMatch(self, *patches):
        pbar = ProgressBar(regex={'total': r'^total is: (?P<value>\d+)$'})
        text = 'count is: 100'
        result = pbar._match_total(text)
        self.assertIsNone(result)

    @patch('progress1bar.progressbar.sys.stderr.isatty', return_value=False)
    @patch('progress1bar.progressbar.colorama_init')
    def test__match_alias_Should_ReturnMatchAndSetExpected_When_RegexMatchGreaterThanWidth(self, *patches):
        pbar = ProgressBar(regex={'alias': r'^id is: (?P<value>.*)$'})
        long_id = 'a' * (ALIAS_WIDTH + 10)
        text = f'id is: {long_id}'
        result = pbar._match_alias(text)
        self.assertEqual(pbar.alias, f'{long_id[0:ALIAS_WIDTH - 3]}...')
        self.assertIsNotNone(result)

    @patch('progress1bar.progressbar.sys.stderr.isatty', return_value=False)
    @patch('progress1bar.progressbar.colorama_init')
    def test__match_alias_Should_ReturnMatchAndSetExpected_When_RegexMatch(self, *patches):
        pbar = ProgressBar(regex={'alias': r'^id is: (?P<value>.*)$'})
        text = 'id is: abc123'
        result = pbar._match_alias(text)
        self.assertEqual(pbar.alias, 'abc123')
        self.assertIsNotNone(result)

    @patch('progress1bar.progressbar.sys.stderr.isatty', return_value=False)
    @patch('progress1bar.progressbar.colorama_init')
    def test__match_alias_Should_ReturnNone_When_NoRegex(self, *patches):
        pbar = ProgressBar()
        text = 'id is: abc'
        result = pbar._match_alias(text)
        self.assertIsNone(result)

    @patch('progress1bar.progressbar.sys.stderr.isatty', return_value=False)
    @patch('progress1bar.progressbar.colorama_init')
    def test__match_alias_Should_ReturnNone_When_NoRegexMatch(self, *patches):
        pbar = ProgressBar(regex={'alias': r'^id is: (?P<value>.*)$'})
        text = 'total is: 100'
        result = pbar._match_alias(text)
        self.assertIsNone(result)

    @patch('progress1bar.progressbar.sys.stderr.isatty', return_value=False)
    @patch('progress1bar.progressbar.colorama_init')
    def test__match_count_ShouldReturnMatchAndSetExpected_When_RegexMatch(self, *patches):
        pbar = ProgressBar(regex={'count': r'processed item'})
        pbar.total = 100
        text = 'processed item'
        result = pbar._match_count(text)
        self.assertEqual(pbar.count, 1)
        self.assertIsNotNone(result)

    @patch('progress1bar.progressbar.sys.stderr.isatty', return_value=False)
    @patch('progress1bar.progressbar.colorama_init')
    def test__match_count_ShouldReturnNone_When_NoRegex(self, *patches):
        pbar = ProgressBar()
        pbar.total = 100
        text = 'processed item'
        result = pbar._match_count(text)
        self.assertEqual(pbar.count, 0)
        self.assertIsNone(result)

    @patch('progress1bar.progressbar.sys.stderr.isatty', return_value=False)
    @patch('progress1bar.progressbar.colorama_init')
    def test__match_count_ShouldReturnNone_When_NoRegexMatch(self, *patches):
        pbar = ProgressBar(regex={'count': r'processed widget'})
        pbar.total = 100
        pbar.count = 10
        text = 'processed item'
        result = pbar._match_count(text)
        self.assertEqual(pbar.count, 10)
        self.assertIsNone(result)

    @patch('progress1bar.progressbar.sys.stderr.isatty', return_value=False)
    @patch('progress1bar.progressbar.colorama_init')
    def test__get_complete_Should_ReturnExpected_When_MessageAndDuration(self, *patches):
        pbar = ProgressBar(show_duration=True)
        pbar.completed_message = 'All done'
        pbar.duration = '01:23:45'
        result = pbar._get_complete()
        expected_result = 'All done - 01:23:45'
        self.assertEqual(result, expected_result)

    @patch('progress1bar.progressbar.sys.stderr.isatty', return_value=False)
    @patch('progress1bar.progressbar.colorama_init')
    def test__get_complete_Should_ReturnExpected_When_NoMessageAndDuration(self, *patches):
        pbar = ProgressBar(show_duration=True)
        pbar.duration = '01:23:45'
        result = pbar._get_complete()
        expected_result = 'Processing complete - 01:23:45'
        self.assertEqual(result, expected_result)

    @patch('progress1bar.progressbar.sys.stderr.isatty', return_value=False)
    @patch('progress1bar.progressbar.colorama_init')
    def test__get_complete_Should_ReturnExpected_When_NoMessageAndNoDuration(self, *patches):
        pbar = ProgressBar()
        result = pbar._get_complete()
        expected_result = 'Processing complete'
        self.assertEqual(result, expected_result)

    @patch('progress1bar.progressbar.sys.stderr.isatty', return_value=False)
    @patch('progress1bar.progressbar.colorama_init')
    @patch('progress1bar.progressbar.ProgressBar._get_complete')
    def test__get_progress_Should_ReturnExpected_When_Complete(self, get_complete_patch, *patches):
        pbar = ProgressBar(total=10)
        pbar.complete = True
        result = pbar._get_progress()
        self.assertEqual(result, get_complete_patch.return_value)

    @patch('progress1bar.progressbar.sys.stderr.isatty', return_value=False)
    @patch('progress1bar.progressbar.colorama_init')
    def test__get_progress_Should_ReturnExpected_When_NotCompleteNoTotal(self, *patches):
        pbar = ProgressBar()
        result = pbar._get_progress()
        self.assertTrue('##/##' in result)

    @patch('progress1bar.progressbar.sys.stderr.isatty', return_value=False)
    @patch('progress1bar.progressbar.colorama_init')
    def test__get_progress_Should_ReturnExpected_When_NotCompleteAndTotal(self, *patches):
        pbar = ProgressBar()
        pbar.total = 100
        pbar.count = 50
        result = pbar._get_progress()
        self.assertTrue('50%' in result)

    @patch('progress1bar.progressbar.sys.stderr.isatty', return_value=False)
    @patch('progress1bar.progressbar.colorama_init')
    def test__get_progress_Should_ReturnExpected_When_NotCompleteAndCountIsTotal(self, *patches):
        pbar = ProgressBar()
        pbar.total = 100
        pbar.count = 100
        result = pbar._get_progress()
        self.assertTrue('100%' in result)

    @patch('progress1bar.progressbar.sys.stderr.isatty', return_value=False)
    @patch('progress1bar.progressbar.colorama_init')
    def test__reset_Should_SetExpected_When_Called(self, *patches):
        pbar = ProgressBar()
        pbar.reset()
        pbar.reset()
        self.assertEqual(pbar._reset, 2)

    def test__set_fill_Should_ReturnExpected_When_NoData(self, *patches):
        pbar = ProgressBar()
        expected_result = {'total': None, 'completed': FILL}
        self.assertEqual(pbar._fill, expected_result)

    def test__set_fill_Should_ReturnExpected_When_Data(self, *patches):
        pbar = ProgressBar(fill={'max_total': 10000, 'max_completed': 12})
        expected_result = {'total': 5, 'completed': 2}
        self.assertEqual(pbar._fill, expected_result)

    @patch('progress1bar.progressbar.cursor')
    @patch('progress1bar.progressbar.sys.stderr')
    def test__enter_exit_Should_HideAndShowCursor_When_Tty(self, stderr_patch, cursor_patch, *patches):
        stderr_patch.isatty.return_value = True
        with ProgressBar(total=10):
            cursor_patch.hide.assert_called_once_with()
        cursor_patch.show.assert_called_once_with()

    @patch('progress1bar.progressbar.cursor')
    @patch('progress1bar.progressbar.sys.stderr')
    def test__enter_exit_Should_NotHideOrShowCursor_When_NotTty(self, stderr_patch, cursor_patch, *patches):
        stderr_patch.isatty.return_value = False
        with ProgressBar():
            cursor_patch.hide.assert_not_called()
        cursor_patch.show.assert_not_called()

    @patch('progress1bar.ProgressBar._print')
    @patch('progress1bar.progressbar.cursor')
    @patch('progress1bar.progressbar.sys.stderr')
    def test__enter_exit_Should_ClearAlias_When_ClearAlias(self, stderr_patch, cursor_patch, *patches):
        stderr_patch.isatty.return_value = True
        with ProgressBar(clear_alias=True) as pb:
            pb.alias = 'something'
        self.assertEqual(pb.alias, '')

    @patch('progress1bar.progressbar.sys.stderr')
    def test__print_Should_Return_When_NoTty(self, stderr_patch, *patches):
        stderr_patch.isatty.return_value = False
        pb = ProgressBar()
        pb._print('total')
        stderr_patch.flush.assert_not_called()

    @patch('builtins.print')
    @patch('progress1bar.progressbar.sys.stderr')
    def test__print_Should_CallExpected_When_TtyNoClear(self, stderr_patch, print_patch, *patches):
        stderr_patch.isatty.return_value = True
        pb = ProgressBar()
        pb.show = True
        pb.reset = 0
        pb._print(False)
        stderr_patch.flush.assert_called_once_with()
        self.assertEqual(len(print_patch.mock_calls), 1)

    @patch('builtins.print')
    @patch('progress1bar.progressbar.sys.stderr')
    def test__print_Should_CallExpected_When_TtyAndClear(self, stderr_patch, print_patch, *patches):
        stderr_patch.isatty.return_value = True
        pb = ProgressBar()
        pb.show = True
        pb._print(True)
        stderr_patch.flush.assert_called_once_with()
        self.assertEqual(len(print_patch.mock_calls), 2)
