import base64
import bcrypt


def hash_password(password: str) -> str:
    hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    return base64.b64encode(hashed).decode("utf-8")


def check_password(password: str, password_hash: str) -> bool:
    hashed_bytes = base64.b64decode(password_hash.encode("utf-8"))
    return bcrypt.checkpw(password.encode("utf-8"), hashed_bytes)
