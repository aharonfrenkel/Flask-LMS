from app.extensions import bcrypt


def hash_password(password: str) -> str:
    return bcrypt.generate_password_hash(password).decode('utf-8')