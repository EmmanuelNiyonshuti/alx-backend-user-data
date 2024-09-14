#!/usr/bin/env python3
""" finds and obfuscate certain fields within a log message. """
import re
from typing import List


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """ obfuscate or hide passed in fields in message"""
    pattern = f'({"|".join(fields)})=[^{separator}]*'
    return re.sub(pattern, f"\\1={redaction}", message)
