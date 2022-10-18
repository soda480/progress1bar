import unittest
from mock import patch
from mock import Mock
from progress1bar.aliasable import Aliasable


class TestAliasable(unittest.TestCase):

    def test__alias_Should_ReturnEmptyString_When_NoAlias(self, *patches):
        aliasable = Aliasable()
        self.assertEqual(aliasable.alias, '')

    def test__alias_Should_ReturnEmptyString_When_CompleteAndCLearAlias(self, *patches):
        aliasable = Aliasable(clear_alias=True)
        aliasable._complete = True
        aliasable.alias = '-alias-'
        self.assertEqual(aliasable.alias, '')

    def test__alias_Should_ReturnString_When_UseColor(self, *patches):
        aliasable = Aliasable(clear_alias=True)
        aliasable._complete = False
        aliasable._use_color = True
        aliasable.alias = '-alias-'
        self.assertTrue(aliasable.alias != '')

    def test__alias_Should_ReturnString_When_NoColor(self, *patches):
        aliasable = Aliasable(clear_alias=True)
        aliasable._complete = False
        aliasable._use_color = False
        aliasable.alias = '-alias-'
        self.assertEqual(aliasable.alias, ' -alias-')
