import pandas as pd

def print_data(list):
    for val in list:
        print(val)


def read_training_data():
    return pd.read_excel("training.xlsx")
