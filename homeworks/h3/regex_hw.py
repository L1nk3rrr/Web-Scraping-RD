import re
from pathlib import Path


def save_regex_matches(text: str, regex_pattern: str, filename: str) -> None:
    matches = re.findall(regex_pattern, text)
    print(f"len {len(matches)}, {matches=}")
    Path(f"results/{filename}").write_text('\n'.join(matches))


def parse_dates(text: str):
    date_pattern = (r"\b\d{2}[-\/\.\s]\d{2}[-\/\.\s](?:1|2)\d{3}\b|\b(?:1|2)\d{3}[-\/\.\s]\d{2}[-\/\.\s]\d{2}\b|"
                    r"\b(?:January|February|March|April|May|June|July|August|September|October|November|December) \d{1,2},? ?(?:1|2)\d{3}\b")
    save_regex_matches(text, date_pattern, "parsed_dates.txt")


def parse_emails(text: str):
    # maybe here can be better regex with full validation of domain parts, but for now it enough?
    email_pattern = r"\b[\S\d._%+-]+@[\S\d.-]+\.[\w]{2,}\b"
    save_regex_matches(text, email_pattern, "parsed_emails.txt")


if __name__ == "__main__":
    file = Path("example_text.txt")
    raw_text = file.read_text()
    parse_dates(raw_text)
    parse_emails(raw_text)
