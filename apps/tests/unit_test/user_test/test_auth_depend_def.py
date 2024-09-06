from datetime import timedelta

import pytest

from apps.auth.jwt import decode_jwt, encode_jwt
from apps.auth.validation import (
    get_current_auth_user,
    get_current_token_payload,
    validate_user_login,
)
from apps.tests.integtation_test.test_auth_api import FAKE


@pytest.mark.asycio
@pytest.mark.parametrize(
    ("email", "password", "test_email"),
    [("john.doe@example.com", "Andreykiller566576!", "john.doe@example.com")],
)
async def test_validate_user_login(email: str, password: str, test_email):
    result = await validate_user_login(email, password)
    assert result.email == test_email


@pytest.mark.asyncio
async def test_get_current_token_payload():
    access_token = await encode_jwt(
        payload={
            "sub": "john.doe@example.com",
            "type": "access_token",
            "given_name": FAKE.first_name_male(),
            "family_name": FAKE.last_name_male(),
            "iat": FAKE.date_time(),
            "exp": FAKE.date_time() + timedelta(minutes=15),
        }
    )
    payload = await decode_jwt(token=access_token)
    payload_result = await get_current_token_payload(access_token)
    user_data = await get_current_auth_user(payload_result)
    print(user_data)
    assert payload_result == payload
