from http import HTTPStatus

import factory.fuzzy

from fast_zero.models import Todo, TodoState


class TodoFactory(factory.Factory):
    class Meta:
        model = Todo
    
    title = factory.Faker('sentence')
    description = factory.Faker('sentence')
    state = factory.fuzzy.FuzzyChoice(TodoState)
    user_id = -1


def test_create_todo(client, token):
    response = client.post(
        '/todos/',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'id': 1,
            'title': 'Test Todo',
            'description': 'Test Description',
            'state': 'draft'
        }
    ) #Act
    assert response.json() == {
        'id' : 1,
        'title': 'Test Todo',
        'description': 'Test Description',
        'state': 'draft',
    } #Assert


def test_list_todos_should_return_5_todos(session, client, user, token):
    expected_todos = 5
    session.bulk_save_objects(TodoFactory.create_batch(
        expected_todos, 
        user_id=user.id))
    session.commit()
    
    response = client.get(
        '/todos/',
        headers={'Authorization': f'Bearer {token}'}
    )
    
    assert len(response.json()['todos']) == expected_todos
    
    
def test_list_todos_pagination_should_return_2_todos(
    session, client, user, token
):
    expected_todos = 2
    session.bulk_save_objects(TodoFactory.create_batch(5, user_id=user.id))
    session.commit()
    
    response = client.get(
        '/todos/?offset=1&limit=2',
        headers={'Authorization': f'Bearer {token}'}
    )
    
    assert len(response.json()['todos']) == expected_todos
    
    
def test_list_todos_filter_title_return_5_todos(
    session, user, client, token
):
    expected_todos = 5
    session.bulk_save_objects(
        TodoFactory.create_batch(5, user_id=user.id, title='Test Todo 1')
    )
    session.commit()
    
    response = client.get(
        '/todos/?title=Test Todo 1',
        headers={'Authorization': f'Bearer {token}'}
    )
    
    assert len(response.json()['todos']) == expected_todos
    
    
def test_list_todos_filter_description_should_return_5_todos(
    session, user, client, token
):
    expected_todos = 5
    session.bulk_save_objects(
        TodoFactory.create_batch(5, user_id=user.id, description='description')
        )
    session.commit()
    
    response = client.get(
        '/todos/?description=description',
        headers={'Authorization': f'Bearer {token}'},
    )
    
    assert len(response.json()['todos']) == expected_todos


def test_list_todos_filter_state_should_return_5_todos(
    session, user, client, token
):
    expected_todos = 5
    session.bulk_save_objects(
        TodoFactory.create_batch(5, user_id=user.id, state=TodoState.draft))
    session.commit()
    
    response = client.get(
        '/todos/?state=draft',
        headers={'Authorization': f'Bearer {token}'}
    )
    
    assert len(response.json()['todos']) == expected_todos
    
    
def test_list_todos_filter_combined_should_return_5_todos(
    session, user, client, token
):
    expected_todos = 5
    session.bulk_save_objects(
        TodoFactory.create_batch(
            5, 
            user_id=user.id,
            state=TodoState.draft,
            title='Test todo combined',
            description='combined description')
    )
    
    session.bulk_save_objects(
        TodoFactory.create_batch(
            3, 
            user_id=user.id,
            title='Other Title',
            description='other description',
            state=TodoState.todo,
        )
    )
    session.commit()
    
    response = client.get(
        '/todos/?state=draft&title=Test todo combined&description=combined description',
        headers={'Authorization': f'Bearer {token}'},
    )
    
    assert len(response.json()['todos']) == expected_todos
    

def test_patch_todo_error(client, token):
    response =  client.patch(
        '/todos/10',
        headers={'Authorization': f'Bearer {token}'},
        json={},
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Task not found'}
    

def test_patch_todo(session, client, user, token):
    todo = TodoFactory(user_id=user.id)
    
    session.add(todo)
    session.commit()
    
    response = client.patch(
        f'/todos/{todo.id}/',
        headers={'Authorization': f'Bearer {token}'},
        json={'title': 'test!'},
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json()['title'] == 'test!'

    
def test_delete_todo(session, client, user, token):
    todo = TodoFactory(user_id=user.id)
    
    session.add(todo)
    session.commit()
    
    response = client.delete(
        f'/todos/{todo.id}',
        headers={'Authorization': f'Bearer {token}'}
    )
    
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'message': 'Task has been deleted successfully'
    }


def test_delete_todo_error(client, token):
    response = client.delete(
        f'/todos/{10}',headers={'Authorization': f'Bearer {token}'}
    )
    
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Task not found'}
    