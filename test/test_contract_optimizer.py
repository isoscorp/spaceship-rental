import unittest

from optimizer.contract import Contract
from optimizer.contract_optimizer import (
    ContractOptimizerFast,
    ContractOptimizerNaive,
    ContractOptimizerNaiveImproved,
)
from test.tools import multitest


class Test(unittest.TestCase):
    def setUp(self) -> None:
        # self.optimizer_class = ContractOptimizerNaive
        # self.optimizer_class = ContractOptimizerNaiveImproved
        self.optimizer_class = ContractOptimizerFast

    @staticmethod
    def _make_contract(
        name: str, start: int = 0, duration: int = 1, price: int = 1
    ) -> Contract:
        return Contract(name=name, start=start, duration=duration, price=price)

    def test_optimize_single_contract_should_return_contract(self):
        c1 = self._make_contract("c1")
        result = self.optimizer_class([c1]).optimize()

        self.assertEqual(c1.price, result["income"])
        self.assertEqual([c1.name], result["path"])

    @multitest(
        [
            {"__description__": "2 contracts", "n": 2},
            {"__description__": "10 contracts", "n": 10},
            {"__description__": "100 contracts", "n": 100},
            {"__description__": "1000 contracts", "n": 1000},
            {"__description__": "10000 contracts", "n": 10000},
        ]
    )
    def test_optimize_n_contracts_disjointed_should_return_all_contracts(self, n):
        contracts = [
            self._make_contract(f"c{i}", start=i, duration=1) for i in range(n)
        ]
        result = self.optimizer_class(contracts).optimize()

        self.assertEqual(sum(c.price for c in contracts), result["income"])
        self.assertEqual([c.name for c in contracts], result["path"])

    @multitest(
        [
            {"__description__": "2 contracts", "n": 2},
            {"__description__": "10 contracts", "n": 10},
            {"__description__": "100 contracts", "n": 100},
            {"__description__": "1000 contracts", "n": 1000},
            {"__description__": "10000 contracts", "n": 10000},
        ]
    )
    def test_optimize_n_contracts_joined_should_return_contract_with_maximum_price(
        self, n
    ):
        contracts = [
            self._make_contract(f"c{i}", start=0, duration=2, price=i) for i in range(n)
        ]
        result = self.optimizer_class(contracts).optimize()

        self.assertEqual(contracts[-1].price, result["income"])
        self.assertEqual([contracts[-1].name], result["path"])

    def test_optimize_example(self):
        contracts = [
            self._make_contract("Contract1", start=0, duration=5, price=10),
            self._make_contract("Contract2", start=3, duration=7, price=14),
            self._make_contract("Contract3", start=5, duration=9, price=8),
            self._make_contract("Contract4", start=5, duration=9, price=7),
        ]
        result = self.optimizer_class(contracts).optimize()

        self.assertEqual(18, result["income"])
        self.assertEqual(["Contract1", "Contract3"], result["path"])
