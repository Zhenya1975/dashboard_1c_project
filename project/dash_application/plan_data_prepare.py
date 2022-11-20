from datetime import date, timedelta
import pandas as pd
import random
import os
from pathlib import Path
import datetime
import json

# print(Path.cwd())  # /home/skovorodkin/stack
project_folder = Path(__file__).resolve().parent.parent
datafiles_path = str(project_folder) + '/datafiles'
# print(datafiles_path)


def sales_data_source():
    sales_data_source_df = pd.read_csv(str(datafiles_path) + '/next_payments_test_data_2.csv')
    return sales_data_source_df


def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)


def plan_data_prepare_func():
    start_date = datetime.datetime(2022, 1, 1)
    end_date = datetime.datetime(2022, 12, 31)

    # список категорий
    sales_data_df = sales_data_source()
    sales_data_df["Дата получения платежа"] = pd.to_datetime(sales_data_df["Дата получения платежа"],
                                                             format="%Y-%m-%d")
    sales_data_df.sort_values(by="Дата получения платежа", inplace=True)
    sales_data_df['date'] = sales_data_df['Дата получения платежа']
    sales_data_df['payment'] = sales_data_df['Сумма платежа']
    # получаем список уникальных значений продуктовых категорий
    product_categories = sales_data_df['Продукт'].unique()
    product_categories_list = []
    for product in product_categories:
        product_categories_list.append(product)

    # получаем значение факта по каждой категории за 2022 год
    sales_data_2022_df = sales_data_df.loc[(sales_data_df['date'] >= start_date) &
                                                    (sales_data_df['date'] <= end_date)
                                                    ]
    product_category_plan_2022 = {}
    for product_category in product_categories_list:
        sales_data_2022_pr_df = sales_data_2022_df.loc[sales_data_2022_df['Продукт']==product_category]
        total_sales = sales_data_2022_pr_df['payment'].sum()
        # product_category_sales_2022[product_category] = total_sales
        rundom_coeff = random.uniform(0.7, 1.2)
        product_category_2022_plan = total_sales * rundom_coeff
        product_category_2022_plan = int(product_category_2022_plan)
        product_category_plan_2022[product_category] = product_category_2022_plan

    result_json_path = datafiles_path + '/plan_by_products.json'
    # print(result_json_path)
    with open(result_json_path, "w") as jsonFile:
        json.dump(product_category_plan_2022, jsonFile, ensure_ascii=False)

    return product_category_plan_2022

    # создаем

# plan_data_prepare_func()