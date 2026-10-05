from datetime import date

from notifier.sent_log import SentLog


def test_not_sent_again_within_wait_days(tmp_path):
    log = SentLog(str(tmp_path / "log.json"), wait_days=7)
    log.mark_sent("a@example.com", date(2026, 10, 1))
    assert log.recently_sent("a@example.com", date(2026, 10, 7)) is True


def test_sent_again_after_wait_days(tmp_path):
    log = SentLog(str(tmp_path / "log.json"), wait_days=7)
    log.mark_sent("a@example.com", date(2026, 10, 1))
    assert log.recently_sent("a@example.com", date(2026, 10, 8)) is False


def test_log_survives_restart(tmp_path):
    path = str(tmp_path / "log.json")
    log = SentLog(path)
    log.mark_sent("a@example.com", date(2026, 10, 1))
    log.save()

    reopened = SentLog(path)
    assert reopened.recently_sent("A@example.com", date(2026, 10, 2)) is True
