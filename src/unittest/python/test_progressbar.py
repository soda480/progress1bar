
# Copyright (c) 2021 Intel Corporation

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#      http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import string
import unittest
from mock import patch
from mock import call
from mock import Mock
from mock import MagicMock

from progress1bar import ProgressBar
from progress1bar.progressbar import FILL
from progress1bar.progressbar import ALIAS_WIDTH

import sys
import logging
logger = logging.getLogger(__name__)


class TestProgressBar(unittest.TestCase):

    def remove_non_printable(self, item):
        """ remove non printable characters from item and return
        """
        return ''.join(char for char in item if char not in string.printable)

    def setUp(self):
        """
        """
        pass

    def tearDown(self):
        """
        """
        pass

    @patch('progress1bar.progressbar.colorama_init')
    @patch('progress1bar.progressbar.ProgressBar._get_fill')
    def test__init_Should_SetDefaults_When_Called(self, get_fill_patch, *patches):
        pbar = ProgressBar(aware=False, index=0)
        self.assertEqual(pbar.index, 0)
        self.assertEqual(pbar.regex, {})
        self.assertIsNone(pbar.completed_message)
        self.assertEqual(pbar._complete, False)
        self.assertEqual(pbar._completed, 0)
        self.assertEqual(pbar.show_completed, False)
        self.assertIsNone(pbar.duration)
        self.assertEqual(pbar.alias, '')
        self.assertIsNone(pbar.total)
        self.assertEqual(pbar._modulus_count, 0)
        self.assertEqual(pbar._reset, 0)
        self.assertEqual(pbar.fill, get_fill_patch.return_value)

    @patch('progress1bar.progressbar.colorama_init')
    @patch('progress1bar.progressbar.ProgressBar._get_fill')
    def test__init_Should_SetDefaults_When_AttributesPassed(self, get_fill_patch, *patches):
        pbar = ProgressBar(aware=False, index=0, total=100, regex={'key', 'value'})
        self.assertEqual(pbar.index, 0)
        self.assertEqual(pbar.regex, {'key', 'value'})
        self.assertIsNone(pbar.completed_message)
        self.assertEqual(pbar._complete, False)
        self.assertEqual(pbar._completed, 0)
        self.assertEqual(pbar.show_completed, False)
        self.assertIsNone(pbar.duration)
        self.assertEqual(pbar.alias, '')
        self.assertEqual(pbar.total, 100)
        self.assertEqual(pbar._modulus_count, 0)
        self.assertEqual(pbar._reset, 0)
        self.assertEqual(pbar.fill, get_fill_patch.return_value)

    @patch('progress1bar.progressbar.colorama_init')
    @patch('progress1bar.progressbar.ProgressBar._get_progress')
    def test__str_Should_ReturnExpected_When_Index(self, get_progress_patch, *patches):
        get_progress_patch.return_value = 'progress'
        pbar = ProgressBar(aware=False, index=0)
        result = str(pbar)
        self.assertEqual(result, '\x1b[1m\x1b[33m\x1b[40m00\x1b[0m: progress \x1b[1m\x1b[33m\x1b[40m\x1b[0m')

    @patch('progress1bar.progressbar.colorama_init')
    @patch('progress1bar.progressbar.ProgressBar._get_progress')
    def test__str_Should_ReturnExpected_When_NoIndex(self, get_progress_patch, *patches):
        get_progress_patch.return_value = 'progress'
        pbar = ProgressBar(aware=False, )
        result = str(pbar)
        self.assertEqual(result, 'progress \x1b[1m\x1b[33m\x1b[40m\x1b[0m')

    @patch('progress1bar.progressbar.colorama_init')
    @patch('progress1bar.progressbar.ProgressBar._get_progress')
    def test__str_Should_ReturnExpected_When_ShowCompleted(self, get_progress_patch, *patches):
        get_progress_patch.return_value = 'Processing complete'
        pbar = ProgressBar(aware=False, index=0)
        pbar._completed = 12
        pbar.show_completed = True
        str(pbar)
        # self.assertEqual(result, '\x1b[1m\x1b[33m\x1b[40m00\x1b[0m: Processing c[62 chars]b[0m')

    @patch('progress1bar.progressbar.colorama_init')
    def test__setattr_Should_SetExpected_When_CountAndTotal(self, *patches):
        pbar = ProgressBar(aware=False, index=0)
        pbar.total = 100
        pbar.count = 10
        self.assertEqual(pbar._modulus_count, 5)

    @patch('progress1bar.progressbar.colorama_init')
    def test__setattr_Should_SetExpected_When_TotalIsNone(self, *patches):
        pbar = ProgressBar(aware=False, index=0)
        pbar.count = 10
        self.assertEqual(pbar._modulus_count, 0)

    @patch('progress1bar.progressbar.colorama_init')
    @patch('progress1bar.progressbar.ProgressBar._match_count', return_value=True)
    @patch('progress1bar.progressbar.ProgressBar._match_alias', return_value=False)
    @patch('progress1bar.progressbar.ProgressBar._match_total', return_value=False)
    def test__match_Should_CallExpected_When_Called(self, match_total_patch, match_alias_patch, match_count_patch, *patches):
        pbar = ProgressBar(aware=False, index=0)
        text = '--some-text--'
        pbar.match(text)
        match_total_patch.assert_called_once_with(text)
        match_alias_patch.assert_called_once_with(text)
        match_count_patch.assert_called_once_with(text)

    @patch('progress1bar.progressbar.colorama_init')
    @patch('progress1bar.progressbar.ProgressBar._match_count', return_value=False)
    @patch('progress1bar.progressbar.ProgressBar._match_alias', return_value=False)
    @patch('progress1bar.progressbar.ProgressBar._match_total', return_value=False)
    def test__match_Should_CallExpected_When_CalledNoMatch(self, match_total_patch, match_alias_patch, match_count_patch, *patches):
        pbar = ProgressBar(aware=False, index=0)
        text = '--some-text--'
        pbar.match(text)
        match_total_patch.assert_called_once_with(text)
        match_alias_patch.assert_called_once_with(text)
        match_count_patch.assert_called_once_with(text)

    @patch('progress1bar.progressbar.colorama_init')
    def test__match_total_Should_ReturnMatchAndSetExpected_When_TotalIsNoneAndMatch(self, *patches):
        pbar = ProgressBar(aware=False, index=0, regex={'total': r'^total is: (?P<value>\d+)$'})
        text = 'total is: 100'
        result = pbar._match_total(text)
        self.assertEqual(pbar.total, 100)
        self.assertIsNotNone(result)

    @patch('progress1bar.progressbar.colorama_init')
    def test__match_total_Should_ReturnNone_When_TotalIsSet(self, *patches):
        pbar = ProgressBar(aware=False, index=0, regex={'total': r'^total is: (?P<value>\d+)$'})
        text = 'total is: 100'
        pbar.total = 50
        result = pbar._match_total(text)
        self.assertIsNone(result)

    @patch('progress1bar.progressbar.colorama_init')
    def test__match_total_Should_ReturnNone_When_TotalIsNoneAndNoRegex(self, *patches):
        pbar = ProgressBar(aware=False, index=0)
        text = 'total is: 100'
        result = pbar._match_total(text)
        self.assertIsNone(result)

    @patch('progress1bar.progressbar.colorama_init')
    def test__match_total_Should_ReturnNone_When_TotalIsNoneAndNoMatch(self, *patches):
        pbar = ProgressBar(aware=False, index=0, regex={'total': r'^total is: (?P<value>\d+)$'})
        text = 'count is: 100'
        result = pbar._match_total(text)
        self.assertIsNone(result)

    @patch('progress1bar.progressbar.colorama_init')
    def test__match_alias_Should_ReturnMatchAndSetExpected_When_RegexMatchGreaterThanWidth(self, *patches):
        pbar = ProgressBar(aware=False, index=0, regex={'alias': r'^id is: (?P<value>.*)$'})
        long_id = 'a' * (ALIAS_WIDTH + 10)
        text = f'id is: {long_id}'
        result = pbar._match_alias(text)
        self.assertEqual(pbar.alias, f'{long_id[0:ALIAS_WIDTH - 3]}...')
        self.assertIsNotNone(result)

    @patch('progress1bar.progressbar.colorama_init')
    def test__match_alias_Should_ReturnMatchAndSetExpected_When_RegexMatch(self, *patches):
        pbar = ProgressBar(aware=False, index=0, regex={'alias': r'^id is: (?P<value>.*)$'})
        text = 'id is: abc123'
        result = pbar._match_alias(text)
        self.assertEqual(pbar.alias, 'abc123')
        self.assertIsNotNone(result)

    @patch('progress1bar.progressbar.colorama_init')
    def test__match_alias_Should_ReturnNone_When_NoRegex(self, *patches):
        pbar = ProgressBar(aware=False, index=0)
        text = 'id is: abc'
        result = pbar._match_alias(text)
        self.assertIsNone(result)

    @patch('progress1bar.progressbar.colorama_init')
    def test__match_alias_Should_ReturnNone_When_NoRegexMatch(self, *patches):
        pbar = ProgressBar(aware=False, index=0, regex={'alias': r'^id is: (?P<value>.*)$'})
        text = 'total is: 100'
        result = pbar._match_alias(text)
        self.assertIsNone(result)

    @patch('progress1bar.progressbar.colorama_init')
    def test__match_count_ShouldReturnMatchAndSetExpected_When_RegexMatch(self, *patches):
        pbar = ProgressBar(aware=False, index=0, regex={'count': r'processed item'})
        pbar.total = 100
        text = 'processed item'
        result = pbar._match_count(text)
        self.assertEqual(pbar.count, 1)
        self.assertIsNotNone(result)

    @patch('progress1bar.progressbar.colorama_init')
    def test__match_count_ShouldReturnNone_When_NoRegex(self, *patches):
        pbar = ProgressBar(aware=False, index=0)
        pbar.total = 100
        text = 'processed item'
        result = pbar._match_count(text)
        self.assertEqual(pbar.count, 0)
        self.assertIsNone(result)

    @patch('progress1bar.progressbar.colorama_init')
    def test__match_count_ShouldReturnNone_When_NoRegexMatch(self, *patches):
        pbar = ProgressBar(aware=False, index=0, regex={'count': r'processed widget'})
        pbar.total = 100
        pbar.count = 10
        text = 'processed item'
        result = pbar._match_count(text)
        self.assertEqual(pbar.count, 10)
        self.assertIsNone(result)

    @patch('progress1bar.progressbar.colorama_init')
    def test__get_complete_Should_ReturnExpected_When_MessageAndDuration(self, *patches):
        pbar = ProgressBar(aware=False, index=0)
        pbar.completed_message = 'All done'
        pbar.duration = '01:23:45'
        result = pbar._get_complete()
        expected_result = 'All done - 01:23:45'
        self.assertEqual(result, expected_result)

    @patch('progress1bar.progressbar.colorama_init')
    def test__get_complete_Should_ReturnExpected_When_NoMessageAndDuration(self, *patches):
        pbar = ProgressBar(aware=False, index=0)
        pbar.duration = '01:23:45'
        result = pbar._get_complete()
        expected_result = 'Processing complete - 01:23:45'
        self.assertEqual(result, expected_result)

    @patch('progress1bar.progressbar.colorama_init')
    def test__get_complete_Should_ReturnExpected_When_NoMessageAndNoDuration(self, *patches):
        pbar = ProgressBar(aware=False, index=0)
        result = pbar._get_complete()
        expected_result = 'Processing complete'
        self.assertEqual(result, expected_result)

    @patch('progress1bar.progressbar.colorama_init')
    @patch('progress1bar.progressbar.ProgressBar._get_complete')
    def test__get_progress_Should_ReturnExpected_When_Complete(self, get_complete_patch, *patches):
        pbar = ProgressBar(aware=False, index=0)
        pbar._complete = True
        result = pbar._get_progress()
        self.assertEqual(result, get_complete_patch.return_value)

    @patch('progress1bar.progressbar.colorama_init')
    def test__get_progress_Should_ReturnExpected_When_NotCompleteNoTotal(self, *patches):
        pbar = ProgressBar(aware=False, index=0)
        result = pbar._get_progress()
        self.assertTrue('##/##' in result)

    @patch('progress1bar.progressbar.colorama_init')
    def test__get_progress_Should_ReturnExpected_When_NotCompleteAndTotal(self, *patches):
        pbar = ProgressBar(aware=False, index=0)
        pbar.total = 100
        pbar.count = 50
        result = pbar._get_progress()
        self.assertTrue('50%' in result)

    @patch('progress1bar.progressbar.colorama_init')
    def test__get_progress_Should_ReturnExpected_When_NotCompleteAndCountIsTotal(self, *patches):
        pbar = ProgressBar(aware=False, index=0)
        pbar.total = 100
        pbar.count = 100
        result = pbar._get_progress()
        self.assertTrue('100%' in result)

    @patch('progress1bar.progressbar.colorama_init')
    def test__reset_Should_SetExpected_When_Called(self, *patches):
        pbar = ProgressBar(aware=False, index=0)
        pbar.reset()
        pbar.reset()
        self.assertEqual(pbar._reset, 2)

    def test__get_fill_Should_ReturnExpected_When_NoData(self, *patches):
        result = ProgressBar._get_fill(None)
        expected_result = {'total': FILL, 'index': FILL, 'completed': FILL}
        self.assertEqual(result, expected_result)

    def test__get_fill_Should_ReturnExpected_When_Data(self, *patches):
        result = ProgressBar._get_fill({'max_index': 203, 'max_total': 10000, 'max_completed': 12})
        expected_result = {'total': 5, 'index': 3, 'completed': 2}
        self.assertEqual(result, expected_result)

    @patch('progress1bar.progressbar.cursor')
    @patch('progress1bar.progressbar.sys.stderr')
    def test__enter_exit_Should_HideAndShowCursor_When_AwareAndTty(self, stderr_patch, cursor_patch, *patches):
        stderr_patch.isatty.return_value = True
        with ProgressBar() as pb:
            cursor_patch.hide.assert_called_once_with()
            self.assertTrue(pb.aware)
        cursor_patch.show.assert_called_once_with()

    @patch('progress1bar.progressbar.cursor')
    @patch('progress1bar.progressbar.sys.stderr')
    def test__enter_exit_Should_NotHideOrShowCursor_When_NotTty(self, stderr_patch, cursor_patch, *patches):
        stderr_patch.isatty.return_value = False
        with ProgressBar() as pb:
            cursor_patch.hide.assert_not_called()
            self.assertTrue(pb.aware)
        cursor_patch.show.assert_not_called()

    @patch('progress1bar.progressbar.sys.stderr')
    def test__print_Should_Return_When_NoTty(self, stderr_patch, *patches):
        stderr_patch.isatty.return_value = False
        pb = ProgressBar(aware=False)
        pb._print('total')
        stderr_patch.flush.assert_not_called()

    @patch('builtins.print')
    @patch('progress1bar.progressbar.sys.stderr')
    def test__print_Should_CallExpected_When_TtyNoClear(self, stderr_patch, print_patch, *patches):
        stderr_patch.isatty.return_value = True
        pb = ProgressBar(aware=False)
        pb.aware = True
        pb.reset = 0
        pb._print(False)
        stderr_patch.flush.assert_called_once_with()
        self.assertEqual(len(print_patch.mock_calls), 1)

    @patch('builtins.print')
    @patch('progress1bar.progressbar.sys.stderr')
    def test__print_Should_CallExpected_When_TtyAndClear(self, stderr_patch, print_patch, *patches):
        stderr_patch.isatty.return_value = True
        pb = ProgressBar(aware=False)
        pb.aware = True
        pb._print(True)
        stderr_patch.flush.assert_called_once_with()
        self.assertEqual(len(print_patch.mock_calls), 2)
