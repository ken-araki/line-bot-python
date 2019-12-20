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
```

## start app

```
docker-compose up -d --build
docker-compose run python ./manage.py migrate

open https://localhost/todo
```