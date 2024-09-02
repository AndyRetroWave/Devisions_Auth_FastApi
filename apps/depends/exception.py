from fastapi import HTTPException


class UserExpectationException(HTTPException):
    status_code = 500
    detail = ""

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class NotUserException(UserExpectationException):
    status_code = 401
    detail = "Не найден данный пользователь!"


class IncorrectPasswordException(UserExpectationException):
    status_code = 401
    detail = "Неверный пароль!"


class NotActiveException(UserExpectationException):
    status_code = 401
    detail = "Пользователь не активен!"


class IncorrectTokenException(UserExpectationException):
    status_code = 401
    detail = "Неверный токен!"
