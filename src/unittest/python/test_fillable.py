import unittest
from mock import patch
from mock import Mock
from progress1bar.fillable import Fillable


class TestFillable(unittest.TestCase):

    def test__get_fill_Should_ReturnDefault_When_DataNoKey(self, *patches):
        fillable = Fillable()
        result = fillable._get_fill({'key': 'value'})
        expected_result = {
            'total': 2,
            'completed': 2
        }
        self.assertEqual(result, expected_result)

    def test__get_fill_Should_ReturnFill_When_DataKey(self, *patches):
        fillable = Fillable()
        result = fillable._get_fill({'max_completed': 100, 'max_total': 10000})
        expected_result = {
            'total': 5,
            'completed': 3
        }
        self.assertEqual(result, expected_result)

    def test__get_fill_Should_ReturnDefault_When_NoData(self, *patches):
        fillable = Fillable()
        result = fillable._get_fill(None)
        expected_result = {
            'total': None,
            'completed': 2
        }
        self.assertEqual(result, expected_result)

    def test__get_fill_total_Should_X_When_Y(self, *patches):
        fillable = Fillable()
        fillable._fill = {
            'total': None
        }
        fillable.set_fill_total('100')
        self.assertEqual(fillable._fill['total'], 3)
