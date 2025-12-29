from __future__ import annotations

from dataclasses import dataclass, field
from collections import deque
from time import time
from typing import Deque, Tuple, Optional


@dataclass
class TokenVelocityMonitor:
    """
    Tracks token consumption rate using a rolling time window.
    """
    window_seconds: int = 30
    _events: Deque[Tuple[int, float]] = field(default_factory=deque)

    def add(self, tokens_used: int, ts: Optional[float] = None) -> None:
        if ts is None:
            ts = time()
        if tokens_used < 0:
            tokens_used = 0
        self._events.append((tokens_used, ts))
        self._trim(ts)

    def _trim(self, now: float) -> None:
        cutoff = now - self.window_seconds
        while self._events and self._events[0][1] < cutoff:
            self._events.popleft()

    def tokens_per_second(self, now: Optional[float] = None) -> float:
        if now is None:
            now = time()
        self._trim(now)
        if not self._events:
            return 0.0
        total = sum(t for t, _ in self._events)
        earliest = self._events[0][1]
        dt = max(1e-6, now - earliest)
        return total / dt

    def snapshot(self) -> dict:
        now = time()
        return {
            "window_seconds": self.window_seconds,
            "tokens_per_second": self.tokens_per_second(now),
            "events_in_window": len(self._events),
            "tokens_in_window": sum(t for t, _ in self._events),
        }
