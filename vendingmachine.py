#実習課題2
#自動販売機

# coding:utf-8

#Flask,テンプレート,リクエスト読み込み
import os
from flask import Flask, render_template, request, redirect, url_for
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
app = Flask(__name__)

#データベースの情報
host = 'localhost' # データベースのホスト名又はIPアドレス
username = 'root'  # MySQLのユーザ名
passwd   = 'Hito05hito'    # MySQLのパスワード
dbname   = 'my_database'    # データベース名

#アップロード画像の保存場所
#UPLOAD_FOLDER = '/Users/hyamauchi/Desktop/codecamp_work/vendingmachine/drink_image'
UPLOAD_FOLDER = './drink_image/'
ALLOWED_EXTENSIONS = set(['png','jpeg'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

#def allowed_file(filename):
#    return '.' in filename and \
#        filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

#管理者画面（ホーム画面）
@app.route('/management', methods=['GET'])
def management():

    try:
        cnx = mysql.connector.connect(host=host, user=username, password=passwd, database=dbname)
        cursor = cnx.cursor()

        query = 'SELECT drink.image, drink.name, drink.price, stock.stock, drink.status FROM drink LEFT JOIN stock ON drink.drink_id = stock.drink_id;'
        cursor.execute(query)

        drink = []
        for (image, name, price, stock, status) in cursor:
            item = {"image":image, "name":name, "price":price, "stock":stock, "status":status}
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


#管理者画面（追加・更新）
@app.route('/management',methods=['POST'])
def management_recieve():

    #変数の定義
    drink_id = request.form.get("drink_id","")
    name = request.form.get("new_name","")
    price = request.form.get("new_price","")
    stock = request.form.get("new_stock","")
    status = request.form.get("new_status","")

    #画像の取得
    #アップロードされていない場合はNone
    image = request.files["new_img"]
    #画像の保存
    filename = secure_filename(image.filename)
    image.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
    
    #公開・非公開ステータス
    #status_public = 1
    #status_private = 0

    #完了メッセージ
    success_message = ""

    #エラーメッセージ
    error_message = ""
    error_message_price = ""
    error_message_stock = ""
    error_message_image = ""

    #sqlの状態
    #insert:追加、update:在庫の更新、change:公開・非公開の変更
    sql_kind = request.form.get("sql_kind","")

    try:
        cnx = mysql.connector.connect(host=host, user=username, password=passwd, database=dbname)
        cursor = cnx.cursor()

        #常にテーブルは表示
        query = 'SELECT drink.image, drink.name, drink.price, stock.stock, drink.status FROM drink LEFT JOIN stock ON drink.drink_id = stock.drink_id;'

        if image == None or name == "" or price == "" or stock == "" or status == "":
            cursor.execute(query)
            error_message = "いずれかの項目が未入力です。全ての項目を入力してください。" 
        
        else:
            #sql_kindがinsertの時
            #sql_kindがupdateの時
            #sql_kindがchangeの時
            # if文
            # priceの話
            # stockの話
            if sql_kind == 'insert':

                try:
                    add_drink = "INSERT INTO drink (name, image, price, status) VALUES('{}', '{}', {}, {})".format(name, image, price, status)
                    #drink_id = cursor.lastrowid # insertした値を取得できます。 
                    add_stock = "INSERT INTO stock (drink_id, stock) VALUES({}, {})".format(drink_id, stock)
                    cursor.execute(add_drink)
                    cursor.execute(add_stock)
                    cnx.commit()
                    success_message = "【追加成功】商品が正しく追加されました"

                except mysql.connector.Error as err:
                    print(err)

                    error_message_image = '許可されていないファイル形式です。'

                    #価格が0以上か確認
                    if re.match('^[0-9]$', price):
                        error_message_price = ""
                    else:
                        error_message_price = "価格は0以上の整数で入力してください。"
    
                    #在庫数が0以上か確認
                    if re.match('^[0-9]$', price):
                        error_message_stock = ""
                    else:
                        error_message_stock = "在庫数は0以上の整数で入力してください。"
                    
                #必ず実行
                cursor.execute(query)
            
            elif sql_kind == 'update':
                try:
                    add_drink = "INSERT INTO drink (name, image, price, status) VALUES('{}', '{}', {}, {})".format(name, image, price, status)
                    #drink_id = cursor.lastrowid # insertした値を取得できます。 
                    add_stock = "INSERT INTO stock (drink_id, stock) VALUES({}, {})".format(drink_id, stock)
                    cursor.execute(add_drink)
                    cursor.execute(add_stock)
                    cnx.commit()
                    success_message = "【追加成功】商品が正しく追加されました"

                except mysql.connector.Error as err:
                    print(err)

                    error_message_image = '許可されていないファイル形式です。'

                    #価格が0以上か確認
                    if re.match('^[0-9]$', price):
                        error_message_price = ""
                    else:
                        error_message_price = "価格は0以上の整数で入力してください。"
    
                    #在庫数が0以上か確認
                    if re.match('^[0-9]$', price):
                        error_message_stock = ""
                    else:
                        error_message_stock = "在庫数は0以上の整数で入力してください。"
            else:    
                #必ず実行
                cursor.execute(query)

            #必ず実行
            cursor.execute(query)

        drink = []
        for (image, name, price, stock, status) in cursor:
            item = {"image":image, "name":name, "price":price, "stock":stock, "status":status}
            drink.append(item)

        params = {
            "drink" : drink,
            "success_message" : success_message

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
#@app.route('/purchase',methods=['GET','POST'])
#def purchase():
#    return render_template('purchase.html')

#購入結果画面
#@app.route('/result',methods=['POST'])
#def result():
#    return render_template('result.html')