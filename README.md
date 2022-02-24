# WebScraper
This is Web-Scrapeing Tool for Japan EC site.<br>
これは日本の販売サイト向けのスクレイピングツールです。<br>

## 前提
- python3実行環境
- インターネット接続環境
- LINE Developerの登録とアクセス鍵の取得
- Google Cloud Platformの登録とアクセス鍵の取得
- Googleスプレッドシートへのアクセス許可およびワークブックキーの取得

## インストール方法
プログラム実行に必要なモジュールをインストールします。<br>
```
cd WebScraper
pip3 install -y -r requirements.txt
```

## 使い方
### 検索ワードの一覧を入力
以下のようにGoogleスプレッドシートの検索ワード用シートに検索したい商品のキーワードと条件を記入します。<br>
![input_sheet](./doc/screenshots/input_sheet.png?raw=true)

### プログラムの実行
ターミナルから以下のようにしてスクレイピングツールのプログラムを実行します。<br>
(以下はメルカリサイトを検索対象とした場合の例)<br>
```
cd WebScraper/app/MercariPriceMonitor
python3 mercariPriceMonitor.py
```

### 検索結果の取得
もし検索ワードにマッチした商品が見つかりますと以下のようにLINEへ通知します。<br>
![line_notify](./doc/screenshots/line_notify.png?raw=true)

また、以下のようにGoogleスプレッドシートの検索結果用シートに検索したアイテムの情報が記載されます。<br>
![output_sheet](./doc/screenshots/output_sheet.png?raw=true)

また、情報を重複なくするために再検索しても検索結果用シートに記載済みのアイテムであればLINE通知とシート記載はされません。<br>