#実習課題2
#自動販売機

# coding:utf-8

#Flask,テンプレート,リクエスト読み込み
import os
from flask import Flask, render_template, request, url_for
#ファイル名をチェックする関数
from werkzeug.utils import secure_filename

#DBを使う
import mysql.connector
from mysql.connector import errorcode

#時間の取得
#import datetime

#画像処理
from PIL import Image

#match関数の利用
#入力した数字がマッチしているかチェック
import re

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
ALLOWED_EXTENSIONS = set(['png','jpeg'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

#ファイルの拡張子の確認
def allwed_file(filename):
    # .があるかどうかのチェックと、拡張子の確認
    # OKなら１、だめなら0
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

'''
#管理者画面（ホーム画面）
@app.route('/management', methods=['GET'])
def management_home():

    try:
        cnx = mysql.connector.connect(host=host, user=username, password=passwd, database=dbname)
        cursor = cnx.cursor()

        query = 'SELECT drink.drink_id, drink.image, drink.name, drink.price, stock.stock, drink.status FROM drink LEFT JOIN stock ON drink.drink_id = stock.drink_id;'
        cursor.execute(query)

        drink = []
        for (drink_id, image, name, price, stock, status) in cursor:
            item = {"drink_id":drink_id, "image":image, "name":name, "price":price, "stock":stock, "status":status}
            drink.append(item)

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
'''
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
    #アップロードされていない場合はNone
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
                if image and allwed_file(image.filename):
                    #危険な文字を削除
                    filename = secure_filename(image.filename)
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
    
                #在庫数が0以上か確認
                #if re.match('^[0-9]$', stock):
                #    error_message_stock = ""
                #else:
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

#購入画面
@app.route('/purchase', methods=['GET'])
def purchase():

    #変数の定義
    drink_id = request.form.get("drink_id","")
    name = request.form.get("new_name","")
    price = request.form.get("new_price","")
    stock = request.form.get("new_stock","")

    #支払い金額
    money = request.form.get("money","")



    try:
        cnx = mysql.connector.connect(host=host, user=username, password=passwd, database=dbname)
        cursor = cnx.cursor()

        query = 'SELECT drink.drink_id, drink.image, drink.name, drink.price, stock.stock, drink.status FROM drink LEFT JOIN stock ON drink.drink_id = stock.drink_id;'
        cursor.execute(query)

        drink = []
        for (drink_id, image, name, price, stock, status) in cursor:
            item = {"drink_id":drink_id, "image":image, "name":name, "price":price, "stock":stock, "status":status}
            drink.append(item)

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
    return render_template('result.html')