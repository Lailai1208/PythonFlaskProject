
# 這頁開發使用者會用到的東西

from  flask import Blueprint, jsonify  #使用blueprint ，來定義 應用程式的藍圖，使各個檔案分開不會因而相互干擾
from flask import render_template,flash,request
from flask_login import login_required,current_user
from .models import Note #引入資料庫中 Note類別
from . import db
import json
views=Blueprint("views",__name__)

@views.route("/",methods=["GET","POST"])
@login_required
def home():
    if request.method=="POST":
        # 獲取notes 所輸入的筆記內容
        note=request.form.get("note")
        if len(note)<1:
            flash("輸入太少字元，請重新輸入大於一個字元",category="error")
        else:
            new_note=Note(data=note,user_id=current_user.id)
            # 將使用者在 Notes 輸入的資訊，寫進資料庫
            db.session.add(new_note)
            db.session.commit()
            flash("已成功添加",category="success")
    return render_template("home.html",user=current_user)


@views.route("/delete-note",methods=["POST"])
def delete_note():
    note= json.loads(request.data)
    noteId= note["noteId"]
    note=Note.query.get(noteId)
    if note:
        if note.user_id ==current_user.id:
            db.session.delete(note)
            db.session.commit()


    return jsonify({})

