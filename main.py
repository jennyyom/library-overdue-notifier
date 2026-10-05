"""Find overdue library books and email the borrowers.

Usage:
    python main.py data/sample_loans.csv            # preview only (safe, nothing is sent)
    python main.py data/sample_loans.csv --send     # really send emails
    python main.py data/sample_loans.csv --today 2026-10-05   # pretend today is another day
"""

import argparse
import os
from datetime import date

from notifier.loans import find_overdue, read_loans_from_csv
from notifier.mailer import print_reminder, send_reminders
from notifier.messages import build_reminders
from notifier.sent_log import SentLog

# Keep the log next to this file, not in whatever folder the program is started from
# (Windows Task Scheduler starts programs in C:\Windows\System32 by default).
SENT_LOG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sent_log.json")


def main() -> None:
    parser = argparse.ArgumentParser(description="Overdue book reminder")
    parser.add_argument("csv_path", help="CSV file exported from the library program")
    parser.add_argument("--send", action="store_true", help="really send emails")
    parser.add_argument("--today", help="use this date instead of today (YYYY-MM-DD)")
    args = parser.parse_args()

    today = date.fromisoformat(args.today) if args.today else date.today()

    # 1. Read the export
    loans, problems = read_loans_from_csv(args.csv_path)
    for problem in problems:
        print(f"[skipped] {problem}")

    # 2. Keep only overdue loans, and build one email per person
    overdue = find_overdue(loans, today)
    reminders, no_email = build_reminders(overdue, today)

    # 3. Skip people we already reminded recently
    log = SentLog(SENT_LOG_PATH)
    to_send = [r for r in reminders if not log.recently_sent(r.email, today)]
    skipped = len(reminders) - len(to_send)

    # 4. Preview or send
    if args.send:
        send_reminders(to_send)
        for reminder in to_send:
            log.mark_sent(reminder.email, today)
        log.save()
    else:
        for reminder in to_send:
            print_reminder(reminder)
        print("=" * 60)
        print("DRY RUN: nothing was sent. Add --send to send for real.")

    # 5. Summary for the librarian
    print(f"\nToday: {today}")
    print(f"Loans read: {len(loans)}, overdue: {len(overdue)}")
    print(f"Reminders {'sent' if args.send else 'to send'}: {len(to_send)}")
    print(f"Skipped (reminded in the last {log.wait_days} days): {skipped}")
    if no_email:
        print("No email on file, please contact directly:")
        for loan in no_email:
            print(f"  - {loan.member_name}: {loan.book_title} (due {loan.due_date})")


if __name__ == "__main__":
    main()
