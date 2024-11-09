#!/usr/bin/env python3
""" logging module """
import re
from typing import (List,)
import logging
import mysql.connector
from os import environ


db_config = {
             'username': environ.get('PERSONAL_DATA_DB_USERNAME', 'root'),
             'password': environ.get('PERSONAL_DATA_DB_PASSWORD', ''),
             'host': environ.get('PERSONAL_DATA_DB_HOST', 'localhost'),
             'database': environ.get('PERSONAL_DATA_DB_NAME')
          }


def get_db() -> mysql.connector.connection.MySQLConnection:
    """ returns a mysql connector object """
    connection = mysql.connector.connect(**db_config)
    return connection


PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def filter_datum(fields: List[str],
                 redaction: str,
                 message: str,
                 separator: str) -> str:
    """ returns log message obfuscated """
    for f in fields:
        message = re.sub(f'{f}=.*?{separator}',
                         f'{f}={redaction}{separator}', message)
    return message


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class"""

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """ initailizer func"""
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        record.msg = filter_datum(self.fields, self.REDACTION,
                                  record.getMessage(), self.SEPARATOR)
        return super(RedactingFormatter, self).format(record)


def get_logger() -> logging.Logger:
    """ gets and returns a logger object"""
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    stream_handler = logging.StreamHandler()
    formatter = RedactingFormatter(fields=PII_FIELDS)
    stream_handler.setFormatter(formatter)

    logger.addHandler(stream_handler)
    logger.propagate = False
    return logger


def main():
    """ main function """
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users;')

    logger = get_logger()
    for (name,
         email,
         phone,
         ssn,
         password,
         ip,
         last_login,
         user_agent) in cursor.fetchall():
        message = f'name={name}; email={email}; phone={phone};\
        ssn={ssn};password={password};\
        ip={ip}; last_login={last_login};\
        user_agent={user_agent}'
        logger.info(message)


if __name__ == "__main__":
    main()
