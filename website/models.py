# 創建資料庫模型裡的table地方
from . import db
# 載入 flask 當中登入模組
from flask_login import UserMixin
from sqlalchemy.sql import func
# 創建資料庫筆記
class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

# 創建資料庫裡的 User Table
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    name = db.Column(db.String(150))
    notes = db.relationship('Note')
