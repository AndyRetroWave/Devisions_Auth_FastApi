import re
import bcrypt


async def hash_password(password):
    pattern = r'^(?=.*[A-Z])(?=.*[!@#$%^&*()_+\-=\[\]{};\':"\\|,.<>\/?])(?=.{8,})'
    if re.match(pattern, password):
        salt = bcrypt.gensalt()

        hashed_password = bcrypt.hashpw(password.encode("utf-8"), salt)
        hashed_password_str = hashed_password.decode("utf-8")

        return hashed_password_str
    return False


async def check_password(password, hashed_password):
    # Проверяем, соответствует ли введенный пароль хешированному паролю
    return bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))
