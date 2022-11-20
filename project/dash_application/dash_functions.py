import datetime
import random
from datetime import date, timedelta
import pandas as pd
from pathlib import Path
import json

project_folder = Path(__file__).resolve().parent.parent
# print(project_folder)
datafiles_path = str(project_folder) + '/datafiles'
def sales_data_source():
    sales_data_source_df = pd.read_csv(str(datafiles_path) + '/next_payments_test_data_2.csv')
    return sales_data_source_df

def prepare_df_from_csv(file_path):
    df = pd.read_csv(file_path)
    # df = pd.read_csv('project/datafiles/next_payments_test_data.csv')
    # print(df)

def selector_content_list(input_from_select, full_selector_list):
    """принимает то, что мы взяли из селекта и список полных значений этого селекта. И отдает результат в виде списка значение селекта"""
    result_select_list = []
    if input_from_select == None:
        result_select_list = full_selector_list

    elif len(input_from_select) == 0:
        result_select_list = full_selector_list

    elif len(input_from_select) > 0:
        result_select_list = input_from_select
    else:
        print("что-то странное в функции selector_content")
    return result_select_list

# выпекаем датафрейм, который отдаст накопленный результат продаж 2022 года
def actual_2022_sales(product_select):
    """расчет df для графика План-факт, ряд с фактическими продажами"""

    sales_data_df = sales_data_source()
    sales_data_df["Дата получения платежа"] = pd.to_datetime(sales_data_df["Дата получения платежа"],
                                                                 format="%Y-%m-%d")
    sales_data_df.sort_values(by="Дата получения платежа", inplace=True)
    sales_data_df['date'] = sales_data_df['Дата получения платежа']
    sales_data_df['payment'] = sales_data_df['Сумма платежа']
    today = datetime.datetime.now()
    first_day_2022 = datetime.datetime(2022, 1, 1)
    sales_data_2022_till_now_df = sales_data_df.loc[(sales_data_df['date'] >= first_day_2022) &
                                                    (sales_data_df['date'] <= today)
                                                    ]

    full_product_list = product_select_full_list()
    product_select_list = selector_content_list(product_select, full_product_list)

    sales_data_2022_till_now_filtered_df = sales_data_2022_till_now_df.loc[
            sales_data_2022_till_now_df['Продукт'].isin(product_select_list)
        ]

    sales_data_2022_till_now_df=sales_data_2022_till_now_filtered_df
    sales_data_2022_till_now_df['payment_cum'] = sales_data_2022_till_now_df['payment'].cumsum()
    # print(sales_data_2022_till_now_df)
    return sales_data_2022_till_now_df

def expected_2022_sales(product_select):
    sales_data_df = sales_data_source()
    sales_data_df["Дата получения платежа"] = pd.to_datetime(sales_data_df["Дата получения платежа"],
                                                             format="%Y-%m-%d")
    sales_data_df.sort_values(by="Дата получения платежа", inplace=True)
    sales_data_df['date'] = sales_data_df['Дата получения платежа']
    sales_data_df['payment'] = sales_data_df['Сумма платежа']
    today = datetime.datetime.now()


    last_day_2022 = datetime.datetime(2022, 12, 31)

    full_product_list = product_select_full_list()
    product_select_list = selector_content_list(product_select, full_product_list)

    expected_sales_data_df = sales_data_df.loc[(sales_data_df['date'] >= today) &
                                               (sales_data_df['date'] <= last_day_2022) &
                                               (sales_data_df['Продукт'].isin(product_select_list))
                                               ]

    # получаем текущую накопленную сумму с 1 января по сегодня
    first_day_2022 = datetime.datetime(2022, 1, 1)
    sales_data_2022_till_now_df = sales_data_df.loc[(sales_data_df['date'] >= first_day_2022) &
                                                    (sales_data_df['date'] <= today) &
                                                    (sales_data_df['Продукт'].isin(product_select_list))
                                                    ]

    current_sales_total = sales_data_2022_till_now_df['payment'].sum()
    # создаем df с начальной строкой
    start_df_for_cumsum = [{'date': today, 'payment': current_sales_total}]
    start_df_for_cumsum_df = pd.DataFrame(start_df_for_cumsum)
    # выбираем колонки из основного датафрейма
    sales_data_2022_till_now_df = expected_sales_data_df.loc[:, ['date', 'payment']]
    sales_data_2022_till_now_for_cumsum_df = pd.concat([start_df_for_cumsum_df, sales_data_2022_till_now_df], axis=0, ignore_index=True)
    # добавляем колонку с накоплением
    sales_data_2022_till_now_for_cumsum_df['payment_cum'] = sales_data_2022_till_now_for_cumsum_df['payment'].cumsum()
    # print(sales_data_2022_till_now_for_cumsum_df)

    return sales_data_2022_till_now_for_cumsum_df


def product_select_content():
    sales_data_df = sales_data_source()
    sales_data_df["Дата получения платежа"] = pd.to_datetime(sales_data_df["Дата получения платежа"],
                                                             format="%Y-%m-%d")
    sales_data_df.sort_values(by="Дата получения платежа", inplace=True)
    sales_data_df['date'] = sales_data_df['Дата получения платежа']
    sales_data_df['payment'] = sales_data_df['Сумма платежа']
    # получаем список уникальных значений продуктовых категорий
    product_categories = sales_data_df['Продукт'].unique()
    product_categories_options = []
    for product in product_categories:
        temp_dict = {}
        temp_dict['label'] = product
        temp_dict['value'] = product
        product_categories_options.append(temp_dict)

    return product_categories_options



def product_select_full_list():
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

    return product_categories_list

def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)
def sales_plan_2022(product_select):
    """Расчет плана продаж."""
    # получаем диапазон дат в 2022 году
    start_date = date(2022, 1, 1)
    end_date = date(2022, 12, 31)

    result_json_path = datafiles_path + '/plan_by_products.json'
    with open(result_json_path, 'r') as openfile:
        plan_data_saved = json.load(openfile)

    # Получаем значение плана для выборки. с учетом примененного фильтра по продуктам


    full_product_list = product_select_full_list()
    product_select_list = selector_content_list(product_select, full_product_list) # список продуктов с учетом фильтра
    filtered_product_plan_data = {}
    plan_sum_payment = 0
    for key, value in plan_data_saved.items():
        if key in product_select_list:
            filtered_product_plan_data['product'] = key
            filtered_product_plan_data['plan_value'] = value
            plan_sum_payment = plan_sum_payment + value

    plan_data_result_list = []
    for single_date in daterange(start_date, end_date):
        temp_dict = {}
        temp_dict['date'] = single_date
        temp_dict['plan'] = plan_sum_payment
        plan_data_result_list.append(temp_dict)

    plan_data_df = pd.DataFrame(plan_data_result_list)


    return plan_data_df



def donut_fact_2022_data():
    sales_data_df = sales_data_source()
    sales_data_df["Дата получения платежа"] = pd.to_datetime(sales_data_df["Дата получения платежа"],
                                                             format="%Y-%m-%d")
    sales_data_df.sort_values(by="Дата получения платежа", inplace=True)
    sales_data_df['date'] = sales_data_df['Дата получения платежа']
    sales_data_df['payment'] = sales_data_df['Сумма платежа']


