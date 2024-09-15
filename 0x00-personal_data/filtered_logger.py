#!/usr/bin/env python3
""" finds and obfuscate certain fields within a log message. """
import re
from typing import List
import logging
import os
import mysql.connector

PII_FIELDS = ("name", "email", "phone", "ssn", "password")


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


def get_logger() -> logging.Logger:
    """ returns a logging.logger object """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    formatter = RedactingFormatter(fields=PII_FIELDS)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    return logger


def get_db() -> mysql.connector.connection.MYSQLConnection:
    """ connect to mysql db using environmental variables"""
    try:
        db_name = os.environ["PERSONAL_DATA_DB_NAME"]
        db_host = os.environ["PERSONAL_DATA_DB_HOST"]
        db_pwd = os.environ["PERSONAL_DATA_DB_PASSWORD"]
        db_user = os.environ["PERSONAL_DATA_DB_USERNAME"]

        cnx = mysql.connector.connect(user=db_user, password=db_pwd,
                                  host=db_host, database=db_name)
        return cnx
    except:
        pass
