
from  flask import Blueprint  #使用blueprint ，來定義 應嫆程式的藍圖，使各個檔案分開不會因而相互干擾
from flask import render_template,redirect,request,url_for
from flask import flash    #  此 module 是 flask中有 閃爍彈出一些資訊(提醒)的功能


# 引入制定好的資料格式 User，來使註冊者新增帳戶 
from . import db
from .models import User
# 引入下方模組,使註冊者密碼用以外包亂碼方式，要求字串傳值給後端，能夠更加保障安全
from werkzeug.security import generate_password_hash,check_password_hash
# 處理網站登入，確保使用者是真的有登入而不是透過網站輸入網址進入
from flask_login import login_user,login_required,logout_user,current_user
# 設定名為 auth 的藍圖
auth=Blueprint("auth",__name__)

#處理註冊路由
@auth.route("/sign-up",methods=["GET","POST"])
def sign_up():
    # 取得經由http協定 連線方式為POST ，註冊者所輸入資訊。
    if request.method=="POST":
        # 後端接，前端user所輸入的資訊
        name=request.form.get("name")
        email=request.form.get("email")
        password1=request.form.get("password1")
        password2=request.form.get("password2")
        # 在資料庫查詢，是否此資料內容已存在資料庫
        user=User.query.filter_by(email=email).first()
        if user:
            flash("此信箱已被註冊過 !!", category="error")
        # 註冊者是不是有沒有輸入正確的格式，來判斷是否要給註冊者新增帳戶
        elif len(email)<4:
            flash("您輸入信箱格式長度不正確(不得輸入小於4個字元)",category="error")
        elif len(name)<2:
            flash("您輸入名字格式長度不正確(不得輸入小於2個字元)",category="error")
        elif len(password1)<5:
            flash("您輸入註冊密碼長度不夠(密碼長度須超過5個字元)",category="error")            
        elif password1!=password2:
            flash("請再次確認您輸入的註冊密碼，是否一致!!",category="error")
        else:
            # 新增使用者資訊                                                                 #sha256 是一種亂序算法
            new_user=User(name=name ,email=email,password=generate_password_hash(password1,method="sha256"))
            # 新增註冊者資訊，提交至創建好的資料庫
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user,remember=True)
            # 可以把註冊者輸入資訊加入至database
            flash("註冊成功",category="success")
            # 小提醒: flask 中的 url_for 模組 可以找出 blueprint所裝飾的function的 路由
            return redirect(url_for("views.home"))

    return render_template("sign_up.html",user=current_user)

#處理登入路由
@auth.route("/login",methods=["GET","POST"])
def login():
    if request.method =="POST":
        email=request.form.get("email")
        password=request.form.get("password")
        # 查詢sqllite資料庫裡有沒有資料，來決定使用者能否成功登入
        user=User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password,password):
                flash(" 已成功登入 !!!", category="success")
                login_user(user, remember=True)
                return redirect(url_for("views.home"))
            else:
                flash("帳號或密碼輸入不正確，請再次輸入",category="error")
        else:
            flash("此帳戶不存在!!",category="error")
    return render_template("login.html",user=current_user)

#處理登出路由
@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))
