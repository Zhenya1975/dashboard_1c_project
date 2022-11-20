import datetime

import pandas as pd
from pathlib import Path

project_folder = Path(__file__).resolve().parent.parent
# print(project_folder)
datafiles_path = str(project_folder) + '/datafiles'
def sales_data_source():
    sales_data_source_df = pd.read_csv(str(datafiles_path) + '/next_payments_test_data_2.csv')
    return sales_data_source_df

def prepare_df_from_csv(file_path):
    df = pd.read_csv(file_path)
    # df = pd.read_csv('project/datafiles/next_payments_test_data.csv')
    print(df)

# выпекаем датафрейм, который отдаст накопленный результат продаж 2022 года
def actual_2022_sales():
    sales_data_df = sales_data_source()
    sales_data_df["Дата получения платежа"] = pd.to_datetime(sales_data_df["Дата получения платежа"],
                                                                 format="%Y-%m-%d")
    sales_data_df.sort_values(by="Дата получения платежа", inplace=True)
    sales_data_df['date'] = sales_data_df['Дата получения платежа']
    sales_data_df['payment'] = sales_data_df['Сумма платежа']
    today = datetime.datetime.now()
    first_day_2022 = datetime.datetime(2022, 1, 1 )
    sales_data_2022_till_now_df = sales_data_df.loc[(sales_data_df['date'] >= first_day_2022) &
                                                    (sales_data_df['date'] <= today)
                                                    ]
    sales_data_2022_till_now_df=sales_data_2022_till_now_df.copy()
    sales_data_2022_till_now_df['payment_cum'] = sales_data_2022_till_now_df['payment'].cumsum()
    # print(sales_data_2022_till_now_df)
    return sales_data_2022_till_now_df

# actual_2022_sales()
