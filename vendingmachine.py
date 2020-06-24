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

#画像ファイルのpathを指定
UPLOAD_FOLDER = '/Users/hyamauchi/Desktop/codecamp_work/vendingmachine/drink_image/'
ALLOWED_EXTENSIONS = {'png','jpeg'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

#商品管理ページ（初期画面）
@app.route('/management', methods=['GET'])
def management():

    drink = []
    try:
        cnx = mysql.connector.connect(host=host, user=username, password=passwd, database=dbname)
        cursor = cnx.cursor()
        query = 'SELECT drink.image, drink.name, drink.price, stock.stock, drink.status FROM drink LEFT JOIN stock ON drink.drink_id = stock.drink_id;'
        cursor.execute(query)

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

#商品管理ページ（追加・更新など、変更後）
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
    image = request.files.get("new_img","")

    # secure_filenameを使ってLinuxでも保存可能なファイル名に変換
    filename = secure_filename(image.filename)
    image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    #sqlの状態
    #insert:追加、update:在庫の更新、change:公開・非公開の変更
    sql_kind = request.form.get("sql_kind","")

    #完了メッセージ
    #success_message = ""

    #エラーメッセージ
    error_message = ""
    #error_message_price = ""
    #error_message_stock = ""
    #error_message_image = ""

    try:
        cnx = mysql.connector.connect(host=host, user=username, password=passwd, database=dbname)
        cursor = cnx.cursor()

        #常にテーブルは表示
        query = 'SELECT drink.image, drink.name, drink.price, stock.stock, drink.status FROM drink LEFT JOIN stock ON drink.drink_id = stock.drink_id;'

        if image == None or name == "" or price == "" or stock == "" or status == "":
            cursor.execute(query)
            error_message = "全ての項目を入力してください。" 
        
        else:
            #sql_kindがinsertの時
            #sql_kindがupdateの時
            #sql_kindがの時
            # if文
            # priceの話
            # stockの話
            # file読み込み
            try:
                sql_drink = "INSERT INTO drink (name, image, price, status) VALUES('{}', '{}', {}, {})".format(name, image, price, status)
                cursor.execute(sql_drink)
                drink_id = cursor.lastrowid # insertした値を取得できます。
                
                sql_stock = "INSERT INTO stock (drink_id, stock) VALUES({}, {})".format(drink_id, stock)
                cursor.execute(sql_stock)
                cnx.commit()

            except mysql.connector.Error as err:
                print(err)

            cursor.execute(query)

            #sql_kind == 'insert':

        drink = []
        for (image, name, price, stock, status) in cursor:
            item = {"image":image, "name":name, "price":price, "stock":stock, "status":status}
            drink.append(item)

        params = {
            "drink" : drink
            #message

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