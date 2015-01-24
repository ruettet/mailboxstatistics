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

    def __get_from_values(self):
        return [message['from'] for message in self.mailbox]

    def get_from_value_counts(self):
        """
        :return: A Counter object with the frequency of all possible 'from' values.
        """
        return Counter(self.__get_from_values())

    def __get_to_values(self):
        return [message['to'] for message in self.mailbox]

    def get_to_value_counts(self):
        """
        :return: A Counter object with the frequency of all possible 'to' value
        """
        return Counter(self.__get_to_values())

    def get_number_of_mails_per_hour(self):
        """
        :return: A Counter object with the amount of mails received per hour.
        """
        return Counter([message['sent'].strftime('%Y-%m-%d %H') for message in self.mailbox])

    def get_number_of_mails_per_hour_of_day(self):
        """
        :return: A Counter object with the total amount of mail per hour of the day [00 - 23].
        """
        return Counter([message['sent'].strftime('%H') for message in self.mailbox])

    def get_number_of_mails_per_day(self):
        """
        :return: A Counter object with the amount of mail per day.
        """
        return Counter([message['sent'].strftime('%Y-%m-%d') for message in self.mailbox])

    def get_number_of_mails_per_weekday(self):
        """
        :return: A Counter object the amount of mails per week day [0 - 6].
        """
        return Counter([message['sent'].weekday for message in self.mailbox])

    def __get_subject_tokens(self):
        return [token for message in self.mailbox for token in message['subject'].split()]

    def get_subject_token_frequencies(self):
        """
        :return: A Counter object with the frequencies of the (lowercased) tokens in the subject line.
        """
        return Counter(self.__get_subject_tokens())

    # TODO def get_subject_token_frequencies_by_from_values(self):


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
                subject_line = compile('Subject:\t(.+?)\r\n').findall(raw_message)
                message['subject'] = sub('(re|fw):', '', subject_line[0].lower()) if len(subject_line) > 0 else 'NA'
                self.mailbox.append(message)