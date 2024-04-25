from http import HTTPStatus


def test_root(client):
    response = client.get('/')  # Act

    assert response.status_code == HTTPStatus.OK  # Assert
    assert response.json() == {'message': 'Olá, Mundo'}  # Assert


def test_html(client):
    response = client.get('/html')  # Act

    assert response.status_code == HTTPStatus.OK  # Assert
    assert response.headers['content-type'] == 'text/html; charset=utf-8'
