import pytest
from sqlalchemy import select
from sqlalchemy.orm import Session

from fast_zero.database import get_session
from fast_zero.models import Todo, User
from fast_zero.settings import Settings


def test_get_session():
    session_gen = get_session()
    session = next(session_gen)

    assert isinstance(session, Session)
    assert str(session.get_bind().url) == Settings().DATABASE_URL

    try:
        next(session_gen)
    except StopIteration:
        pass
    else:
        pytest.fail('get_session generator yielded more than one value')


def test_create_user(session):
    new_user = User(username='user', password='123456', email='test@test.com')
    session.add(new_user)
    session.commit()

    user = session.scalar(select(User).where(User.username == 'user'))

    assert user.username == 'user'
    

def test_create_todo(session, user: User):
    todo = Todo(
        title= 'Test Todo',
        description= 'Test Description',
        state= 'draft',
        user_id= user.id 
    )
    
    session.add(todo)
    session.commit()
    session.refresh(todo)
    
    user = session.scalar(select(User).where(User.id == user.id))
    
    assert todo in user.todos
    
    