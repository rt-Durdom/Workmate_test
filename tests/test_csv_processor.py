import pytest
from main import OperationCSV
import csv

@pytest.fixture
def example_csv_file(tmp_path):
    """Создает временный CSV файл для тестов"""
    file_path = tmp_path / "test.csv"
    data = [
        ['name', 'brand', 'price', 'rating'],
        ['iphone 15 pro', 'apple', '999', '4.9'],
        ['galaxy s23 ultra', 'samsung', '1199', '4.8'],
        ['redmi note 12', 'xiaomi', '199', '4.6'],
        ['poco x5 pro', 'xiaomi', '299', '4.4']
    ]
    
    with open(file_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(data)
    
    return str(file_path)

def test_load_data(example_csv_file):
    """Тест загрузки данных из CSV файла"""
    test = OperationCSV(example_csv_file)
    test.load_data_in_file()
    assert len(test.data) == 4
    assert test.data[0]['name'] == 'iphone 15 pro'
    assert test.data[0]['brand'] == 'apple'

def test_parse_condition():
    """Тест парсинга условия фильтрации"""
    test = OperationCSV("test.csv")
    assert test.parse_condition("price>500") == ("price", ">", "500")
    assert test.parse_condition("brand=xiaomi") == ("brand", "=", "xiaomi")
    assert test.parse_condition("rating<4.5") == ("rating", "<", "4.5")

def test_filter_greater_than(example_csv_file):
    """Тест фильтрации с оператором 'больше'"""
    test = OperationCSV(example_csv_file)
    test.load_data_in_file()
    result = test.filter_data("price>500")
    assert len(result) == 2
    assert all(float(row['price']) > 500 for row in result)

def test_filter_less_than(example_csv_file):
    """Тест фильтрации с оператором 'меньше'"""
    test = OperationCSV(example_csv_file)
    test.load_data_in_file()
    result = test.filter_data("price<300")
    assert len(result) == 2
    assert all(float(row['price']) < 300 for row in result)

def test_filter_equals(example_csv_file):
    """Тест фильтрации с оператором 'равно'"""
    test = OperationCSV(example_csv_file)
    test.load_data_in_file()
    result = test.filter_data("brand=xiaomi")
    assert len(result) == 2
    assert all(row['brand'] == 'xiaomi' for row in result)

def test_filter_string_comparison(example_csv_file):
    """Тест фильтрации строковых значений"""
    test = OperationCSV(example_csv_file)
    test.load_data_in_file()
    result = test.filter_data("name>iphone 15 pro")
    assert len(result) == 2
    assert all(row['name'] > 'iphone' for row in result)

def test_filter_invalid_column(example_csv_file):
    """Тест фильтрации по несуществующей колонке"""
    test = OperationCSV(example_csv_file)
    test.load_data_in_file()
    with pytest.raises(ValueError):
        test.filter_data("invalid>500")

def test_parse_aggregation():
    """Тест парсинга условия агрегации"""
    test = OperationCSV("test.csv")
    assert test.parse_aggregation("price=max") == ("price", "max")
    assert test.parse_aggregation("price=min") == ("price", "min")
    assert test.parse_aggregation("price=avg") == ("price", "avg")
    
    with pytest.raises(ValueError):
        test.parse_aggregation("price avg")
    
    with pytest.raises(ValueError):
        test.parse_aggregation("price")

def test_aggregate_avg(example_csv_file):
    """Тест агрегации среднего значения"""
    test = OperationCSV(example_csv_file)
    test.load_data_in_file()
    result = test.aggregate(test.data, "price=avg")
    assert result == 674.0

def test_aggregate_min(example_csv_file):
    """Тест агрегации минимального значения"""
    test = OperationCSV(example_csv_file)
    test.load_data_in_file()
    result = test.aggregate(test.data, "price=min")
    assert result == 199.0

def test_aggregate_max(example_csv_file):
    """Тест агрегации максимального значения"""
    test = OperationCSV(example_csv_file)
    test.load_data_in_file()
    result = test.aggregate(test.data, "price=max")
    assert result == 1199.0

def test_filter_and_aggregate(example_csv_file):
    """Тест фильтрации и агрегации"""
    test = OperationCSV(example_csv_file)
    test.load_data_in_file()
    filtered_data = test.filter_data("price<500")
    result = test.aggregate(filtered_data, "price=max")
    assert result == 299.0

def test_aggregate_invalid_column(example_csv_file):
    """Тест агрегации по несуществующей колонке"""
    test = OperationCSV(example_csv_file)
    test.load_data_in_file()
    with pytest.raises(ValueError):
        test.aggregate(test.data, "invalid=max")

def test_aggregate_non_numeric(example_csv_file):
    """Тест агрегации нечисловой колонки"""
    test = OperationCSV(example_csv_file)
    test.load_data_in_file()
    with pytest.raises(ValueError):
        test.aggregate(test.data, "brand=max")


def test_invalid_aggregation(example_csv_file):
    """Тест обработки неверной операции агрегации"""
    test = OperationCSV(example_csv_file)
    test.load_data_in_file()
    with pytest.raises(ValueError):
        test.aggregate(test.data, "price=sum") 