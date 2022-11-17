import pandas as pd


def prepare_df_from_csv(file_path):
    df = pd.read_csv('project/datafiles/next_payments_test_data.csv')
    print(df)