import unittest
from mock import patch
from mock import Mock
from progress1bar.completable import Completable


class TestCompletable(unittest.TestCase):

    def test__complete_Should_ResetValues_When_FalseValue(self, *patches):
        completable = Completable()
        completable._duration = '-duration-',
        completable._total = 100
        completable._count = 100
        completable.complete = False
        self.assertIsNone(completable._duration)
        self.assertIsNone(completable._total)
        self.assertEqual(completable._count, 0)
        self.assertEqual(completable._modulus_count, 0)

    @patch('progress1bar.completable.datetime')
    def test__complete_Should_ResetValues_When_TrueValue(self, datetime_patch, *patches):
        completable = Completable()
        completable._start_time = Mock()
        completable.complete = True
        self.assertTrue(completable._duration is not None)
        self.assertTrue(completable.complete)

    def test__completed_Should_ReturnEmpty_When_NotCompleted(self, *patches):
        completable = Completable()
        completable._completed = False
        self.assertEqual(completable.completed, '')

    def test__completed_Should_ReturnEmpty_When_NoResetCount(self, *patches):
        completable = Completable()
        completable._completed = 1
        completable._reset_count = 0
        self.assertEqual(completable.completed, '')

    def test__completed_Should_ReturnStr_When_CompletedAndResetCountAndNotUseColor(self, *patches):
        completable = Completable()
        completable._use_color = False
        completable._fill = {
            'completed': 2
        }
        completable._completed = 1
        completable._reset_count = 1
        self.assertEqual(completable.completed, ' [01]')

    def test__completed_Should_ReturnStr_When_CompletedAndResetCountAndUseColor(self, *patches):
        completable = Completable()
        completable._use_color = True
        completable._fill = {
            'completed': 2
        }
        completable._completed = 1
        completable._reset_count = 1
        self.assertTrue(completable.completed is not None)

    def test__completed_message_Should_ReturnDefault_When_NoCompletedMessage(self, *patches):
        completable = Completable()
        self.assertEqual(completable.completed_message, 'Processing complete')

    def test__completed_message_Should_ReturnCompletedMessage_When_CompletedMessage(self, *patches):
        completable = Completable(completed_message='Done')
        self.assertEqual(completable.completed_message, 'Done')
