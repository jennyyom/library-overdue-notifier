"""Remember who we emailed and when, so nobody gets the same reminder every day.

The log is a small JSON file kept next to this program.
We never write anything into the library program's own data.
"""

import json
import os
from datetime import date, timedelta


class SentLog:
    def __init__(self, path: str, wait_days: int = 7):
        self.path = path
        self.wait_days = wait_days
        self._last_sent: dict[str, str] = {}
        if os.path.exists(path):
            with open(path, encoding="utf-8") as f:
                self._last_sent = json.load(f)

    def recently_sent(self, email: str, today: date) -> bool:
        last = self._last_sent.get(email.lower())
        if last is None:
            return False
        return today - date.fromisoformat(last) < timedelta(days=self.wait_days)

    def mark_sent(self, email: str, today: date) -> None:
        self._last_sent[email.lower()] = today.isoformat()

    def save(self) -> None:
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(self._last_sent, f, ensure_ascii=False, indent=2)
