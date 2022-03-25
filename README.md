## Встановлення

### Docker

Команда для запуску програми через docker:
```console
docker run -i -it --rm --pull always ghcr.io/itswoid/reporter:1.0.0
```

Також можна передати параметри через аргументи.
Приклад:
```console
docker run -i -it --rm --pull always ghcr.io/itswoid/reporter:1.0.0 --api-id API_ID --api-hash API_HASH
```

Аргументи:
Аргумент | Опис
--- | ---
--api-id | API ID
--api-hash | API Hash

### Python

1. Встановіть файл main.py
2. Встановіть необхідні бібліотеки з файлу requirements.txt (pip install -r requirements.txt)
3. Перейдіть за посиланням [https://my.telegram.org](https://my.telegram.org/), та зайдіть використовуючи ваш номер телефону.
Натичніть **API development tools** та введіть **App title** і **Short name** **(App title та Short можуть бути які завгодно)**
<br>Далі ви дістанете api_id та api_hash, які зможете використати у програмі
4. Програма попросить вас ввести api_id та api_hash, після чого вам потрібно буде ввести ваш номер телефону (у форматі +380XXXXXXXX) який прив'язаний до телеграму, і код який прийде
