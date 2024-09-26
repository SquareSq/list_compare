import os
import pandas as pd

file_sources_list = ['~/Projects/list_compare/список_кандидатов.xlsx',
                     '~/Projects/list_compare/список_проверка.xlsx']

# Словарь для хранения данных из каждого файла
file_data = {}


def file_to_dict(file_path):
    """Функция выполняет поиск колонок ФИО и Дата рождения создает из них 2 списка,
      а затем объединяет их в словарь."""
    df_orders = pd.read_excel(file_path, header=5)

    # Проверяем наличия требуемых колонок
    if 'Ф.И.О.' in df_orders.columns and 'Дата рождения' in df_orders.columns:
        names = df_orders['Ф.И.О.'].tolist()
        birth_date = df_orders['Дата рождения'].tolist()

        # Создаем словарь из списков
        return dict(zip(names, birth_date))
    else:
        print(f"Неверный формат данных в файле: {file_path}")
        return None


# Обработка и сохранение данных каждого файла
for file_source in file_sources_list:
    # Имя переменной для хранения данных
    variable_name = file_source.split('/')[-1].split('.')[0]
    file_data[variable_name] = file_to_dict(file_source)

# Извлечение данных из переменных
data1 = list(file_data.values())[0]
data2 = list(file_data.values())[1]

# Поиск совпадений
matches = {name: birth_date for name, birth_date in data1.items() if data2.get(name) == birth_date}

# Вывод данных совпадений в терминал
for key, value in matches.items():
    print(f"ФИО: {key}, Дата рождения: {value}")

# Сохранение совпадений
output_file_path = os.path.expanduser('~/Projects/list_compare/совпадения.txt')

# Убедиться, что директория существует
output_dir = os.path.dirname(output_file_path)
os.makedirs(output_dir, exist_ok=True)

with open(output_file_path, 'w', encoding='utf-8') as f:
    for name, birth_date in matches.items():
        f.write(f"{name}\t{birth_date}\n")

print(f"Совпадения сохранены в файл: {output_file_path}")
