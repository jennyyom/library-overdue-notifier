from datetime import date

from notifier.loans import Loan, find_overdue, read_loans_from_csv

TODAY = date(2026, 10, 4)


def make_loan(due, returned=None, email="a@example.com"):
    return Loan("Test", email, "Book", due, returned)


def test_past_due_and_not_returned_is_overdue():
    assert len(find_overdue([make_loan(date(2026, 10, 3))], TODAY)) == 1


def test_due_today_is_not_overdue_yet():
    assert find_overdue([make_loan(TODAY)], TODAY) == []


def test_returned_book_is_not_overdue():
    loan = make_loan(date(2026, 9, 1), returned=date(2026, 9, 2))
    assert find_overdue([loan], TODAY) == []


def test_bad_rows_are_reported_not_crashing(tmp_path):
    csv_file = tmp_path / "loans.csv"
    csv_file.write_text(
        "member_name,email,book_title,due_date,returned_date\n"
        "Good,g@example.com,Book A,2026-09-01,\n"
        "Bad,b@example.com,Book B,not-a-date,\n",
        encoding="utf-8",
    )
    loans, problems = read_loans_from_csv(str(csv_file))
    assert len(loans) == 1
    assert len(problems) == 1
    assert "line 3" in problems[0]
