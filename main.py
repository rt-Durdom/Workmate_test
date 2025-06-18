import argparse
import csv
from typing import List, Dict, Any, Union
from tabulate import tabulate


OPERATORS = {'>', '<', '='}
OPERATIONS = ['avg', 'min', 'max']


class OperationCSV:
    def __init__(self, file_path: str):
        self.file_path: str = file_path
        self.data: List[Dict[str, Any]] = []

    def load_data_in_file(self) -> None:
        """Загружает данные из CSV файла"""
        with open(self.file_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            self.data = list(reader)

    def parse_condition(self, condition: str) -> tuple:
        """Парсит условие фильтрации"""
        for op in OPERATORS:
            if op in condition:
                column, value = condition.split(op)
                return column, op, value
        raise ValueError(f"Неподдерживаемый оператор в условии: {condition}")

    def filter_operator(self, condition: str, x: str, y: str) -> bool:
        """Фильтрует данные по заданному условию"""
        try:
            # Пробуем сравнить как числа
            if condition == ">" and float(x) > float(y):
                return True
            elif condition == "<" and float(x) < float(y):
                return True
            elif condition == "=" and str(x) == str(y):
                return True
        except ValueError:
        # Если не получилось преобразовать в числа, сравниваем как строки
            if condition == ">" and str(x) > str(y):
                return True
            elif condition == "<" and str(x) < str(y):
                return True
            elif condition == "=" and str(x) == str(y):
                return True
        return False

    def filter_data(self, condition: str) -> List[Dict[str, Any]]:
        """Фильтрует данные по заданному условию"""
        if not self.data:
            raise ValueError("Нет данных для фильтрации")
        column, operator, value = self.parse_condition(condition)
        if column not in self.data[0]:
            raise ValueError(f"Колонка {column} не найдена")
        filtered = [row for row in self.data if self.filter_operator(
            operator,
            row[column], value
        )]
        return filtered

    def filter_operations(
        self,
        operation: str,
        value: List[Union[float, int]]
    ) -> Union[float, int]:
        """Выполняет операцию агрегации"""
        if operation == 'avg':
            return sum(value) / len(value)
        elif operation == 'min':
            return min(value)
        elif operation == 'max':
            return max(value)
        else:
            raise ValueError(
                f"Неподдерживаемая операция агрегации: {operation}"
            )

    def parse_aggregation(self, aggregation: str) -> tuple:
        """Парсит условие агрегации"""
        if '=' not in aggregation:
            raise ValueError(f"Неверный формат агрегации: {aggregation}")
        column, operation = aggregation.split('=')
        if operation not in OPERATIONS:
            raise ValueError(f"Неподдерживаемая операция агрегации: {operation}")
        return column.strip(), operation

    def aggregate(self, data: List[Dict[str, Any]], condition: str) -> float:
        """Выполняет агрегацию данных"""
        if not data:
            raise ValueError(
                "Нет данных для агрегации после применения фильтра"
            )
        column, operation = condition.split('=')
        if column not in data[0]:
            raise ValueError(f"Колонка {column} не найдена")
        values = []
        for row in data:
            value = float(row[column])
            values.append(value)
        results = self.filter_operations(operation, values)
        return results


def main():
    input_obj = argparse.ArgumentParser(description='Обработка CSV файлов')
    input_obj.add_argument('--file', required=True, help='Путь к CSV файлу')
    input_obj.add_argument(
        '--where',
        action='append',
    )
    input_obj.add_argument('--aggregate')

    string_input = input_obj.parse_args()
    try:
        csv_obj = OperationCSV(string_input.file)
        csv_obj.load_data_in_file()
        filtered_data = csv_obj.data
        if string_input.where:
            for condition in string_input.where:
                filtered_data = csv_obj.filter_data(condition)
                csv_obj.data = filtered_data
            print(tabulate(filtered_data, headers='keys', tablefmt='grid'))
        if string_input.aggregate:
            aggr_data = csv_obj.aggregate(
                filtered_data,
                string_input.aggregate
            )
            column, operation = string_input.aggregate.split('=')
            print(tabulate([[aggr_data]], headers=[operation], tablefmt='grid'))

        if not string_input.where and not string_input.aggregate:
            print(tabulate(csv_obj.data, headers='keys', tablefmt='grid'))
    except Exception as e:
        print(f"Ошибка: {str(e)}")


if __name__ == '__main__':
    main()
