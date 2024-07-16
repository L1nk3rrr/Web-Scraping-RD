import re

SPECIAL_QUOTES = re.compile(r'[“”]')


def remove_special_quotes(text: str) -> str:
    return SPECIAL_QUOTES.sub('', text)
