from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Hasher:
    @staticmethod
    def verify_password(raw_password, hashed_password):
        return pwd_context.verify(raw_password, hashed_password)

    @staticmethod
    def hash_password(raw_password):
        return pwd_context.hash(raw_password)
