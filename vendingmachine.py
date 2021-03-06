#実習課題2
#自動販売機

# coding:utf-8

#Flask,テンプレート,リクエスト読み込み
import os
from flask import Flask, render_template, request, redirect, url_for
#ファイル名をチェックする関数
from werkzeug.utils import secure_filename

#DBを使う
import mysql.connector
from mysql.connector import errorcode

#numpyを使う
import numpy as np

#時間の取得
#import datetime

#画像処理
from PIL import Image

#自分をappという名称でインスタンス化
app = Flask(__name__, static_folder='drink_image')

#データベースの情報
host = 'localhost' # データベースのホスト名又はIPアドレス
username = 'root'  # MySQLのユーザ名
passwd   = 'Hito05hito'    # MySQLのパスワード
dbname   = 'my_database'    # データベース名

#アップロード画像の保存場所
UPLOAD_FOLDER = './drink_image/'
#アップロードされる拡張子の制限
#ALLOWED_EXTENSIONS = set(['png','jpeg','jpg'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

#ファイルの拡張子の確認
#def is_allowed_file(filename):
    # .があるかどうかのチェックと、拡張子の確認
    # OKなら１、だめなら0
#    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

#画像の保存
def save_image(image):
    filename = secure_filename(image.filename)
    image.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
    return filename

#ドリンク情報の取得
def get_drink_info(cursor):
    drink = []
    for (drink_id, sql_image, name, price, stock, status) in cursor:
        item = {"drink_id":drink_id, "image":sql_image, "name":name, "price":price, "stock":stock, "status":status}
        drink.append(item)
    return drink

#DBの操作
def db_connection():
    cnx = mysql.connector.connect(host=host, user=username, password=passwd, database=dbname)
    cursor = cnx.cursor()
    return cnx, cursor

#insert判定
def can_insert(image, name, price, stock):
    if image == "" or name == "" or price == "" or stock == "":
        return False, 1 #"【追加失敗】いずれかの項目が未入力です。全ての項目を入力してください。"
    if stock == "" or np.sign(int(stock)) == -1:
        return False, 2 #"【追加失敗】在庫数は0以上の整数で入力してください。"
    if price == "" or np.sign(int(price)) == -1:
        return False, 3 #"【追加失敗】値段は0以上の整数で入力してください。"
    #if not (filename[-3:] == "png" and filename[-3:] == "jpg" and filename[-4:] == "jpeg"):
    #    return False, 4 #【追加失敗】アップロード画像のファイル形式が違います。
    return True,  5 #"【追加成功】商品が追加されました。"

#update判定
def can_update(stock):
    if stock == "" or np.sign(int(stock)) == -1:
        return False, 6 #"【更新失敗】在庫数は0以上の整数で入力してください。"
    return True, 7 #"【更新成功】在庫数が変更されました。"

#change判定
def can_change(status):
    if status == "":
        return False, 8 #"【更新失敗】公開または非公開を選択してください。"
    return True, 9 #"【更新成功】公開ステータスが変更されました。"

#購入情報の取得
def buy_drink_info(cursor):
    for (drink_id, image, name, price, stock, status) in cursor:
        item = {"drink_id":drink_id, "image":image, "name":name, "price":price, "stock":stock, "status":status}

    #購入商品の値を取得
    buy_image = item["image"]
    buy_name = item["name"]
    buy_price = item["price"]
    buy_stock = item["stock"]

    return buy_image, buy_name, buy_price, buy_stock

#商品選択判定
def can_select(drink_id, payment):
    if drink_id == "" and payment == "":
        return False, 10 #ドリンクを選択してください
    if drink_id == "":
        return False, 11 #ドリンクを選択してください
    return True, ""

#購入判定
def can_payment(payment, buy_price):
    if payment == "":
        return False, 12
    if np.sign(int(payment)) == -1:
        return False, 13
    if int(payment) < buy_price:
        return False, 14
    return True, ""

#管理者画面：初期画面
@app.route('/index', methods=['GET'])
def management_index():
    try:
        cnx, cursor = db_connection()

        query = 'SELECT drink.drink_id, drink.image, drink.name, drink.price, stock.stock, drink.status FROM drink LEFT JOIN stock ON drink.drink_id = stock.drink_id;'
        cursor.execute(query)

        drink = get_drink_info(cursor)

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("ユーザ名かパスワードに問題があります。")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("データベースが存在しません。")
        else:
            print(err)
    else:
        cnx.close()
    return render_template('management.html', drink=drink)

#追加
@app.route('/insert', methods=['POST'])
def management_insert():
    drink_id = request.form.get("drink_id","")
    name = request.form.get("new_name","")
    price = request.form.get("new_price","")
    stock = request.form.get("new_stock","")
    status = request.form.get("new_status","")
    image = request.files.get("new_img","")
    sql_kind = request.form.get("sql_kind","")

    message = ""
    can_insert_drink = ""

    try:
        cnx, cursor = db_connection()
        query = 'SELECT drink.drink_id, drink.image, drink.name, drink.price, stock.stock, drink.status FROM drink LEFT JOIN stock ON drink.drink_id = stock.drink_id;'

        #商品の追加
        if sql_kind == 'insert':
            can_insert_drink, message = can_insert(image, name, price, stock)
            
            if can_insert_drink: #Trueの場合insert
                filename = save_image(image)
                sql_image = './drink_image/' + filename

                add_drink = "INSERT INTO drink (name, image, price, status) VALUES ('{}', '{}', {}, {});".format(name, sql_image, price, status)
                cursor.execute(add_drink)
                drink_id = cursor.lastrowid #insertした値を取得 

                add_stock = "INSERT INTO stock (drink_id, stock) VALUES({}, {});".format(drink_id, stock)
                cursor.execute(add_stock)
                cnx.commit()
            
            else:
                return render_template("management_result.html",message=message)
                #return redirect('index')

        cursor.execute(query)

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("ユーザ名かパスワードに問題があります。")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("データベースが存在しません。")
        else:
            print(err)
    else:
        cnx.close()

    return render_template("management_result.html",message=message)
    
#在庫数の変更
@app.route('/update', methods=['POST'])
def management_update():
    drink_id = request.form.get("drink_id","")
    sql_kind = request.form.get("sql_kind","")
    message = ""
    can_update_stock = ""

    try:
        cnx, cursor = db_connection()
        query = 'SELECT drink.drink_id, drink.image, drink.name, drink.price, stock.stock, drink.status FROM drink LEFT JOIN stock ON drink.drink_id = stock.drink_id;'

        if sql_kind == 'update':
            stock = request.form.get("update_stock","")
            can_update_stock, message = can_update(stock)

            if can_update_stock: #Trueの場合update
                update_stock = "UPDATE stock SET stock = {} WHERE drink_id = {}".format(stock, drink_id)
                cursor.execute(update_stock)
                cnx.commit()
            else:
                return render_template("management_result.html",message=message)
                #return redirect('index')

        cursor.execute(query)

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("ユーザ名かパスワードに問題があります。")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("データベースが存在しません。")
        else:
            print(err)

    else:
        cnx.close()

    return render_template("management_result.html",message=message)
    #return redirect('index')

#ステータス変更
@app.route('/change', methods=['POST'])
def management_change():
    drink_id = request.form.get("drink_id","")
    status = request.form.get("new_status","")
    message = ""
    sql_kind = request.form.get("sql_kind","")
    can_change_status = ""

    try:
        cnx, cursor = db_connection()
        query = 'SELECT drink.drink_id, drink.image, drink.name, drink.price, stock.stock, drink.status FROM drink LEFT JOIN stock ON drink.drink_id = stock.drink_id;'

        if sql_kind == 'change':
            status = request.form.get("change_status","")
            can_change_status, message = can_change(status)
            
            if can_change_status: #Trueの場合change
                change_status = "UPDATE drink SET status = {} WHERE drink_id = {}".format(status, drink_id)
                cursor.execute(change_status)
                cnx.commit()
            else:
                return render_template("management_result.html",message=message)
                #return redirect('index')

        cursor.execute(query)

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("ユーザ名かパスワードに問題があります。")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("データベースが存在しません。")
        else:
            print(err)

    else:
        cnx.close()

    return render_template("management_result.html",message=message)
    #return redirect('index')

#購入画面
@app.route('/purchase', methods=['GET'])
def purchase():

    try:
        cnx, cursor = db_connection()

        query = 'SELECT drink.drink_id, drink.image, drink.name, drink.price, stock.stock, drink.status FROM drink LEFT JOIN stock ON drink.drink_id = stock.drink_id;'
        cursor.execute(query)

        drink = get_drink_info(cursor)

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("ユーザ名かパスワードに問題があります。")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("データベースが存在しません。")
        else:
            print(err)
    else:
        cnx.close()
    return render_template('purchase.html',drink=drink)

#購入結果画面
@app.route('/result',methods=['POST'])
def result():
    drink_id = request.form.get("drink_id","")
    payment = request.form.get("payment","")

    change = ""
    new_stock = ""
    buy_image = ""
    buy_name = ""
    buy_price = ""
    buy_stock = ""
    message = ""
    can_buy_drink = ""
    can_select_drink = ""

    can_select_drink, message = can_select(drink_id, payment)
    if not can_select_drink:
        return render_template("result.html",message=message)

    try:
        cnx, cursor = db_connection()
        query = 'SELECT drink.drink_id, drink.image, drink.name, drink.price, stock.stock, drink.status FROM drink LEFT JOIN stock ON drink.drink_id = stock.drink_id WHERE drink.drink_id = {}'.format(drink_id)
        cursor.execute(query)

        buy_image, buy_name, buy_price, buy_stock = buy_drink_info(cursor)
        can_buy_drink, message = can_payment(payment, buy_price)

        if can_buy_drink: #Trueの場合
            change = int(payment) - buy_price

            if buy_stock != 0:
                #在庫数を減らす
                new_stock = buy_stock-1
                reduce_stock = "UPDATE stock SET stock = {} WHERE drink_id = {};".format(new_stock, drink_id)
                cursor.execute(reduce_stock)

                #購入日時
                purchase_date = "INSERT INTO purchase(drink_id) VALUES({});".format(drink_id)
                cursor.execute(purchase_date)
                cnx.commit()

        else:
            return render_template("result.html",message=message)

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                    print("ユーザ名かパスワードに問題があります。")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
                    print("データベースが存在しません。")
        else:
            print(err)
    else:
        cnx.close()

    return render_template('result.html',image=buy_image,name=buy_name,change=change,message=message)

'''
#修正後コメント
- redirectでの値の受け渡し
sessionを使えばいい
redirectを使うときにsessionから値を出せばいい

- 関数名は動詞で！

- 関数化（l.123）
①DBに接続
②DBからデータをとる
③表示

def get_drinks_by_db(cursor):
    query = 
    cursor.execute(query)

    return get_drink_info(cursor)

def printError(err):
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("ユーザ名かパスワードに問題があります。")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("データベースが存在しません。")
    else:
        print(err)

def register_drink(cursor, cnx, name...):
    #add_drink =
    #cursor.execute()
    #cn
    dirnk_id = insert_into_drink

    #add_stock
    #cursor.execute
    insert_into_stock =
    cnc.commit()

#indexのところ
def management_index():
    cnx, cursor = 
    drinks = get_drinks_by_db()

#insertのところ
変数
frink_id, name, price get_drink_info_by(request)

#fileimage
sql_imageを返す関数でよくない？

#編集前
#管理者画面（追加・更新）
@app.route('/management',methods=['GET','POST'])
def management():

    #変数の定義
    drink_id = request.form.get("drink_id","")
    name = request.form.get("new_name","")
    price = request.form.get("new_price","")
    stock = request.form.get("new_stock","")
    
    #公開か非公開かのステータス
    status = request.form.get("new_status","")

    #完了メッセージ
    success_message = ""

    #エラーメッセージ
    error_message = ""
    error_message_price = ""
    error_message_stock = ""
    error_message_image = ""

    #画像の取得
    image = request.files.get("new_img","")
    
    #sqlの状態
    #insert:追加、update:在庫数の更新、change:公開・非公開ステータスの変更
    sql_kind = request.form.get("sql_kind","")

    try:
        #DBの読み込み
        cnx = mysql.connector.connect(host=host, user=username, password=passwd, database=dbname)
        cursor = cnx.cursor()

        #常にテーブルは表示
        query = 'SELECT drink.drink_id, drink.image, drink.name, drink.price, stock.stock, drink.status FROM drink LEFT JOIN stock ON drink.drink_id = stock.drink_id;'

        #商品の追加
        if sql_kind == 'insert':

            #いずれかの項目が入力されていない場合
            if image == None or name == "" or price == "" or stock == "":
                cursor.execute(query)
                error_message = "いずれかの項目が未入力です。全ての項目を入力してください。" 

            else:

                #画像の読み込み
                if image and is_allowed_file(image.filename):
                    #危険な文字を削除
                    filename = secure_filename(image.filename)
                    print(filename)
                    #ファイルの保存
                    image.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
                    #パスを含めたものをsqlに格納
                    sql_image = './drink_image/' + filename
    
                else:
                    error_message_image = 'ファイルの形式が違います。「png」「jpeg」形式の画像を選択してください。'

                try:
                    add_drink = "INSERT INTO drink (name, image, price, status) VALUES ('{}', '{}', {}, {})".format(name, sql_image, price, status)
                    cursor.execute(add_drink)
                    drink_id = cursor.lastrowid # insertした値を取得できます。 

                    add_stock = "INSERT INTO stock (drink_id, stock) VALUES({}, {})".format(drink_id, stock)
                    cursor.execute(add_stock)

                    cnx.commit()

                    success_message = "【追加成功】商品が追加されました"

                except mysql.connector.Error as err:
                    print(err)

                    #価格が0以上か確認
                    if re.match('^[0-9]$', price):
                        error_message_price = ""
                    else:
                        error_message_price = "価格は0以上の整数で入力してください。"
    
                    #在庫数が0以上か確認
                    if re.match('^[0-9]$', stock):
                        error_message_stock = ""
                    else:
                        error_message_stock = "在庫数は0以上の整数で入力してください。"
                    
                #必ず実行
                cursor.execute(query)

        #在庫数の更新
        elif sql_kind == 'update':

            stock = request.form.get("update_stock","")

            try:
                update_stock = "UPDATE stock SET stock = {} WHERE drink_id = {}".format(stock, drink_id)
                #drink_id = cursor.lastrowid # insertした値を取得できます。 

                #add_stock = "INSERT INTO stock (drink_id, stock) VALUES({}, {})".format(drink_id, stock)
                #cursor.execute(add_drink)
                cursor.execute(update_stock)
                cnx.commit()

                success_message = "【更新成功】在庫数が変更されました。"

            except mysql.connector.Error as err:
                print(err)
    
                error_message_stock = "在庫数は0以上の整数で入力してください。"
                    
            #必ず実行
            cursor.execute(query)

        #公開・非公開ステータスの変更
        elif sql_kind == 'change':

            #変更後の公開ステータス
            status = request.form.get("change_status","")
            
            try:
                #公開→非公開へ
                #if status == 1:
                change_status = "UPDATE drink SET status = {} WHERE drink_id = {}".format(status, drink_id)

                #非公開・公開へ
                #else:
                #    change_status = "UPDATE drink SET status = {} WHERE drink_id = {}".format(status, drink_id)

                cursor.execute(change_status)
                cnx.commit()

                success_message = "【更新成功】公開ステータスが変更されました。"

            except mysql.connector.Error as err:
                print(err)
                    
            #必ず実行
            cursor.execute(query)

        else:
            #必ず実行
            cursor.execute(query)

        drink = []
        for (drink_id, sql_image, name, price, stock, status) in cursor:
            item = {"drink_id":drink_id, "image":sql_image, "name":name, "price":price, "stock":stock, "status":status}
            drink.append(item)

        params = {
            "drink" : drink,
            "success_message" : success_message,
            "error_message": error_message,
            "error_message_image":error_message_image,
            "error_message_price":error_message_price,
            "error_message_stock":error_message_stock
        }

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("ユーザ名かパスワードに問題があります。")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("データベースが存在しません。")
        else:
            print(err)

    else:
        cnx.close()
    return render_template('management.html', **params)

#購入結果画面
@app.route('/result',methods=['POST'])
def result():
    #購入ドリンクの情報
    drink_id = request.form.get("drink_id","")
    #支払い金額
    payment = request.form.get("payment","")
    
    #お釣り
    change = ""

    #新しい在庫数
    new_stock = ""

    #購入商品の情報
    buy_image = ""
    buy_name = ""
    buy_price = ""
    buy_stock = ""

    #エラーメッセージ
    error_message_drink = ""
    error_message_price = ""

    #商品のエラーメッセージ
    if drink_id == "" and payment == "":
        error_message_drink = "商品を選択してください。"

    elif drink_id == "":
        error_message_drink = "商品を選択してください。"

    else:
        error_message_drink = ""

    try:
        #DBに接続
        #cnx = mysql.connector.connect(host=host, user=username, password=passwd, database=dbname)
        #cursor = cnx.cursor()
        cnx, cursor = db_connection()

        query = 'SELECT drink.drink_id, drink.image, drink.name, drink.price, stock.stock, drink.status FROM drink LEFT JOIN stock ON drink.drink_id = stock.drink_id WHERE drink.drink_id = {};'.format(drink_id)
        cursor.execute(query)

        for (drink_id, image, name, price, stock, status) in cursor:
            item = {"drink_id":drink_id, "image":image, "name":name, "price":price, "stock":stock, "status":status}

        #購入商品の値を取得
        buy_image = item["image"]
        buy_name = item["name"]
        buy_price = item["price"]
        buy_stock = item["stock"]

        #お金のエラーメッセージ
        if payment == "":
            error_message_price = "お金を投入してください。"

        elif int(payment) < buy_price:
                error_message_price = "投入金額が足りません。"
    
        else:
            change = int(payment) - buy_price
            error_message_price = ""
        
            if buy_stock != 0:
                #在庫数を減らす
                new_stock = buy_stock-1
                #print(new_stock)

                reduce_stock = "UPDATE stock SET stock = {} WHERE drink_id = {};".format(new_stock, drink_id)
                cursor.execute(reduce_stock)

                #指定ドリンクと購入日時を記録
                purchase_date = "INSERT INTO purchase(drink_id) VALUES({});".format(drink_id)
                cursor.execute(purchase_date)

                cnx.commit()

        #params={
        #    "image":buy_image,
        #    "name":buy_name,
        #    "change":change,
        #    "error_message_drink":error_message_drink,
        #    "error_message_price":error_message_price
        #}

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                    print("ユーザ名かパスワードに問題があります。")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
                    print("データベースが存在しません。")
        else:
            print(err)
    else:
        cnx.close()

    return render_template('result.html',image=buy_image,name=buy_name,change=change,error_message_drink=error_message_drink,error_message_price=error_message_price)
    #return render_template('result.html', **params)


'''