import time
from dataclasses import dataclass
from pathlib import Path

import pandas as pd
import numpy as np

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


def load_data(csv_file):
    df = pd.read_csv(csv_file, sep=",")
    df.drop(df[df['price'] <= 0].index, inplace=True)  # supprime les valeurs < 0
    df.drop(df[df['profit'] <= 0].index, inplace=True)
    df['gain'] = df['price'] * df['profit']
    # df['price'] = df['price'] * 100
    # df['price'] = df['price'].map(int)
    # df['gain'] = df['gain'] * 100
    # df['gain'] = df['gain'].map(int)
    actions = [Action(name=action[0], price=action[1], profit=action[2],
                      gain=action[3]) for action in df.values]  # Crée une liste d ' objet Action
    return actions


def algo_optimize(datas, max_money):
    matrice = np.zeros((len(datas) + 1, max_money + 1), dtype=int)  # Crée un matrice rempli de zéro (21 * 501)
    for r in range(1, len(datas) + 1):  # Boucle sur les lignes
        for c in range(1, max_money + 1):  # Boucle sur les colonnes
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


def display_result(best_actions):
    tot = 0
    tot_return = 0
    for action in best_actions:
        print(action.name)
        tot += action.price
        tot_return += action.gain / 100
    print(tot)
    print(tot_return)


if __name__ == "__main__":
    start = time.time()

    filter_datas = load_data(DATA_BRUTE)
    actions_selected = algo_optimize(filter_datas, MAX_MONEY)
    display_result(actions_selected)

    end = time.time()
    elapsed = end - start
    print(f'Temps d\'exécution : {elapsed}s')
