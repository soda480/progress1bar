import unittest
from mock import patch
from mock import Mock
from progress1bar.prefixable import Prefixable


class TestPrefixable(unittest.TestCase):

    def test__prefix_Should_ReturnEmpty_When_NoShowPrefix(self, *patches):
        prefixable = Prefixable(show_prefix=False)
        self.assertEqual(prefixable.prefix, '')

    def test__prefix_Should_ReturnDefaultPrefix_When_ShowPrefix(self, *patches):
        prefixable = Prefixable()
        self.assertEqual(prefixable.prefix, 'Processing ')
