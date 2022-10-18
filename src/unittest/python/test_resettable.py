import unittest
from mock import patch
from mock import Mock
from progress1bar.resettable import Resettable


class TestResettable(unittest.TestCase):

    def test__reset_Should_SetAliasAndComplete_When_ClearAlias(self, *patches):
        resettable = Resettable()
        resettable._alias = '-alias-'
        resettable.reset()
        self.assertIsNone(resettable._alias)
        self.assertFalse(resettable.complete)

    def test__reset_Should_SetAliasAndCompleteIncrementResetCount_When_NoClearAlias(self, *patches):
        resettable = Resettable()
        resettable._reset_count = 2
        resettable._alias = '-alias-'
        resettable.reset(clear_alias=False)
        self.assertEqual(resettable._alias, '-alias-')
        self.assertFalse(resettable.complete)
        self.assertEqual(resettable._reset_count, 3)
