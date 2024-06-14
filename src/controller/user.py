from src.db.config import db
from src.models.user import User as UserModel
from sqlalchemy.sql import text

class User():

    def __init__(self):
        pass

    def save(self, model):
        x = text('select 1+1 total')
        rs = db.session.execute(x)
        for row in rs:
            print (row[0])
        db.session.add(model)
        db.session.commit()
        UserModel.query.filter_by(role='admin').update()
    
    def list(self):
        rs = UserModel.query.order_by(UserModel.id).all()
        return rs

