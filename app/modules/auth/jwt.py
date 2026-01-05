from datetime import datetime, timedelta, timezone

import jwt
from fastapi import HTTPException

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

    @staticmethod
    def decode_access_token(token: str) -> int:
        try:
            payload = jwt.decode(
                token, config.token_key, algorithms=[config.token_algorithm]
            )
            user_id = int(payload["sub"])
            return user_id
        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=401,
                detail="Token has expired"
            )
        except jwt.InvalidTokenError:
            raise HTTPException(
                status_code=401,
                detail="Invalid token"
            )
        except Exception:
            raise HTTPException(
                status_code=401,
                detail="Could not validate credentials"
            )
