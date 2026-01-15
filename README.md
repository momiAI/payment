## Запуск проекта осуществляется через Docker

`git clone https://github.com/momiAI/payment.git`
`cd payment`

**файл .example_env описывает секреты которые вам понадобятся, секреты которые связаны с бд уже заполнены и связаны с ней
вам нужно в корне проекта создать .env переместив содержимое файла .example_env и заполнить три секрета:**
- DJANGO_SECRET_KEY=1
- STRIPE_SECRET_KEY=1
- STRIPE_WEBHOOK_SECRET=1

## запуск проекта
docker-compose up --build

веб страница будет доступна по данному адресу `http://localhost:8000`

## остановка проекта:
docker-compose down
