from datetime import datetime, timedelta, timezone

import jwt
from fastapi import HTTPException

from app.core.config import config


class JWTokens:
    @staticmethod
    def create_access_token(user_id: str):
        time_loc = datetime.now(timezone.utc)
        expiration = time_loc + timedelta(minutes=int(config.token_time_expire))
        payload = {"sub": str(user_id), "exp": expiration, "iat": time_loc, "type": "access"}
        token = jwt.encode(
            payload, key=config.token_key, algorithm=config.token_algorithm
        )
        return token

    @staticmethod
    def create_refresh_token(user_id: str):
        """Create a long-lived refresh token (7 days by default)"""
        time_loc = datetime.now(timezone.utc)
        expiration = time_loc + timedelta(minutes=int(config.refresh_token_time_expire))
        payload = {"sub": str(user_id), "exp": expiration, "iat": time_loc, "type": "refresh"}
        token = jwt.encode(
            payload, key=config.token_key, algorithm=config.token_algorithm
        )
        return token

    @staticmethod
    def create_token_reset(user_id : str):
        time_loc = datetime.now(timezone.utc)
        expiration = time_loc + timedelta(minutes=int(config.reset_token_time_expire))
        payload = {"sub": str(user_id), "exp": expiration, "iat": time_loc}
        header = {"typ": "password-reset+jwt"}
        token = jwt.encode(
            payload, key=config.token_key, algorithm=config.token_algorithm, headers=header
        )
        return token

    @staticmethod
    def decode_access_token(token: str) -> int:
        try:
            payload = jwt.decode(
                token, config.token_key, algorithms=[config.token_algorithm]
            )
            token_type = payload.get("type")
            if token_type != "access":
                raise HTTPException(
                    status_code=401,
                    detail="Invalid token type"
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

    @staticmethod
    def decode_refresh_token(token: str) -> int:
        try:
            payload = jwt.decode(
                token, config.token_key, algorithms=[config.token_algorithm]
            )
            token_type = payload.get("type")
            if token_type != "refresh":
                raise HTTPException(
                    status_code=401,
                    detail="Invalid token type"
                )
            user_id = int(payload["sub"])
            return user_id
        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=401,
                detail="Refresh token has expired - please login again"
            )
        except jwt.InvalidTokenError:
            raise HTTPException(
                status_code=401,
                detail="Invalid refresh token"
            )
        except Exception:
            raise HTTPException(
                status_code=401,
                detail="Could not validate refresh token"
            )
        
    @staticmethod
    def decode_reset_token(token : str) -> int:
        try:
            header = jwt.get_unverified_header(token)
            if header.get("typ") != "reset-password+jwt":
                raise HTTPException(
                    detail="invalid token type",
                    status_code=401
                )
            payload = jwt.decode(token, key=config.token_key, algorithms=[config.token_algorithm])
            user_id = int(payload["sub"])
            return user_id
        except jwt.ImmatureSignatureError:
            raise HTTPException(
                status_code=401,
                detail="reset token has expired"
            )
        except jwt.InvalidTokenError:
            raise HTTPException(
                status_code=401,
                detail="invalid token"
            )
        except Exception:
            raise HTTPException(
                status_code=401,
                detail="could not validate token"
            )