import codecs
import locale
from re import sub
from re import compile
from datetime import datetime
from collections import Counter


class MailboxStatistics(object):
    def __init__(self):
        """ Generic MailboxStatistics object that contains the statistics calculations. """
        self.mailbox = []

    def get_from_values(self):
        return [message['from'] for message in self.mailbox]

    def get_from_value_counts(self):
        return Counter(self.get_from_values())

    def get_n_most_frequent_from_values(self, n=1):
        return self.get_from_value_counts().most_common(n)

    def get_number_of_mails_per_hour(self):
        return Counter([message['sent'].strftime('%Y-%m-%d %H') for message in self.mailbox])

    def get_number_of_mails_per_hour_of_day(self):
        return Counter([message['sent'].strftime('%H') for message in self.mailbox])

    def get_number_of_mails_per_day(self):
        return Counter([message['sent'].strftime('%Y-%m-%d') for message in self.mailbox])


class OutlookMailboxStatistics(MailboxStatistics):
    def __init__(self, path_to_mbox_file, mbox_file_encoding, mbox_file_datetime_locale, mbox_file_datetime_format):
        """ Parses the text file that results from saving (multiple) messages in MS Outlook as text.
        :param path_to_mbox_file: full path to mbox file
        :param mbox_file_encoding: encoding of mbox file, for MS Outlook, this is typically latin1
        :param mbox_file_datetime_locale: locale to be used for parsing the datetime field
        :param mbox_file_datetime_format: format of the datetime string for parsing
        """
        MailboxStatistics.__init__(self)
        with codecs.open(path_to_mbox_file, 'r', mbox_file_encoding) as mailbox_file:
            self.raw_messages = mailbox_file.read().split("From:\t")
        for raw_message in self.raw_messages:
            if len(raw_message.split('\n')) > 5:
                message = {'from': raw_message.split('\n')[0].strip()}
                to_line = compile('To:\t(.+?)\r\n').findall(raw_message)
                message['to'] = [sub('[\'"]', '', item).strip()
                                 for item in to_line[0].split(';')] if len(to_line) > 0 else []
                locale.setlocale(locale.LC_ALL, mbox_file_datetime_locale)
                message['sent'] = datetime.strptime(compile('Sent:\t(.+?)\r\n').findall(raw_message)[0],
                                                    mbox_file_datetime_format)
                locale.resetlocale()
                self.mailbox.append(message)