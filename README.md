# Работа с CSV-файлами
Скрипт для обработки CSV-файлов с поддержкой фильтрации и агрегации данных.

## Установка
```bash
pip install -r requirements.txt
```

## Использование
### Просмотр данных
После --file задайте путь к CSV-файлу

```bash
python3 main.py --file products.csv
```

### Примеры фильтрации
```bash
python3 main.py --file products.csv --where "price>500"
python3 main.py --file products.csv --where "price<300"
python3 main.py --file products.csv --where "brand=xiaomi"
```

### Агрегация
```bash
python3 main.py --file products.csv --aggregate "price=avg"
python3 main.py --file products.csv --aggregate "price=min"
python3 main.py --file products.csv --aggregate "price=max"
```

## Тестирование
```bash
pytest tests/
```

## Операции
### Фильтрация
- `>` - больше
- `<` - меньше
- `=` - равно
### Агрегация
- `avg` - среднее значение
- `min` - минимальное значение
- `max` - максимальное значение 