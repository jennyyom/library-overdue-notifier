"""Group overdue loans by person and write one friendly email per person."""

from dataclasses import dataclass
from datetime import date

from notifier.loans import Loan

LIBRARY_NAME = "교회 도서부"


@dataclass
class Reminder:
    member_name: str
    email: str
    subject: str
    body: str


def group_by_member(overdue: list[Loan]) -> dict[str, list[Loan]]:
    """Key by email (lowercase) so two rows for the same person become one email."""
    groups: dict[str, list[Loan]] = {}
    for loan in overdue:
        key = loan.email.lower()
        groups.setdefault(key, []).append(loan)
    return groups


def build_reminder(loans: list[Loan], today: date) -> Reminder:
    first = loans[0]
    lines = []
    for loan in sorted(loans, key=lambda l: l.due_date):
        days_late = (today - loan.due_date).days
        lines.append(f"  - {loan.book_title} (반납일 {loan.due_date}, {days_late}일 지남)")

    body = (
        f"{first.member_name}님, 안녕하세요.\n\n"
        f"{LIBRARY_NAME}입니다. 아래 책의 반납일이 지나 안내드립니다.\n\n"
        + "\n".join(lines)
        + "\n\n"
        "혹시 아직 읽고 계시면 도서부에 말씀해 주세요. 연장해 드릴게요.\n"
        "이미 반납하셨다면 이 메일은 무시해 주세요.\n\n"
        f"감사합니다.\n{LIBRARY_NAME} 드림"
    )
    subject = f"[{LIBRARY_NAME}] 도서 반납 안내 ({len(loans)}권)"
    return Reminder(first.member_name, first.email, subject, body)


def build_reminders(overdue: list[Loan], today: date) -> tuple[list[Reminder], list[Loan]]:
    """Return reminders to send, plus loans whose borrower has no email."""
    no_email = [loan for loan in overdue if not loan.email]
    with_email = [loan for loan in overdue if loan.email]

    reminders = [
        build_reminder(group, today) for group in group_by_member(with_email).values()
    ]
    return reminders, no_email
