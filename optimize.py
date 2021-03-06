import pandas as pd

import time
from dataclasses import dataclass
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent / "data"

DATA_BRUTE = DATA_DIR / "data_brute.csv"
DATASET1 = DATA_DIR / "dataset1_Python+P7.csv"
DATASET2 = DATA_DIR / "dataset2_Python+P7.csv"

MAX_MONEY = 500


@dataclass
class Action:
    name: str
    price: int
    profit: int
    gain: int


def load_data(csv_file: str) -> list:
    """
       Create a dataframe from csv file.
       Delete value <= 0.
       Create a new columns "gains" and sort the dataframe according to "gain".
       :param csv_file:csv file to load
       :return:A list of objet action.
    """
    df = pd.read_csv(csv_file, sep=",")
    df.drop(df[df['price'] <= 0].index, inplace=True)  # supprime les valeurs < 0
    df.drop(df[df['profit'] <= 0].index, inplace=True)
    df['gain'] = df['price'] * df['profit']
    df_sorted = df.sort_values(by="gain", ascending=False)
    actions = [Action(name=action[0], price=action[1], profit=action[2],
                      gain=action[3]) for action in df_sorted.values]  # Crée une liste d ' objet Action
    return actions


def algo_optimize(datas: list) -> list:
    """
    Select all actions possible with the best "gain".
    :param datas: Datas to test.
    :return: A list with the selected actions.
    """
    actions_selected = []
    remain_money = MAX_MONEY
    while remain_money > min(action.price for action in datas):
        for data in datas:
            if remain_money - data.price >= 0:
                actions_selected.append(data)
                remain_money = remain_money - data.price
                datas.remove(data)
    return actions_selected


def display_result(best_actions: list):
    """ Display the results"""
    tot = 0
    tot_return = 0
    for action in best_actions:
        print(action.name)
        tot += action.price
        tot_return += action.gain / 100
    print(tot)
    print(tot_return)


def main(csv_file):
    result = algo_optimize(load_data(csv_file))
    display_result(result)


if __name__ == "__main__":
    start = time.perf_counter()
    main(DATA_BRUTE)
    end = time.perf_counter()
    elapsed = end - start
    print(f'Temps d\'exécution : {elapsed}s')
