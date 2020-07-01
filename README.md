# 実習課題2：自動販売機
## 概要
自動販売機のプログラムです。<br>
商品の管理や、商品の購入を行うことができます。

### 管理画面でできること
- 商品情報の確認
- 商品の追加
- 在庫数の変更
- 購入者画面に表示するか否かの選択

### 購入画面でできること
- 商品の購入
- お金の投入

## vendingmachine.py
### 自動販売機の基本的な処理は、vendingmachine.pyで行われています。
- 管理者画面の処理：management()<br>
URL：/management
- 購入画面の処理：purchase()<br>
URL：/purchase
- 購入結果画面の処理：result()<br>
URL：/result

## 自動販売機のHTMLファイル
### 全てtemplatesフォルダに格納されています
- management.html<br>
管理ページのHTMLです。
- purchase.html<br>
購入ページのHTMLです。
- result.html<br>
購入結果ページのHTMLです。

## 自動販売機のテーブル
- drink_table.sql<br>
ドリンク情報を格納するテーブルです。
- stock_table.sql<br>
在庫数情報を格納するテーブルです。
- purchase_table.sql<br>
購入情報を格納するテーブルです。