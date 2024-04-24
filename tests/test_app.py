from http import HTTPStatus


def test_root(client):
    response = client.get('/')  # Act

    assert response.status_code == HTTPStatus.OK  # Assert
    assert response.json() == {'message': 'Olá, Mundo'}  # Assert


def test_html(client):
    response = client.get('/html')  # Act

    assert response.status_code == HTTPStatus.OK  # Assert
    assert response.headers['content-type'] == 'text/html; charset=utf-8'


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


def test_read_users(client):
    response = client.get('/users/')  # Act

    assert response.status_code == HTTPStatus.OK  # Assert
    assert response.json() == {
        'users': [
            {
                'username': 'user',
                'email': 'test@test.com',
                'id': 1,
            }
        ]
    }  # Assert


def test_update_user(client):
    response = client.put(
        '/users/1',
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
        'id': 1,
    }  # Assert


def test_update_user_not_found(client):
    response = client.put(
        '/users/0',
        json={
            'username': 'user',
            'email': 'adfasd@dasd.com',
            'password': 'new123456',
        },
    )  # Act

    assert response.status_code == HTTPStatus.NOT_FOUND  # Assert


def test_read_user(client):
    response = client.get('/users/1')  # Act

    assert response.status_code == HTTPStatus.OK  # Assert
    assert response.json() == {
        'username': 'user',
        'email': 'test@test.com',
        'id': 1,
    }  # Assert
    
def test_read_user_not_found(client):
    response = client.get('/users/0')  # Act

    assert response.status_code == HTTPStatus.NOT_FOUND  # Assert
    assert response.json() == {'detail': 'User not found'}  # Assert

def test_delete_user(client):
    response = client.delete('/users/1')  # Act

    assert response.status_code == HTTPStatus.OK  # Assert
    assert response.json() == {'message': 'User deleted'}  # Assert


def test_delete_user_not_found(client):
    response = client.delete('/users/0')  # Act

    assert response.status_code == HTTPStatus.NOT_FOUND  # Assert
    assert response.json() == {'detail': 'User not found'}  # Assert
