import unittest
from mboxstats.mboxstats import MailboxStatistics
from collections import Counter

class MailboxStatisticsTest(unittest.TestCase):
    def setUp(self):
        self.mailbox = MailboxStatistics("/media/sf_datasets/mails/received-2014.txt")

    def test_show_mailbox_from_values(self):
        from_values = self.mailbox.get_mailbox_from_values()
        self.assertTrue(isinstance(from_values, list))

    def test_show_mailbox_from_value_counts(self):
        from_value_counts = self.mailbox.get_mailbox_from_value_counts()
        self.assertTrue(isinstance(from_value_counts, Counter))
