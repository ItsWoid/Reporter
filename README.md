# Reporter
Ця програма автоматизує репорт телеграм каналів з російською пропагандою.

Схема роботи:
- Знаходимо канал
- Чекаємо 15 - 20 секунд
- Ставимо реакцію під рандомне повідомлення та чекаємо 15 - 20 секунд
- Якщо канал закрив реакції, чекаємо ще 20 - 20 секунд
- Кидаємо репорт
- Чекаємо 30 - 60 секунд

## Підготовка
Перед тим як встановлювати та запускати програму вам потрібні `api_id` та `api_hash`.
Для цього перейдіть за посиланням [https://my.telegram.org](https://my.telegram.org/), та зайдіть використовуючи ваш номер.
Натисніть **API development tools** та введіть **App title** і **Short name** **(App title та Short можуть бути які завгодно)**
<br>Далі ви дістанете `api_id` та `api_hash`, які зможете використати у програмі

## Встановлення

### Docker

Команда для запуску програми через docker:
```console
docker run -i -it --rm --pull always ghcr.io/itswoid/reporter:1.0.0
```

Також можна передати параметри через [аргументи](https://github.com/ItsWoid/Reporter#%D0%B0%D1%80%D0%B3%D1%83%D0%BC%D0%B5%D0%BD%D1%82%D0%B8).
Приклад:
```console
docker run -i -it --rm --pull always ghcr.io/itswoid/reporter:1.0.0 --api-id API_ID --api-hash API_HASH
```

### Python

1. Встановіть файли `main.py` та `requirements.txt`
2. Встановіть необхідні бібліотеки з файлу `requirements.txt`
```console
pip install -r requirements.txt
```
3. Запустіть програму
```console
python main.py
```
4. Програма попросить вас ввести api_id та api_hash, після чого вам потрібно буде ввести ваш номер телефону (у форматі +380XXXXXXXX) який прив'язаний до телеграму, і код який прийде

## Аргументи

Аргумент | Опис
--- | ---
--api-id | API ID
--api-hash | API Hash
