#!/usr/bin/env python3
""" Filter log data."""
import re


def filter_datum(fields, redaction, message, separator):
    """ finds and obfuscate certain fields within a log message. """
    pattern = f'({"|".join(fields)})=[^{separator}]*'
    return re.sub(pattern, f"\\1={redaction}", message)



