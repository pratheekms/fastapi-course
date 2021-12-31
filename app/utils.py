from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_hash_pwd(password: str):
    return pwd_context.hash(password)
