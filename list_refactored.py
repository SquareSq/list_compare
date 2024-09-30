
import os
import pandas as pd

file_sources_list = [
    '~/Projects/list_compare/список_кандидатов.xlsx',
    '~/Projects/list_compare/список_проверка.xlsx'
]

# Функция для преобразования файла в словарь
def file_to_dict(file_path):
    """Создает словарь из колонок ФИО и Дата рождения файла Excel."""
    df_orders = pd.read_excel(file_path, header=5)

    if {'Ф.И.О.', 'Дата рождения'}.issubset(df_orders.columns):
        names = df_orders['Ф.И.О.'].tolist()
        birth_dates = df_orders['Дата рождения'].tolist()
        return dict(zip(names, birth_dates))
    else:
        print(f"Неверный формат данных в файле: {file_path}")
        return {}

# Обработка файлов и создание словарей данных
def process_files(file_sources):
    file_data = {}
    for file_source in file_sources:
        file_path = os.path.expanduser(file_source)
        file_name = os.path.basename(file_path).split('.')[0]
        file_data[file_name] = file_to_dict(file_path)
    return file_data

# Поиск совпадений
def find_matches(data1, data2):
    return {name: dob for name, dob in data1.items() if data2.get(name) == dob}

# Сохранение совпадений в файл
def save_matches(matches, output_path):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        for name, birth_date in matches.items():
            f.write(f"{name}\t{birth_date}\n")

def main():
    file_data = process_files(file_sources_list)
    data1, data2 = list(file_data.values())
    matches = find_matches(data1, data2)

    # Вывод совпадений в терминал
    for name, birth_date in matches.items():
        print(f"ФИО: {name}, Дата рождения: {birth_date}")

    # Сохранение совпадений
    output_file_path = os.path.expanduser('~/Projects/list_compare/совпадения.txt')
    save_matches(matches, output_file_path)
    print(f"Совпадения сохранены в файл: {output_file_path}")

if __name__ == "__main__":
    main()