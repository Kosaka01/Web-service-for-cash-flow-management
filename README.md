# CFM (ДДС) Web Service

Небольшой веб‑сервис на Django для учета движения денежных средств: записи, фильтры и управление справочниками.

## Требования
- Python 3.10+

## Установка
```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

## Настройка базы данных
```bash
python manage.py migrate
python manage.py loaddata cashflow/fixtures/initial_data.json
python manage.py createsuperuser
```

## Запуск
```bash
python manage.py runserver
```

Откройте:
- Основная страница: http://127.0.0.1:8000/
- Админка для справочников: http://127.0.0.1:8000/admin/

## Что реализовано
- CRUD для записей ДДС
- Фильтры по дате, статусу, типу, категории, подкатегории
- Зависимости: тип → категория → подкатегория
- Валидация на сервере и на клиенте
- Управление справочниками через Django admin

## Примечания
- Сумма хранится как Decimal (2 знака после запятой).
- Дата по умолчанию — текущая, но редактируемая.
