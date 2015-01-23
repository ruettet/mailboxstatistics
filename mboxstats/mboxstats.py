import codecs
import locale
from re import sub
from re import compile
from datetime import datetime
from collections import Counter

class MailboxStatistics(object):
    def __init__(self, path_to_mbox_file):
        self.mailbox = []
        with codecs.open(path_to_mbox_file, 'r', 'latin1') as mailbox_file:
            self.raw_messages = mailbox_file.read().split("From:\t")
        for raw_message in self.raw_messages:
            if len(raw_message.split('\n')) > 5:
                message = {}

                message['from'] = raw_message.split('\n')[0].strip()

                to_line = compile('To:\t(.+?)\r\n').findall(raw_message)
                message['to'] = [sub('[\'"]', '', item).strip() for item in to_line[0].split(';')] if len(to_line) > 0 else []

                locale.setlocale(locale.LC_ALL, 'nl_BE')
                message['sent'] = datetime.strptime(compile('Sent:\t(.+?)\r\n').findall(raw_message)[0], '%A %d %B %Y %H:%M')
                locale.resetlocale()

                self.mailbox.append(message)

    def get_mailbox_from_values(self):
        return [message['from'] for message in self.mailbox]

    def get_mailbox_from_value_counts(self):
        return Counter(self.get_mailbox_from_values())