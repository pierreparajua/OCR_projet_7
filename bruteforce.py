import pandas as pd

import time
import itertools
import operator
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
    df.drop(df[df['price'] <= 0].index, inplace=True)
    df.drop(df[df['profit'] <= 0].index, inplace=True)
    df['gain'] = df['price'] * df['profit']
    df_sorted = df.sort_values(by="gain", ascending=False)
    actions = [Action(name=action[0], price=action[1], profit=action[2],
                      gain=action[3]) for action in df_sorted.values]
    return actions


def force_brute(datas: list) -> list:
    """
    Compute all combinations, add each combinations to the list "all_combinations" if the total cost <= MAX_MONEY,
    and to finish, sort this list by profit and return it
    :param datas: Datas to test.
    :return: Sorted list by profit.
    """
    all_combinations = []
    for nbr_action in range(0, len(datas) + 1):
        print(nbr_action)
        for combination in itertools.combinations(datas, nbr_action):
            nbr_action_bought = len(combination)
            if nbr_action_bought != 0:
                combinations = []
                total_cost = 0
                total_return = 0
                for i in range(nbr_action_bought):
                    profit_by_action = combination[i].gain
                    combinations.append(combination[i].name)
                    total_return += profit_by_action
                    total_cost += combination[i].price
                if total_cost <= MAX_MONEY:
                    all_combinations.append([combinations, total_cost, total_return])
    return sorted(all_combinations, key=operator.itemgetter(2), reverse=True)


def display_result(results: list):
    """ Display the results"""
    print("\nRESULTS: ")
    for action in results[0]:
        print(action)
    print(f"Total cost: {results[1]}")
    print(f"Total return: {results[2]/100}")


def main(csv_file):
    best_combination = force_brute(load_data(csv_file))[0]
    display_result(best_combination)


if __name__ == "__main__":
    start = time.perf_counter()
    main(DATASET2)
    end = time.perf_counter()
    elapsed = end - start
    print(f'Temps d\'exécution : {elapsed}s')
