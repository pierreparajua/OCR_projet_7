import pandas as pd
import numpy as np

import time
from dataclasses import dataclass
from pathlib import Path


DATA_DIR = Path(__file__).resolve().parent / "data"

DATA_BRUTE = DATA_DIR / "data_brute.csv"
DATASET1 = DATA_DIR / "dataset1_Python+P7.csv"
DATASET2 = DATA_DIR / "dataset2_Python+P7.csv"

MAX_MONEY = 50000


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
       Modifie "price" and "gain" to obtain only integer
       Create a new columns "gains" and sort the dataframe according to "gain".
       :param csv_file:csv file to load
       :return:A list of objet action.
    """
    df = pd.read_csv(csv_file, sep=",")
    df.drop(df[df['price'] <= 0].index, inplace=True)  # supprime les valeurs < 0
    df.drop(df[df['profit'] <= 0].index, inplace=True)
    df['price'] = (df['price'] * 100).map(int)
    df['gain'] = df['price'] * (df['profit'] * 100).map(int)
    actions = [Action(name=action[0], price=action[1], profit=action[2],
                      gain=action[3]) for action in df.values]  # Crée une liste d ' objet Action
    return actions


def algo_optimize(datas: list) -> list:
    """
    Create a matrix (nbr_action * MAX_MONEY).
    Fill in the matrix box by box to find the best combination of actions.
    :param datas: Datas to test.
    :return: A list with the selected actions.
    """
    matrice = np.zeros((len(datas) + 1, MAX_MONEY + 1), dtype=int)  # Crée un matrice rempli de zéro (21 * 501)
    for r in range(1, len(datas) + 1):  # Boucle sur les lignes
        for c in range(1, MAX_MONEY + 1):  # Boucle sur les colonnes
            if datas[r - 1].price <= c:
                matrice[r][c] = max(datas[r - 1].gain + matrice[r - 1][c - datas[r - 1].price],
                                    matrice[r - 1][c])
            else:
                matrice[r][c] = matrice[r - 1][c]

    money = MAX_MONEY
    n = len(datas)
    selection = []
    while money > 0 and n >= 0:
        action = datas[n - 1]
        if matrice[n][money] == matrice[n - 1][money - action.price] + action.gain:
            selection.append(action)
            money -= action.price
        n -= 1
    return selection


def display_result(best_actions: list):
    """ Display the results"""
    tot = 0
    tot_return = 0
    for action in best_actions:
        print(action.name)
        tot += action.price / 100
        tot_return += action.gain / 1000000
    print(f"Total cost: {tot}")
    print(f"Total return: {round(tot_return, 2)}")


def main(csv_file):
    result = algo_optimize(load_data(csv_file))
    display_result(result)


if __name__ == "__main__":
    start = time.perf_counter()
    main(DATASET1)
    end = time.perf_counter()
    elapsed = end - start
    print(f'Temps d\'exécution : {elapsed}s')
