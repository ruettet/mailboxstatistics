import unittest
from mboxstats.mboxstats import OutlookMailboxStatistics
from collections import Counter


class OutlookMailboxStatisticsTest(unittest.TestCase):
    def setUp(self):
        self.mailbox = OutlookMailboxStatistics('/media/sf_datasets/mails/received-2014.txt', 'latin1', 'nl_BE',
                                                '%A %d %B %Y %H:%M')

    def test_get_number_of_mails(self):
        mail_count = self.mailbox.get_number_of_mails()
        self.assertTrue(isinstance(mail_count, int))

    def test_get_from_value_counts(self):
        from_value_counts = self.mailbox.get_from_value_counts()
        self.assertTrue(isinstance(from_value_counts, Counter))

    def test_get_number_of_mails_per_hour(self):
        mails_per_hour = self.mailbox.get_number_of_mails_per_hour()
        self.assertTrue(isinstance(mails_per_hour, Counter))

    def test_get_number_of_mails_per_hour_of_day(self):
        mails_per_hour_of_day = self.mailbox.get_number_of_mails_per_hour_of_day()
        self.assertTrue(isinstance(mails_per_hour_of_day, Counter))

    def test_get_number_of_mails_per_day(self):
        mails_per_day = self.mailbox.get_number_of_mails_per_day()
        self.assertTrue(isinstance(mails_per_day, Counter))

    def test_get_subject_token_frequencies(self):
        subject_token_frequencies = self.mailbox.get_subject_token_frequencies()
        self.assertTrue(isinstance(subject_token_frequencies, Counter))