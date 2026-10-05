"""Read loan records and find the ones that are overdue.

This is the only file that knows where the data comes from.
Right now it reads a CSV export from the library program.
If we later connect to the database directly, only this file changes.
"""

import csv
from dataclasses import dataclass
from datetime import date, datetime
from typing import Optional

# Column names in the CSV export.
# When we see the real export file, we only need to change the right-hand side.
COLUMNS = {
    "member_name": "member_name",
    "email": "email",
    "book_title": "book_title",
    "due_date": "due_date",
    "returned_date": "returned_date",
}

DATE_FORMAT = "%Y-%m-%d"


@dataclass
class Loan:
    member_name: str
    email: str
    book_title: str
    due_date: date
    returned_date: Optional[date]


def parse_date(text: str) -> Optional[date]:
    """Turn '2026-10-01' into a date. Empty text means 'no date'."""
    text = (text or "").strip()
    if not text:
        return None
    return datetime.strptime(text, DATE_FORMAT).date()


def read_loans_from_csv(path: str) -> tuple[list[Loan], list[str]]:
    """Read every row. Rows we cannot understand are skipped and reported."""
    loans: list[Loan] = []
    problems: list[str] = []

    with open(path, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for line_number, row in enumerate(reader, start=2):  # line 1 is the header
            try:
                due = parse_date(row[COLUMNS["due_date"]])
                if due is None:
                    raise ValueError("missing due date")
                loans.append(
                    Loan(
                        member_name=row[COLUMNS["member_name"]].strip(),
                        email=(row[COLUMNS["email"]] or "").strip(),
                        book_title=row[COLUMNS["book_title"]].strip(),
                        due_date=due,
                        returned_date=parse_date(row[COLUMNS["returned_date"]]),
                    )
                )
            except (KeyError, ValueError) as error:
                problems.append(f"line {line_number}: {error}")

    return loans, problems


def find_overdue(loans: list[Loan], today: date) -> list[Loan]:
    """A loan is overdue if it is not returned and the due date has passed.

    A book due *today* is not overdue yet.
    """
    return [
        loan
        for loan in loans
        if loan.returned_date is None and loan.due_date < today
    ]
