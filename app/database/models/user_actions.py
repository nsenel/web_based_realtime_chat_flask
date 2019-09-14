from app import app, db
from sqlalchemy import ForeignKey, DateTime
from sqlalchemy.orm import relationship
import datetime
from app.database.models_schema.user_schema import UserSchema
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

    def __init__(self, user_id, login=True):
        self.user_id = user_id
        self.login = login
        self.login_time = datetime.datetime.utcnow()

class UserActionInterface:
    def __init__(self, user_id):
        self.user = User.query.filter_by(user_id=user_id).first()

    def get_user_info(self):
        return UserSchema().dump(self.user, many=False)

    def save_new_login(self):
        user_action = UserAction(self.user.user_id)
        db.session.add(user_action)
        db.session.commit()
    
    def log_out_user(self):
        UserAction.query.filter_by(user_id=self.user.user_id).update({'login': False,'logout_time': datetime.datetime.utcnow()})
        db.session.commit()
