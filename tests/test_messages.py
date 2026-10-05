from datetime import date

from notifier.loans import Loan
from notifier.messages import build_reminders

TODAY = date(2026, 10, 4)


def test_two_books_same_person_become_one_email():
    overdue = [
        Loan("Kim", "kim@example.com", "Book A", date(2026, 9, 20), None),
        Loan("Kim", "KIM@example.com", "Book B", date(2026, 9, 25), None),
    ]
    reminders, _ = build_reminders(overdue, TODAY)
    assert len(reminders) == 1
    assert "Book A" in reminders[0].body and "Book B" in reminders[0].body
    assert "(2권)" in reminders[0].subject


def test_member_without_email_goes_to_manual_list():
    overdue = [Loan("Choi", "", "Book C", date(2026, 9, 1), None)]
    reminders, no_email = build_reminders(overdue, TODAY)
    assert reminders == []
    assert no_email[0].member_name == "Choi"


def test_days_late_is_shown():
    overdue = [Loan("Lee", "lee@example.com", "Book D", date(2026, 10, 1), None)]
    reminders, _ = build_reminders(overdue, TODAY)
    assert "3일 지남" in reminders[0].body


def test_shared_email_different_members_get_separate_reminders():
    overdue = [
        Loan("김은혜", "kim.family@example.com", "Book A", date(2026, 9, 20), None),
        Loan("김요한", "kim.family@example.com", "Book B", date(2026, 9, 25), None),
    ]
    reminders, _ = build_reminders(overdue, TODAY)
    assert len(reminders) == 2
    names = sorted(r.member_name for r in reminders)
    assert names == ["김요한", "김은혜"]