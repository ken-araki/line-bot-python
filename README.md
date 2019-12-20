# step to start app

## create ssl key (self certificate)

```bash
cd line-bot-python

mkdir nginx/ssl
cd nginx/ssl
openssl genrsa 2048 > server.key
openssl req -new -key server.key > server.csr
openssl x509 -days 36500 -req -signkey server.key < server.csr > server.crt
```

## create .env

```bash
touch python3/src/.env
echo "ALLOWED_HOSTS=localhost,127.0.0.1" >> python3/src/.env
echo "LINE_BOT_CHANNEL_SECRET=${your-channel-secret}" >> python3/src/.env
echo "LINE_BOT_CHANNEL_TOKEN=${your-channel-token}" >> python3/src/.env
echo "LINE_USER_ID=${your-user-id}" >> python3/src/.env
echo "GCP_PROJECT_ID=${your-gcp-project-id}" >> python3/src/.env
```

## create service-key and copy

access the following URL and create a service key from "認証情報を作成 > サービスアカウントキー"
https://console.cloud.google.com/apis/credentials?cloudshell=false&hl=ja

"サービスアカウント" can be anything, and "キーのタイプ" is JSON
Then the JSON will be downloaded, so copy the contents and paste it below

```bash
vi python3/src/service-key.json
```

## start app

```
docker-compose up -d --build
## do not need to execute this command
# docker-compose run python ./manage.py migrate

open https://localhost/todo
```