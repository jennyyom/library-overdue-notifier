# Library Overdue Notifier

Sends a friendly email reminder to church library members whose books are past due.

The church library runs on an older Windows program. This tool does not change that
program or its data. It reads an exported list of loans, finds overdue books, and
emails each borrower once, listing all of their overdue books in a single message.

## How It Works

1. **Read** a CSV export of loans from the library program (`notifier/loans.py`)
2. **Find overdue loans**: not returned, and the due date is before today
3. **Group by person** so someone with three late books gets one email (`notifier/messages.py`)
4. **Skip people reminded in the last 7 days** using a small local log (`notifier/sent_log.py`)
5. **Preview or send** the emails (`notifier/mailer.py`)
6. **List members with no email** so a librarian can contact them directly

## Run It

```bash
pip install -r requirements.txt

# Preview only (default). Nothing is sent.
python main.py data/sample_loans.csv --today 2026-10-04

# Send for real (needs email settings below)
python main.py path/to/export.csv --send
```

### Email settings (only needed with `--send`)

Set these as environment variables. Never put the password in the code.

| Variable | Example |
|---|---|
| `SMTP_USER` | library@yourchurch.org |
| `SMTP_PASSWORD` | Gmail App Password |
| `SMTP_HOST` | smtp.gmail.com (default) |
| `SMTP_PORT` | 587 (default) |

## Tests

```bash
python -m pytest -v
```

The tests cover the edge cases that matter most:

- A book due **today** is not overdue yet
- Returned books are never reminded
- Two books for the same person (even with different email capitalization) become **one** email
- Members **without an email** go to a manual contact list instead
- Nobody is reminded twice within 7 days, even after the program restarts
- A row with a bad date is reported and skipped instead of crashing the run

## Status

- [x] Read CSV export, find overdue loans, build one email per person
- [x] Dry-run preview by default
- [x] Duplicate-send protection
- [ ] Confirm the real export format and map its columns in `notifier/loans.py`
- [ ] Run weekly with Windows Task Scheduler
- [ ] (Optional) Read the library database directly instead of a CSV export
- [ ] (Optional) Text message reminders for members who opt in

`data/sample_loans.csv` contains made-up names only.
# library-overdue-notifier
