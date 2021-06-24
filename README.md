# IoT_Frame_RaspberryPi
[IoT_Frame_ops](https://github.com/spadr/IoT_Frame_ops)
で公開されているものをRaspberryPi向けに調節したものです。<br>
Docker buildに小一時間かかります。<br>


# Usage

### 動作確認のための手順
```
#このリポジトリをGit cloneする
$ git clone https://github.com/spadr/IoT_Frame_RaspberryPi.git

#cdを移動
$ cd IoT_Frame_ops

#.env.exampleを.envにリネーム
$ mv .env.example .env

#.envのEmail設定をする

#app/entrypoint.shの権限変更
$ chmod +x app/entrypoint.sh

#イメージをビルドし、各コンテナを起動
$ sudo docker-compose -f docker-compose.yml up -d --build

#稼働状況を確認
$ sudo docker-compose -f docker-compose.yml ps -a
すべてUpになっていればOKです


#実際にデータを送信する
test.pyにsin,cos.tan波を送信するテスト用コードを記載しております。
認証メールに記載されているアクセスキーを設定の上、お使いください。
また、実際にマイコンを使って送信する場合は下記のリポジトリにサンプルコードがあります。
https://github.com/spadr/CANASPAD-IoT_SAMPLE
```
### その他の操作
```
#データの初期化
$ sudo docker-compose -f docker-compose.yml exec app python manage.py flush --no-input

#マイグレーション
$ sudo docker-compose -f docker-compose.yml exec app python manage.py makemigrations

#DBの作成
$ sudo docker-compose -f docker-compose.yml exec app python manage.py migrate

#静的ファイルのコピー
$ sudo docker-compose -f docker-compose.yml exec app python manage.py collectstatic --no-input --clear

#Djangoの管理者ユーザの登録
$ sudo docker-compose -f docker-compose.yml exec app python manage.py createsuperuser

#イメージをビルドし、各コンテナを起動
$ sudo docker-compose -f docker-compose.yml up -d --build

#イメージ、コンテナ、ボリューム、ネットワークを削除
$ sudo docker-compose -f docker-compose.yml down

#各コンテナを開始
$ sudo docker-compose -f docker-compose.yml start

#各コンテナを停止
$ sudo docker-compose -f docker-compose.yml stop

#各コンテナをリスタート
$ sudo docker-compose -f docker-compose.yml restart

#稼働状況を確認
$ sudo docker-compose -f docker-compose.yml ps -a
```
