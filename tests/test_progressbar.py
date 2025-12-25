import string
import unittest
from mock import patch
from mock import Mock
from mock import call
from progress1bar import ProgressBar
from progress1bar.progressbar import TICKER


class TestProgressBar(unittest.TestCase):

    def remove_non_printable(self, item):
        """ remove non printable characters from item and return
        """
        return ''.join(char for char in item if char not in string.printable)

    def test__init_Should_RaiseValueError_When_TickerNotInRange(self, *patches):
        with self.assertRaises(ValueError):
            ProgressBar(ticker=32, use_color=False)
        with self.assertRaises(ValueError):
            ProgressBar(ticker=65534, use_color=False)

    @patch('progress1bar.progressbar.sys.stderr.isatty', return_value=False)
    @patch('progress1bar.progressbar.colorama_init')
    def test__init_Should_SetDefaults_When_Called(self, get_fill_patch, *patches):
        pbar = ProgressBar()
        self.assertEqual(pbar._modulus_count, 0)
        self.assertEqual(pbar._count, 0)

    @patch('progress1bar.progressbar.sys.stderr.isatty', return_value=False)
    @patch('progress1bar.progressbar.colorama_init')
    def test__str_Should_ReturnExpected_When_Complete(self, *patches):
        pbar = ProgressBar(total=10, show_complete=True)
        pbar.complete = True
        result = str(pbar)
        self.assertEqual(result, 'Processing complete')

    @patch('progress1bar.progressbar.sys.stderr.isatty', return_value=False)
    @patch('progress1bar.progressbar.colorama_init')
    def test__str_Should_ReturnExpected_When_NotComplete(self, *patches):
        pbar = ProgressBar(total=10, show_complete=True, use_color=False)
        pbar.count = 1
        self.assertEqual(pbar.count, 1)
        self.assertEqual(pbar.total, 10)
        result = str(pbar)
        self.assertTrue(result.startswith(' 10% 01/10'))

    @patch('progress1bar.progressbar.sys.stderr.isatty', return_value=True)
    @patch('progress1bar.ProgressBar.print')
    @patch('progress1bar.progressbar.cursor')
    def test__enter_exit_Should_HideAndShowCursor_When_Tty(self, cursor_patch, print_patch, *patches):
        with ProgressBar(total=10):
            cursor_patch.hide.assert_called_once_with()
        cursor_patch.show.assert_called_once_with()
        self.assertTrue(call(True, force=True) in print_patch.mock_calls)

    @patch('progress1bar.progressbar.sys.stderr.isatty', return_value=False)
    @patch('progress1bar.ProgressBar.print')
    @patch('progress1bar.progressbar.cursor')
    def test__enter_exit_Should_NotHideOrShowCursor_When_NotTty(self, cursor_patch, print_patch, *patches):
        with ProgressBar():
            cursor_patch.hide.assert_not_called()
        cursor_patch.show.assert_not_called()
        print_patch.assert_called_once_with(True, force=True)

    @patch('progress1bar.progressbar.sys.stderr')
    def test__print_Should_NotPrint_When_NoTtyAndNotForced(self, stderr_patch, *patches):
        stderr_patch.isatty.return_value = False
        pb = ProgressBar()
        pb.print(True)
        stderr_patch.flush.assert_not_called()

    @patch('progress1bar.progressbar.sys.stderr')
    def test__print_Should_NotPrint_When_TtyAndControlledNotForced(self, stderr_patch, *patches):
        stderr_patch.isatty.return_value = True
        pb = ProgressBar(control=True)
        pb.print(True)
        stderr_patch.flush.assert_not_called()

    @patch('progress1bar.progressbar.sys.stderr')
    def test__print_Should_NotPrint_When_PreviousSameAsCurrent(self, stderr_patch, *patches):
        stderr_patch.isatty.return_value = True
        pb = ProgressBar()
        pb._previous = '  0% ##/##                                                   '
        pb.print(False)
        stderr_patch.flush.assert_not_called()

    @patch('builtins.print')
    @patch('progress1bar.progressbar.sys.stderr')
    def test__print_Should_Print_When_TtyAndNoClear(self, stderr_patch, print_patch, *patches):
        stderr_patch.isatty.return_value = True
        pb = ProgressBar()
        pb.print(False)
        stderr_patch.flush.assert_called_once_with()
        self.assertEqual(len(print_patch.mock_calls), 1)

    @patch('builtins.print')
    @patch('progress1bar.progressbar.sys.stderr')
    def test__print_Should_ClearAndPrint_When_TtyAndNoClearAndResetCount(self, stderr_patch, print_patch, *patches):
        stderr_patch.isatty.return_value = True
        pb = ProgressBar()
        pb._reset_count = 1
        pb.print(False)
        stderr_patch.flush.assert_called_once_with()
        self.assertEqual(len(print_patch.mock_calls), 2)

    @patch('builtins.print')
    @patch('progress1bar.progressbar.sys.stderr')
    def test__print_Should_ClearAndPrint_When_TtyAndClear(self, stderr_patch, print_patch, *patches):
        stderr_patch.isatty.return_value = True
        pb = ProgressBar()
        pb.print(True)
        stderr_patch.flush.assert_called_once_with()
        self.assertEqual(len(print_patch.mock_calls), 2)

    @patch('progress1bar.progressbar.colorama_init')
    def test__percentage_Should_ReturnEmpty_When_NoShowPercentage(self, *patches):
        pb = ProgressBar(show_percentage=False)
        self.assertEqual(pb.percentage, '')

    @patch('progress1bar.progressbar.colorama_init')
    def test__fraction_Should_ReturnEmpty_When_NoShowFraction(self, *patches):
        pb = ProgressBar(show_fraction=False)
        self.assertEqual(pb.fraction, '')

    @patch('progress1bar.ProgressBar.print')
    def test__count_Should_NotSetCount_When_NoTotal(self, *patches):
        pb = ProgressBar()
        pb.count = 1
        self.assertIsNone(pb.total)

    @patch('progress1bar.ProgressBar.print')
    def test__count_Should_UpdateCompletedAttributes_When_CountEqualTotal(self, *patches):
        pb = ProgressBar(total=1)
        pb.count = 1
        self.assertTrue(pb.complete)
        self.assertEqual(pb._completed, 1)
