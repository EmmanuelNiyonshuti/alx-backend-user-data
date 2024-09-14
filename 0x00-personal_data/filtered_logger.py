#!/usr/bin/env python3
""" finds and obfuscate certain fields within a log message. """
import re
from typing import List
import logging


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """ obfuscate or hide passed in fields in message log"""
    pattern = f'({"|".join(fields)})=[^{separator}]*'
    return re.sub(pattern, f"\\1={redaction}", message)


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """ filter values in incoming log records """
        formated_msg = super(RedactingFormatter, self).format(record)

        return filter_datum(self.fields, self.REDACTION,
                            formated_msg, self.SEPARATOR)
