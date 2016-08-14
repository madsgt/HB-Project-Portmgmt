import datetime
import sys

if sys.version_info < (2, 7):
    from unittest2 import main as test_main, SkipTest, TestCase
else:
    from unittest import main as test_main, SkipTest, TestCase

from yahoo_finance import Currency, Share, edt_to_utc, get_date_range


class TestShare(TestCase):

    def setUp(self):
        self.yahoo = Share('YHOO')

    def test_yhoo(self):
        # assert that these are float-like
        float(self.yahoo.get_open())
        float(self.yahoo.get_price())

    def test_get_info(self):
        info = self.yahoo.get_info()
        self.assertEqual(info['start'], '1996-04-12')
        self.assertEqual(info['symbol'], 'YHOO')

    def test_get_historical(self):
        history = self.yahoo.get_historical('2014-04-25', '2014-04-29')
        self.assertEqual(len(history), 3)
        expected = {
            'Adj_Close': '35.83',
            'Close': '35.83',
            'Date': '2014-04-29',
            'High': '35.89',
            'Low': '34.12',
            'Open': '34.37',
            'Symbol': 'YHOO',
            'Volume': '28736000'
        }
        self.assertDictEqual(history[0], expected)

    def test_get_historical_longer_than_1y(self):
        # issue #2
        history = self.yahoo.get_historical('2012-04-25', '2014-04-29')
        self.assertEqual(history[-1]['Date'], '2012-04-25')
        self.assertEqual(history[0]['Date'], '2014-04-29')
        self.assertEqual(len(history), 505)






if __name__ == "__main__":
    test_main()
