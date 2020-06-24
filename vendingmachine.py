#実習課題2
#自動販売機

# coding:utf-8

#Flask,テンプレート,リクエスト読み込み
from flask import Flask, render_template, request

import mysql.connector
from mysql.connector import errorcode

#時間の取得
import datetime
#更新日時の取得
#import os

#画像処理
import io
from PIL import Image

#自分をappという名称でインスタンス化
app = Flask(__name__)

 #データベースの情報
host = 'localhost' # データベースのホスト名又はIPアドレス
username = 'root'  # MySQLのユーザ名
passwd   = 'Hito05hito'    # MySQLのパスワード
dbname   = 'my_database'    # データベース名

#商品管理ページ（初期画面、常にテーブルが表示されるように）
@app.route('/management')
def management_send():

    #日時の取得
    date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    drink = []
    try:
        cnx = mysql.connector.connect(host=host, user=username, password=passwd, database=dbname)
        cursor = cnx.cursor()
        query = 'SELECT drink.image, drink.name, drink.price, stock.stock, drink.status FROM drink LEFT JOIN stock ON drink.drink_id = stock.drink_id;'
        cursor.execute(query)

        for (id, image_binary, name, price, stock, status, date) in cursor:
            item = {"drink_id":id, "image":image_binary, "name":name, "price":price, "stock":stock, "status":status, "date":date}
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

#商品管理ページ（追加・更新など、変更後の画面）
@app.route('/management',methods=['POST'])
def management_recieve():

    #初期値
    id = request.form.get("drink_id","")
    name = request.form.get("new_name","")
    price = request.form.get("new_price","")
    stock = request.form.get("new_stock","")
    status = request.form.get("new_status","")

    #画像読み込み
    image = request.form.get("new_img","")

    #sqlの状態
    #insert:追加、update:在庫の更新、change:公開・非公開の変更
    #sql_kind = request.form.get("sql_kind","")

    #imageをバイナリデータに変換
    image_in = Image.open('image/' + image) #画像があるフォルダのパス
    image_bin = io.BytesIO(image_in)
    image_binary = image_bin.getvalue()

    #日時の取得
    date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    #入力の判定（エラー文を表示する）
    result = ""

    cnx = None

    try:
        cnx = mysql.connector.connect(host=host, user=username, password=passwd, database=dbname)
        cursor = cnx.cursor()

        #常にテーブルは表示
        query = 'SELECT drink.image, drink.name, drink.price, stock.stock, drink.status FROM drink LEFT JOIN stock ON drink.drink_id = stock.drink_id;'

        if image == "" or name == "" or price == "" or stock == "" or status == "":
            cursor.execute(query)
            result = "全ての項目を入力してください。"  
        
        else:
            #テーブルに追加する
            try:
                sql_drink = "INSERT INTO drink (drink_id, name, image, price, created_date, update_date, status) VALUES({}, '{}', {}, {},'{}','{}',{})".format(id, name, image_binary, price, date, date, status)
                cursor.execute(sql_drink)
                cnx.commit()
                #order_id = cursor.lastrowid # insertした値を取得できます。
                
                sql_stock = "INSERT INTO stock (drink_id, stock, created_date, update_date) VALUES({}, {}, '{}', '{}')".format(id, stock, date, date)
                cursor.execute(sql_stock)
                cnx.commit()

            except mysql.connector.Error as err:
                print(err)
                result = "「JPEG」または「PNG」形式の画像をアップロードしてください。"

            cursor.execute(query)

            #sql_kind == 'insert':

        drink = []
        for (id, image_binary, name, price, stock, status, date) in cursor:
            item = {"drink_id":id, "img":image_binary, "name":name, "price":price, "stock":stock, "status":status, "date":date}
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
    return render_template('management.html', drink=drink, result=result)

#購入画面
#@app.route('/purchase',methods=['GET','POST'])
#def purchase():
#    return render_template('purchase.html')

#購入結果画面
#@app.route('/result',methods=['POST'])
#def result():
#    return render_template('result.html')