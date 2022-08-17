from dao.model.user import User
from sqlalchemy.orm import scoped_session


class UserDAO:
    def __init__(self, db_session: scoped_session):
        self.db_session = db_session

    def get_one(self, uid):
        return self.db_session.query(User).get(uid)

    def get_all_by_query(self, **kwargs):
        stmt = self.db_session.query(User)
        if kwargs:
            filters = {getattr(User, field): value for field, value in kwargs.items()}
            stmt.filter_by(**filters)
        return stmt.all()

    def create(self, **kwargs):
        new = User(**kwargs)
        self.db_session.add(new)
        self.db_session.commit()
        return new

    def delete(self, uid):
        user = self.get_one(uid)
        self.db_session.delete(user)
        self.db_session.commit()

    def update(self, **kwargs):
        user = self.get_one(kwargs.get("id"))
        for keyword in kwargs.keys():
            if kwargs[keyword]:
                setattr(user, keyword, kwargs[keyword])

        self.db_session.add(user)
        self.db_session.commit()
