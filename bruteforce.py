import csv
import itertools
import operator
from dataclasses import dataclass
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent / "data"

DATA_BRUTE = DATA_DIR / "data_brute.csv"
DATASET1 = DATA_DIR / "dataset1_Python+P7.csv"
DATASET2 = DATA_DIR / "dataset2_Python+P7.csv"


@dataclass
class Action:
    name: str
    price: float
    profit: float

    def buy(self) -> float:
        """
        Compute the gain for the purchase according to number of action
        :return: gain for the purchase
        """
        return self.price * self.profit


def load_data(csv_file: Path) -> list[Action]:
    """
    load datas from csv file and return a list of "Action"
    :param csv_file: csv file to load
    :return: List of objet Action
    """
    values = []
    with open(DATA_DIR / csv_file, 'r', newline='') as f:
        datas = csv.reader(f)
        for row in datas:
            if row[0] != "name":
                value = Action(name=row[0], price=float(row[1]), profit=float(row[2]) / 100)
                values.append(value)
        return values


def force_brute(datas):
    """
    Compute all combinaisons, add each combinaison to the list "all_combinaisons" if the total cost <= 500€,
    and to finish, sort this list by profit and return it
    :param datas: datas to compute
    :return: sorted list by profit
    """
    all_combinaisons = []
    for L in range(0, len(datas) + 1):
        for combinaison in itertools.combinations(datas, L):
            nbr_action_bought = len(combinaison)
            if nbr_action_bought != 0:
                combinaisons = []
                total_cost = 0
                total_return = 0
                for i in range(nbr_action_bought):
                    profit_by_action = combinaison[i].buy()
                    combinaisons.append(combinaison[i].name)
                    total_return += profit_by_action
                    total_cost += combinaison[i].price
                if total_cost <= 500:
                    all_combinaisons.append([combinaisons, total_cost, total_return])
    return sorted(all_combinaisons, key=operator.itemgetter(2), reverse=True)


if __name__ == "__main__":
    print("Work in progress ...")
    best_combinaison = force_brute(load_data(DATA_BRUTE))[0]
    print("\nRESULTS: ")
    for action in best_combinaison[0]:
        print(action)
    print(f"Total cost: {best_combinaison[1]}")
    print(f"Total return: {best_combinaison[2]}")
