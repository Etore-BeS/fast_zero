from http import HTTPStatus

from fast_zero.schemas import UserPublic


def test_create_user(client):
    response = client.post(
        '/users/',
        json={
            'username': 'user',
            'email': 'test@test.com',
            'password': '123456',
        },
    )  # Act

    assert response.status_code == HTTPStatus.CREATED  # Assert
    assert response.json() == {
        'username': 'user',
        'email': 'test@test.com',
        'id': 1,
    }  # Assert


def test_create_user_already_exists(client, user):
    response = client.post(
        '/users/',
        json={
            'username': 'Teste',
            'email': 'test@test.com',
            'password': '123456',
        },
    )  # Act

    assert response.status_code == HTTPStatus.BAD_REQUEST  # Assert
    assert response.json() == {'detail': 'Email already registered'}  # Assert


def test_read_users(client, user, token):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get(
        '/users/', headers={'Authorization': f'Bearer {token}'}
    )  # Act
    assert response.json() == {'users': [user_schema]}


def test_update_user(client, user, token):
    response = client.put(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'user',
            'email': 'test@test.com',
            'password': 'new123456',
        },
    )  # Act

    assert response.status_code == HTTPStatus.OK  # Assert
    assert response.json() == {
        'username': 'user',
        'email': 'test@test.com',
        'id': user.id,
    }  # Assert


def test_update_user_forbidden(client, user, token):
    response = client.put(
        f'/users/{user.id + 1}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'user',
            'email': 'test@test.com',
            'password': 'new123456',
        },
    )  # Act

    assert response.status_code == HTTPStatus.FORBIDDEN  # Assert
    assert response.json() == {'detail': 'Not enough permissions'}  # Assert


def test_read_user(client, user, token):
    response = client.get(
        f'/users/{user.id}', headers={'Authorization': f'Bearer {token}'}
    )  # Act

    assert response.status_code == HTTPStatus.OK  # Assert
    assert response.json() == {
        'username': 'Teste',
        'email': 'test@test.com',
        'id': user.id,
    }  # Assert


def test_read_user_forbidden(client, user, token):
    response = client.get(
        f'/users/{user.id + 1}', headers={'Authorization': f'Bearer {token}'}
    )  # Act

    assert response.status_code == HTTPStatus.FORBIDDEN  # Assert
    assert response.json() == {'detail': 'Not enough permissions'}  # Assert


def test_read_user_not_found(client, user, token):
    user.id = -1
    response = client.get(
        '/user/{user.id}', headers={'Authorization': f'Bearer {token}'}
    )  # Act
    assert response.status_code == HTTPStatus.NOT_FOUND  # Assert
    assert response.json() == {'detail': 'Not Found'}  # Assert


def test_delete_user(client, user, token):
    response = client.delete(
        f'/users/{user.id}', headers={'Authorization': f'Bearer {token}'}
    )  # Act

    assert response.status_code == HTTPStatus.OK  # Assert
    assert response.json() == {'message': 'User deleted'}  # Assert


def test_delete_user_forbidden(client, user, token):
    response = client.delete(
        f'/users/{user.id + 1}', headers={'Authorization': f'Bearer {token}'}
    )  # Act

    assert response.status_code == HTTPStatus.FORBIDDEN  # Assert
    assert response.json() == {'detail': 'Not enough permissions'}  # Assert
