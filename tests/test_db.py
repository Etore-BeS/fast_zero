from sqlalchemy import select

from fast_zero.models import User


def test_create_user(session):
    new_user = User(username='user', password='123456', email='test@test.com')
    session.add(new_user)
    session.commit()

    user = session.scalar(select(User).where(User.username == 'user'))

    assert user.username == 'user'
