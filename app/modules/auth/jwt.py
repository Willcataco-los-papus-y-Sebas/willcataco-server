from datetime import datetime, timedelta, timezone

import jwt

from app.core.config import config


class JWTokens:
    @staticmethod
    def create_access_token(user_id: str):
        time_loc = datetime.now(timezone.utc)
        expiration = time_loc + timedelta(minutes=int(config.token_time_expire))
        payload = {"sub": str(user_id), "exp": expiration, "iat": time_loc}
        token = jwt.encode(
            payload, key=config.token_key, algorithm=config.token_algorithm
        )
        return token
