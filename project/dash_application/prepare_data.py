from datetime import date, timedelta
import pandas as pd
import random
import os
from pathlib import Path

print(Path.cwd())  # /home/skovorodkin/stack
project_folder = Path(__file__).resolve().parent.parent
datafiles_path = str(project_folder) + '/datafiles'
print(datafiles_path)

def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)

start_date = date(2022, 1, 1)
end_date = date(2023, 6, 2)

data = {'Name': ['Tom', 'nick', 'krish', 'jack'],
        'Age': [20, 21, 19, 18]}

# df = pd.DataFrame(data)
# print(df)
result_data = {}
date_list = []
product_list = []
product_category_list = []
payment_list = []
product_source = {'Лизинг российской сельхозтехники': 'СХТ',
                  'Лизинг иностранной сельхозтехники': 'СХТ',
                  'Лизинг российской строительной техники': 'Строительная техника',
                  'Лизинг импортной строительной техники': 'Строительная техника',
                  'Лизинг авиационного оборудования': 'Оборудование',
                  'Лизинг медицинского оборудования': 'Оборудование',
                  }


for single_date in daterange(start_date, end_date):
    date_list.append(single_date)
    # получаем случайную запись из дикта с продуктами
    product_name, product_category = random.choice(list(product_source.items()))
    product_list.append(product_name)
    product_category_list.append(product_category)
    payment = random.randint(800000, 18000000)
    payment_list.append(payment)

result_data['Дата получения платежа'] = date_list
result_data['Продукт'] = product_list
result_data['Тип имущества'] = product_category_list
result_data['Сумма платежа'] = payment_list
df = pd.DataFrame(result_data)
df.to_csv(datafiles_path + '/next_payments_test_data_2.csv')


