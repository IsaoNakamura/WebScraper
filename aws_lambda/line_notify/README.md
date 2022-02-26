# LineNotify on AWS Lambda

## インストール方法
```
cd aws_lambda/line_notify
pip install -r requirements.txt -t .
zip -r line_notify.zip *
```

## ポリシー追加
GitHub actionsに登録するアクセスキーID・シークレットアクセスキーのIAMユーザに以下のポリシーを持たせる。<br>
```
AWSLambdaRole
```