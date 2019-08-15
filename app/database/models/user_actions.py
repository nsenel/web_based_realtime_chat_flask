from app import app, db
from sqlalchemy import ForeignKey, DateTime
from sqlalchemy.orm import relationship
import datetime
from app.database.models.user import User
import datetime


class UserAction(db.Model):
    """ UserAction Model for storing user actions details """
    __tablename__ = "UserAction"

    action_id   = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    user_id     = db.Column(db.BigInteger, ForeignKey("UserAccount.user_id"), nullable=False)
    login       = db.Column(db.Boolean,    nullable=True)
    login_time  = db.Column(db.TIMESTAMP,   nullable=True)
    logout_time = db.Column(db.TIMESTAMP,  nullable=True)

    user_relation = relationship(User, primaryjoin=user_id == User.user_id)
# To do numan remove
    def __init__(self, user_id, login=True):
        self.user_id = user_id
        self.login = login
        self.login_time = datetime.datetime.utcnow()

class UserActionInterface:
    def __init__(self):
        pass
    
    def saveNewLogin(self, user_id):
        user_action = UserAction(user_id)
        db.session.add(user_action)
        db.session.flush()
        db.session.commit()
        return user_action.action_id
    
    def logOutUser(self, action_id):
        user_action = UserAction.query.filter_by(action_id=action_id).first()
        user_action.logout_time = datetime.datetime.utcnow()
        user_action.login = False
        db.session.merge(user_action)
        db.session.commit()
