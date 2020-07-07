# 実習課題2：自動販売機
## 概要
自動販売機のプログラムです。  
商品の管理や、商品の購入を行うことができます。

### 管理画面でできること
[管理画面](http://localhost:5000/index)
- 商品情報の確認
- 商品の追加
- 在庫数の変更
- 購入者画面に表示するか否かの選択

### 購入画面でできること
[購入画面](http://localhost:5000/purchase)
- 商品の購入
- お金の投入

## 実行ファイル：vendingmachine.py
### 自動販売機の基本的な処理は、vendingmachine.pyで行われています。
- 管理者画面の処理：management_index(),management_insert(), management_update(), management_change()
- 購入画面の処理：purchase()  
- 購入結果画面の処理：result()  

## 自動販売機のHTMLファイル
### 全てtemplatesフォルダに格納されています
- management.html  
管理ページのHTMLです。
- management_result.html  
管理画面の更新結果を表示するHTMLです。
- purchase.html  
購入ページのHTMLです。
- result.html  
購入結果ページのHTMLです。

## 自動販売機のテーブル
- drink_table.sql  
ドリンク情報を格納するテーブルです。
- stock_table.sql  
在庫数情報を格納するテーブルです。
- purchase_table.sql  
購入情報を格納するテーブルです。

## 実行方法
ターミナルで以下のコマンドを入力してください。

```
export FLASK_APP=vendingmachine  
export FLASK_ENV=development  
flask run  
```

実行後、**管理画面** または **購入画面** を開いてください。

## 質問したいこと
- redirectを使用する際の値の受け渡し
- まだ関数が長いところがあるが、更に関数を分けることはできるのか
- mysql.connector.Errorは省略できるのか