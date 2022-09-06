from typing import NamedTuple
import re

import utils.exceptions as exceptions

class Message(NamedTuple):
    amount: int
    category_text: str


def parse_message(raw_message: str) -> Message:
    regexp_result = re.match(r"([\d ]+) (.*)", raw_message)
    if not regexp_result or not regexp_result.group(0) \
            or not regexp_result.group(1) or not regexp_result.group(2):
        raise exceptions.NotCorrectMessage(
            "Don't quite understand your message. Write message in format, "
            "e.g:\n150 subway")

    amount = regexp_result.group(1).replace(" ", "")
    category_text = regexp_result.group(2).strip().lower()
    return Message(amount=amount, category_text=category_text)
