# 実習課題2：自動販売機
## 概要
自動販売機のプログラムです。
商品の管理や、商品の購入を行うことができます。

### 管理画面でできること
①商品の追加
②在庫数の変更
③購入者画面に表示するか否かの選択

### 購入画面でできること
①商品の購入

## vendingmachine.py
### 自動販売機の基本的な処理はvendingmachine.pyで行われています。
- /management
管理者画面
- /purchase
購入画面
- /result
購入結果画面

## 自動販売機のHTMLファイル
### templatesフォルダに格納されています
- management.html
管理者画面のHTML
- purchase.html
購入画面のHTML
- result.html
購入結果のHTML

## 自動販売機のテーブル
- drink_table.sql
- stock_table.sql
- purchase_table.sql