import unittest
from mock import patch
from mock import Mock
from progress1bar.durationable import Durationable


class TestDurationable(unittest.TestCase):

    def test__duration_Should_ReturnEmpty_When_NoShowDuration(self, *patches):
        durationable = Durationable()
        durationable.duration = '-duration-'
        self.assertEqual(durationable.duration, '')

    def test__duration_Should_ReturnEmpty_When_ShowDurationAndNoDuration(self, *patches):
        durationable = Durationable(show_duration=True)
        durationable.duration = None
        self.assertEqual(durationable.duration, '')

    def test__duration_Should_ReturnDuration_When_ShowDuration(self, *patches):
        durationable = Durationable(show_duration=True)
        durationable.duration = '-duration-'
        self.assertEqual(durationable.duration, ' - -duration-')
