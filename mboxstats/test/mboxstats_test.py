import unittest
from mboxstats.mboxstats import MailboxStatistics
from collections import Counter


class MailboxStatisticsTest(unittest.TestCase):
    def setUp(self):
        self.mailbox = MailboxStatistics("/media/sf_datasets/mails/received-2014.txt")

    def test_get_from_values(self):
        from_values = self.mailbox.get_from_values()
        self.assertTrue(isinstance(from_values, list))

    def test_get_from_value_counts(self):
        from_value_counts = self.mailbox.get_from_value_counts()
        self.assertTrue(isinstance(from_value_counts, Counter))

    def test_get_n_most_frequent_from_values(self):
        n_most_frequent_from_values = self.mailbox.get_n_most_frequent_from_values()
        self.assertEqual(len(n_most_frequent_from_values), 1)
