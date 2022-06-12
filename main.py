#把她想像成最終的啟動的關鍵
from website import create_app

app=create_app()

if __name__ =="__main__" :    # if __name__ =="__main__" : 此行表示當我們運行這個檔案，並不是import進來的檔案    ("__main__"表示未知的描述檔)   
    app.run(debug=True)     # debuger=True  當有任何更動會自動重啟伺服器