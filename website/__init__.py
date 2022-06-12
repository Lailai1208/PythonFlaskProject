# 快速創建一個application
# 所有製作 blueprint 藍圖 都要放置在這
from  flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
# 用來管理使用者登入介面
from flask_login import LoginManager

# 創建連線flask_sqlalchemy
db= SQLAlchemy()
DB_NAME="database.db"


def create_app():
    # 創建flask 網路伺服器
    app=Flask(__name__)
    app.config["SECRET_KEY"]="AJSISCXNSICXCID"   # 安裝"SECRET_KEY" 用來保護 SESSION、COOKIES 進行加密，切記此密碼不能讓他人知道
    
    # 安裝 SQLlite
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    # 告訴application 要和sqllite資料庫一起使用
    db.init_app(app) 

    # 從 views.py匯入 views這個變數  !!!!!切記 from "."views
    from .views import views

    # 從 auth.py匯入 auth這個變數
    from .auth import auth

    # 將各個所製作的blueprint的產物放入 flask的應用程式之中
    app.register_blueprint(views,url_prefix="/")  #告訴此藍圖 在前面修飾url是甚麼 "/"
    app.register_blueprint(auth,url_prefix="/")

    # 使用 SQLalchemy 模組創建資料庫
    from .models import User,Note
    create_database(app)

    login_manager=LoginManager()
    login_manager.login_view="auth.login"  # 目的讓沒有登入使用者，會引導去一個指定的頁面
    # ' 此功能將login_manger的功能傳遞給我們創建的應用程序
    login_manager.init_app(app)
    @login_manager.user_loader
    def load_user(id):    
        return User.query.get(int(id))
    return app


def create_database(app):
    if not path.exists("website/"+ DB_NAME):
        db.create_all(app=app)
        print("創建資料庫成功")