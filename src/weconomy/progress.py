"""Heartbeat updates for long-running collection steps."""
from contextlib import contextmanager
from threading import Event, Thread
from time import monotonic


@contextmanager
def heartbeat(progress, message: str, interval: int = 10):
    if progress is None:
        yield
        return
    stop = Event()
    started = monotonic()

    def report():
        while not stop.wait(interval):
            progress({"event": "heartbeat", "message": message,
                      "elapsed_seconds": int(monotonic() - started)})

    thread = Thread(target=report, daemon=True)
    thread.start()
    try:
        yield
    finally:
        stop.set()
        thread.join()
