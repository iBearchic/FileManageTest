# FileManageTest

## Фичи

- **Загрузка файлов**: Авторизированные пользователи могу загружать свои текстовые файлы.
- **Скачивание файлов**: Любой пользователь может скачать файл, предоставив его хэш.
- **Удаление файлов**: Авторизированные пользователи могу удалять файлы.

## Стек

- **Python 3.11**
- **Flask**
- **SQLAlchemy**
- **pytest**
- **BasicAuth**

## Установка

1. Склонировать репозиторий:

    ```sh
    git clone https://github.com/iBearchic/FileManageTest.git
    cd FileManageTest
    ```

2. Создать вертуальное окружение:

    ```sh
    python -m venv venv
    source venv/bin/activate  
    # On Windows use `venv\Scripts\activate`
    ```

3. Установить требуемые библиотеки:

    ```sh
    pip install -r requirements.txt
    ```

4. Инициализировать базу:

    ```sh
    python -c 'from app import init_db; init_db()'
    ```

## Запуск

Команда ниже запускает flask приложение:

```sh
python app.py
```

## API Endpoints

### Upload File

- **URL**: `/upload`
- **Method**: `POST`
- **Authorization**: Required
- **Form Data**: `file`

**Пример Curl запроса**:

```sh
curl -u user1:password1 -F "file=@<filepath>" http://localhost:5000/upload
```

### Download File

- **URL**: `/download/<file_hash>`
- **Method**: `GET`
- **Authorization**: Not required

**Пример Curl запроса**:

```sh
curl http://localhost:5000/download/<file_hash> --output output_file
```

### Delete File

- **URL**: `/delete`
- **Method**: `POST`
- **Authorization**: Required
- **JSON Body**: `{ "hash": "<file_hash>" }`

**Пример Curl запроса**:

```sh
curl -u user1:password1 -X POST -H "Content-Type: application/json" -d '{"hash":"<file_hash>"}' http://localhost:5000/delete
```

## Запуск тестов

```sh
pytest
```

## Логирование

В приложение предусмотрено логирование. Запись логов производится в файл app.log

## Масштабирование

- **Aссинхроннось**: Использование `aiohttp` для ассинхронной работы с запросами.
- **Улучшенная аутенфикация**: JWT для дополнительной безопасности.
- **Документация разработанногоAPI**
