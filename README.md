# foodgram-project
foodgram-project

## Описание проекта
Приложение «Продуктовый помощник»: сайт, на котором пользователи публикую рецепты,
добавляют чужие рецепты в избранное и подписываются на публикации других авторов.
Сервис «Список покупок» позволит пользователям создавать список продуктов,
которые нужно купить для приготовления выбранных блюд.
##### Демо: http://84.201.150.162/ Логин admin, пароль admin
## Установка и запуск в Docker контейнере
- Создать в рабочей директории каталог для проекта: `mkdir foodgram-project`
- В каталог foodgram-project поместить файл docker-compose.yaml
- В каталоге foodgram-project создать каталог nginx и внего поместить файл настроек nginx.conf со следующим содержимым:
```
upstream web {
    server web:8000;
}
server {
    listen 80;
    location / {
        proxy_pass http://web;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header Host $host;
        proxy_redirect off;
    }

    location /static/ {
        alias /code/static/;
    }
    location /media/ {
        alias /code/media/;
    }
    server_tokens off;
}
```
- Обновит образ приложения с DockerHub `sudo docker pull dzanto/foodgram`
- Запустить контейнеры `sudo docker-compose up --detach`
- Перейти в контейнер web `docker-compose exec web bash`
- Внутри контейнера выполнить следующие команды:
```
python manage.py makemigrations shoplist
python manage.py migrate
python manage.py createsuperuser
python manage.py shell
>>> import shoplist.importcsv
>>> exit()
```
- Приложение готово к работе
## Стэк технологий
- Docker
- Nginx
- Djnago
- Django Rest Framework
- JS, CSS, HTML
## Об авторе:
######Шишлин Антон
######https://github.com/dzanto