from http import HTTPStatus

import pytest
from fastapi import HTTPException
from jwt import decode

from fast_zero.security import (
    create_access_token,
    get_current_user,
    settings,
)


def test_jwt():
    data = {'test': 'test'}
    token = create_access_token(data)

    decoded = decode(
        token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
    )

    assert decoded['test'] == 'test'
    assert decoded['exp']


@pytest.mark.asyncio()
async def test_get_current_user_valid_token_user_exists(session, user):
    token_data = {'sub': user.email}  # Arrange
    token = create_access_token(token_data)  # Arrange

    result = await get_current_user(session=session, token=token)  # Act

    assert result == user  # Assert


@pytest.mark.asyncio()
async def test_get_current_user_no_sub_in_token(session):
    token_data = {}  # Arrange: no 'sub' field in the token data
    token = create_access_token(token_data)  # Arrange

    with pytest.raises(HTTPException) as exc_info:
        await get_current_user(session=session, token=token)  # Act

    assert exc_info.value.status_code == HTTPStatus.UNAUTHORIZED  # Assert
    assert exc_info.value.detail == 'Could not validate credentials'  # Assert


@pytest.mark.asyncio()
async def test_get_current_user_valid_token_user_not_exists(session):
    token_data = {'sub': 'dontexist@gmail.com'}  # Arrange
    token = create_access_token(token_data)  # Arrange

    with pytest.raises(HTTPException) as exc_info:
        await get_current_user(session=session, token=token)  # Act

    assert exc_info.value.status_code == HTTPStatus.UNAUTHORIZED  # Assert


@pytest.mark.asyncio()
async def test_get_current_user_invalid_token(session):
    token = 'invalidtoken'  # Arrange

    with pytest.raises(HTTPException) as exc_info:
        await get_current_user(session=session, token=token)  # Act

    assert exc_info.value.status_code == HTTPStatus.UNAUTHORIZED  # Assert
    assert exc_info.value.detail == 'Could not validate credentials'  # Assert
