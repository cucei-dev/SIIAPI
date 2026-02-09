from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
from app.core.config import settings
from app.modules.auth.schemas import Token, RefreshTokenData, AccessTokenData
import uuid
from ShieldCipher.encryption.symmetric import encrypt as sc_encrypt, decrypt as sc_decrypt

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str = settings.DUMMY_HASH) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: AccessTokenData) -> Token:
    #now = datetime.now(timezone.utc)
    now = datetime.now()
    expire = now + timedelta(days=1)

    data.exp = int(expire.timestamp())
    data.iat = int(now.timestamp())
    data.iss = settings.APP_SITE
    data.jti = str(uuid.uuid4())

    JWT = jwt.encode(data.model_dump(), settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    HASH = hash_password(JWT)

    return Token(token=JWT, data=data, hash=HASH)

def create_refresh_token(data: RefreshTokenData) -> Token:
    #now = datetime.now(timezone.utc)
    now = datetime.now()
    expire = now + timedelta(days=1)

    data.exp = int(expire.timestamp())
    data.iat = int(now.timestamp())
    data.jti = str(uuid.uuid4())

    JWT = jwt.encode(data.model_dump(), settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    HASH = hash_password(JWT)

    return Token(token=JWT, data=data, token_hash=HASH)

def check_token(token: str, token_type: str) -> dict | None:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM], audience=settings.APP_ENV)
        if payload.get("type") == token_type:
            return payload
        else:
            return None
    except jwt.JWTError:
        return None

def encrypt(message: str) -> str:
    encrypted_result = sc_encrypt(secret=settings.SECRET_KEY, message=message)
    return f"{encrypted_result[0]}${encrypted_result[1]}${encrypted_result[2].hex()}${encrypted_result[3].hex()}"

def decrypt(encrypted_text: str, split="$") -> str:
    encrypted = encrypted_text.split(split)
    algorithm = encrypted[0]
    length = int(encrypted[1])
    salt = bytes.fromhex(encrypted[2])
    ciphertext = bytes.fromhex(encrypted[3])

    return sc_decrypt(
        settings.SECRET_KEY,
        algorithm,
        length,
        salt,
        ciphertext,
    )
