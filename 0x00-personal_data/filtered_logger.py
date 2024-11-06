#!/usr/bin/env python3
""" logging module """
import re
from typing import (List,)


def filter_datum(fields: List[str],
                 redaction: str,
                 message: str,
                 separator: str) -> str:
    """ returns log message obfuscated """
    for item in fields:
        message = re.sub(f"{item}=[^{separator}]*",
                         f"{item}={redaction}", message)
        return message
