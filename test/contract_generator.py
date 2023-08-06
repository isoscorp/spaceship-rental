import json
import random
import string
from os import path
from typing import List

from optimizer.contract import Contract


class ContractGenerator:
    """
    Helper class used to easily generate contracts, for testing.
    """

    DATA_FOLDER = path.join(
        path.abspath(path.dirname(path.dirname(__file__))), "test", "data"
    )

    def __init__(self, from_file: bool = False):
        """
        Initializes settings for contract generation.
        :param from_file: when True, contracts are generated from json files in data folder (defaults to False).
        """
        self.from_file = from_file

    @staticmethod
    def _generate_random_contract() -> Contract:
        """
        Returns a single Contract randomly generated.
        """
        return Contract(
            name="".join(random.choices(string.ascii_lowercase, k=12)),
            start=random.randint(0, 1000),
            duration=random.randint(1, 1000),
            price=random.randint(0, 1000),
        )

    def generate(
        self, nb_contracts: int, *, save_payload: bool = False
    ) -> List[Contract]:
        """
        Generates randomly a list of contracts and optionally saves the payload in a json file.
        If instance is initialized with from_file, this method returns
        contracts loaded from the json file named 'payload_{nb_contracts}' if file exists
        :param nb_contracts: number of contracts to be generated.
        :param save_payload: when True, saves the generated contracts in a json file (defaults to False).
        :return: the list of contracts generated.
        """
        if self.from_file:
            try:
                return self.load(json_file=f"payload_{nb_contracts}.json")
            except FileNotFoundError:
                save_payload = True
                pass

        contracts = [
            ContractGenerator._generate_random_contract() for _ in range(nb_contracts)
        ]

        if save_payload:
            with open(
                path.join(self.DATA_FOLDER, f"payload_{nb_contracts}.json"),
                "w",
                encoding="utf-8",
            ) as f:
                json.dump(
                    [c._asdict() for c in contracts], f, ensure_ascii=False, indent=4
                )

        return contracts

    def load(self, json_file: str) -> List[Contract]:
        """
        Generates a list of contracts from a json file.
        :param json_file: name of the json file containing the list of contracts.
        Must be located in the data folder defined at the class level.
        :return: the list of contracts generated.
        :raises: FileNotFoundError if file is missing from the data folder.
        """
        with open(path.join(self.DATA_FOLDER, json_file)) as f:
            data = json.load(f)
            return [Contract(**c) for c in data]
