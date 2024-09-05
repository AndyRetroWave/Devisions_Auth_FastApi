import pytest

from apps.auth.validation import validate_user_login


@pytest.mark.parametrize(
    ("email", "password", "test_email"),
    [("john.doe@example.com", "Andreykiller566576!", "john.doe@example.com")],
)
async def test_validate_user_login(email: str, password: str, test_email):
    result = await validate_user_login(email, password)
    assert result.email == test_email


# @pytest.mark.parametrize(('token', "result_token"),
#                          [()])
# async def test_get_current_token_payload()
