from app.extensions import bcrypt


def hash_password(password: str) -> str:
    return bcrypt.generate_password_hash(password).decode('utf-8')

def verify_password(hashed_password: str, plain_password: str) -> bool:
    return bcrypt.check_password_hash(hashed_password, plain_password)