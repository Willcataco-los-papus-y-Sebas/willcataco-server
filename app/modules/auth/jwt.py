from datetime import datetime, timedelta, timezone

import jwt
from fastapi import HTTPException

from app.core.config import config


class JWTokens:
    @staticmethod
    def create_access_token_simple(user_id: str):
        time_loc = datetime.now(timezone.utc)
        expiration = time_loc + timedelta(minutes=int(config.token_time_expire))
        payload = {
            "sub": str(user_id),
            "exp": expiration,
            "iat": time_loc,
        }
        header = {"typ": "access+jwt"}
        token = jwt.encode(
            payload, key=config.token_key, algorithm=config.token_algorithm, headers=header
        )
        return token

    @staticmethod
    def create_access_token(user_id: str, role: str, scope: str):
        time_loc = datetime.now(timezone.utc)
        expiration = time_loc + timedelta(minutes=int(config.token_time_expire))
        payload = {
            "sub": str(user_id),
            "role": role,
            "scope": scope,
            "exp": expiration,
            "iat": time_loc,
        }
        header = {"typ": "access+jwt"}
        token = jwt.encode(
            payload, key=config.token_key, algorithm=config.token_algorithm, headers=header
        )
        return token

    @staticmethod
    def create_refresh_token(user_id: str, role: str, scope: str):
        time_loc = datetime.now(timezone.utc)
        expiration = time_loc + timedelta(minutes=int(config.refresh_token_time_expire))
        payload = {
            "sub": str(user_id),
            "role": role,
            "scope": scope,
            "exp": expiration,
            "iat": time_loc,
        }
        header = {"typ": "refresh+jwt"}
        token = jwt.encode(
            payload, key=config.token_key, algorithm=config.token_algorithm, headers=header
        )
        return token

    @staticmethod
    def create_token_reset(user_id : str):
        time_loc = datetime.now(timezone.utc)
        expiration = time_loc + timedelta(minutes=int(config.reset_token_time_expire))
        payload = {"sub": str(user_id), "exp": expiration, "iat": time_loc}
        header = {"typ": "reset-password+jwt"}
        token = jwt.encode(
            payload, key=config.token_key, algorithm=config.token_algorithm, headers=header
        )
        return token

    @staticmethod
    def decode_access_token(token: str) -> int:
        try:
            header = jwt.get_unverified_header(token)
            if header.get("typ") != "access+jwt":
                raise HTTPException(
                    status_code=401,
                    detail="Invalid token type"
                )
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

    @staticmethod
    def decode_access_payload(token: str) -> dict:
        """Decode access token and return full payload (includes scope/role)."""
        try:
            header = jwt.get_unverified_header(token)
            if header.get("typ") != "access+jwt":
                raise HTTPException(status_code=401, detail="Invalid token type")
            payload = jwt.decode(
                token, config.token_key, algorithms=[config.token_algorithm]
            )
            return payload
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token has expired")
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail="Invalid token")
        except Exception:
            raise HTTPException(status_code=401, detail="Could not validate credentials")

    @staticmethod
    def decode_refresh_token(token: str) -> int:
        try:
            header = jwt.get_unverified_header(token)
            if header.get("typ") != "refresh+jwt":
                raise HTTPException(
                    status_code=401,
                    detail="Invalid token type"
                )
            payload = jwt.decode(
                token, config.token_key, algorithms=[config.token_algorithm]
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
    def decode_refresh_payload(token: str) -> dict:
        """Decode refresh token and return full payload (includes scope/role)."""
        try:
            header = jwt.get_unverified_header(token)
            if header.get("typ") != "refresh+jwt":
                raise HTTPException(status_code=401, detail="Invalid token type")
            payload = jwt.decode(
                token, config.token_key, algorithms=[config.token_algorithm]
            )
            return payload
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Refresh token has expired - please login again")
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail="Invalid refresh token")
        except Exception:
            raise HTTPException(status_code=401, detail="Could not validate refresh token")
        
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

    @staticmethod
    def create_internal_request_token(user_id: str, role: str):
        time_loc = datetime.now(timezone.utc)
        minutes = getattr(config, "internal_token_time_expire", 10)
        expiration = time_loc + timedelta(minutes=int(minutes))
        jti = f"int-{user_id}-{int(time_loc.timestamp())}"
        payload = {"sub": str(user_id), "role": role, "exp": expiration, "iat": time_loc, "jti": jti}
        header = {"typ": "internal-login+jwt"}
        token = jwt.encode(payload, key=config.token_key, algorithm=config.token_algorithm, headers=header)
        return token, jti, expiration

    @staticmethod
    def decode_internal_request_token(token: str) -> dict:
        try:
            header = jwt.get_unverified_header(token)
            if header.get("typ") != "internal-login+jwt":
                raise HTTPException(status_code=401, detail="invalid token type")
            payload = jwt.decode(token, key=config.token_key, algorithms=[config.token_algorithm])
            return payload
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="internal token has expired")
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail="invalid token")
        except Exception:
            raise HTTPException(status_code=401, detail="could not validate token")