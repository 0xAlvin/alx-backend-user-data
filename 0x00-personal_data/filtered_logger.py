#!/usr/bin/env python3
"""
Regexing data
"""

from typing import List
import re
import logging
import os
import mysql.connector


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """a function that filters values in incoming log records"""
        log_message = super(RedactingFormatter, self).format(record)
        for field in self.fields:
            log_message = re.sub(
                r"({}=)([^{};]+)({})".format(field,
                                             self.SEPARATOR, self.SEPARATOR),
                r"\1{}{}".format(self.REDACTION, self.SEPARATOR),
                log_message
            )
        return log_message


PII_FIELDS = ["name", "email", "ssn", "password", "credit_card"]


def filter_datum(fields: List, redaction: str, message: str,
                 separator: str) -> str:
    """a function that returns the log message obfuscated"""
    for i in fields:
        obfuscate = re.sub(r'({}=)([^{}]+)({})'.format(i, separator,
                                                       separator),
                           r"\1{}{}".format(redaction, separator), message)
        message = obfuscate
    return obfuscate


def get_logger() -> logging.Logger:
    """a function that returns a logger object"""
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    handler = logging.StreamHandler()
    handler.setFormatter(RedactingFormatter(fields=PII_FIELDS))
    logger.addHandler(handler)

    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """a function that returns a connector to the database"""
    username = os.environ.get("PERSONAL_DATA_DB_USERNAME", "root")
    password = os.environ.get("PERSONAL_DATA_DB_PASSWORD", "")
    host = os.environ.get("PERSONAL_DATA_DB_HOST", "localhost")
    db_name = os.environ.get("PERSONAL_DATA_DB_NAME")

    db = mysql.connector.connect(
        host=host,
        user=username,
        password=password,
        database=db_name
    )

    return db


def main():
    """a main function that takes no arguments and returns nothing."""
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users;")
    fields = [i[0] for i in cursor.description]

    logger = logging.getLogger("user_data")
    for row in cursor:
        log_message = '; '.join([f"{fields[i]}={RedactingFormatter.REDACTION}"
                                 if fields[i]
                                in PII_FIELDS else f"{fields[i]}={row[i]}"
                                for i in range(len(row))])
        logger.info(log_message)

    cursor.close()
    db.close()


if __name__ == '__main__':
    main()
