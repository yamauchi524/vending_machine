# 実習課題2：自動販売機
## 概要
自動販売機のプログラムです。<br>
商品の管理や、商品の購入を行うことができます。

### 管理画面でできること
- 商品の追加
- 在庫数の変更
- 購入者画面に表示するか否かの選択

### 購入画面でできること
- 商品の購入

## vendingmachine.py
### 自動販売機の基本的な処理はvendingmachine.pyで行われています。
- /management<br>
管理者画面
- /purchase<br>
購入画面
- /result<br>
購入結果画面

## 自動販売機のHTMLファイル
### templatesフォルダに格納されています
- management.html<br>
管理者画面のHTML
- purchase.html<br>
購入画面のHTML
- result.html<br>
購入結果のHTML

## 自動販売機のテーブル
- drink_table.sql
- stock_table.sql
- purchase_table.sql