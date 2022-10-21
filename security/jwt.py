import datetime
from jose import jwt, JWTError
from config import SECRET, ALGORITHM


class JWT:
    @staticmethod
    def decode_token(token):
        try:
            decoded_token = jwt.decode(token=token, key=SECRET, algorithms=[ALGORITHM])
        except JWTError as e:
             raise e
        return decoded_token

    @staticmethod
    def gen_new_access_token(data: dict, expiration_delta: int = 15):
        expires = datetime.datetime.utcnow() + datetime.timedelta(expiration_delta)
        data.update({'exp': expires})

        access_token = jwt.encode(
            claims=data, key=SECRET, algorithm=ALGORITHM)
        return access_token
