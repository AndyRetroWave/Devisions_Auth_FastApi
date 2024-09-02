import bcrypt


async def hash_password(password):
    salt = bcrypt.gensalt()

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    hashed_password_str = hashed_password.decode('utf-8')
    return hashed_password_str


async def check_password(password, hashed_password):
    # Проверяем, соответствует ли введенный пароль хешированному паролю
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
