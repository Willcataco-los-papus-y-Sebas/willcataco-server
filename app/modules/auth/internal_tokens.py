from datetime import datetime, timezone
from typing import Dict, Tuple

class InternalTokenStore:
    _pending: Dict[str, datetime] = {}
    _used: Dict[str, datetime] = {}

    @classmethod
    def register(cls, jti: str, expires_at: datetime) -> None:
        cls._pending[jti] = expires_at

    @classmethod
    def consume(cls, jti: str) -> bool:
        now = datetime.now(timezone.utc)
        exp = cls._pending.get(jti)
        if exp is None:
            return False
        if now > exp:
            cls._pending.pop(jti, None)
            return False
        cls._pending.pop(jti, None)
        cls._used[jti] = now
        return True

    @classmethod
    def is_used(cls, jti: str) -> bool:
        return jti in cls._used
