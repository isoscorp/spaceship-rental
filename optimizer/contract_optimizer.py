import math
from typing import List, Dict, Any

from optimizer.contract import Contract, ContractPath


class ContractOptimizerNaive:
    """
    DEPRECATED
    Entry class for contract naive optimization.

    Iterates over the list of contracts sorted by descending end.
    For each contract, iterates over its successors and store the best path found:
    - if no successor found: best path is the sublist of current contract itself;
    - if successors found: best path is the sublist of current contract +
    best path of the successor with the maximum income.
    Result is the best path with the maximum income.
    Time complexity: O(n²) with n the number of contracts.
    """
    def __init__(self, contracts: List[Contract]):
        self.contracts = contracts

    def optimize(self) -> Dict[str, Any]:
        n = len(self.contracts)
        self.contracts = sorted(self.contracts, key=lambda c: c.end)

        # keep track of intermediate results: best path for contract c[i] is (c[i] + best path for contract c[i+1])
        best_path_by_contract: Dict[str, ContractPath] = {}

        # for each contract ci, find best successor cj
        for i in reversed(range(n)):
            ci = self.contracts[i]
            best_successor = ""
            best_total_price = 0

            # iterates over all successors of contract ci
            for j in range(i + 1, n):
                cj = self.contracts[j]

                # not a successor of ci => skip
                if ci.intersects(cj):
                    continue

                # track successor with maximum income
                if best_total_price < best_path_by_contract[cj.name].income:
                    best_total_price = best_path_by_contract[cj.name].income
                    best_successor = cj.name

            # store best price & path
            best_path_by_contract[ci.name] = ContractPath(
                income=ci.price + best_total_price,
                path=[ci.name] + best_path_by_contract[best_successor].path
                if best_successor
                else [ci.name],
            )

        best_contract = max(
            best_path_by_contract, key=lambda c: best_path_by_contract[c].income
        )
        return best_path_by_contract[best_contract]._asdict()


class ContractOptimizerNaiveImproved:
    """
    DEPRECATED
    Entry class for contract naive optimization, slightly improved.

    Same as ContractOptimizerNaive with the following improvements:
    - contracts are sorted by ascending start
    - this allows to stop iterating over successors starting after the 1st successor
    - dataclass replaced with namedtuple (requires extra serialization in endpoint)
    - inlined function calls
    Time complexity: O(n²) with n the number of contracts.
    """
    def __init__(self, contracts: List[Contract]):
        self.contracts = contracts

    def optimize(self) -> Dict[str, Any]:
        """
        Iterates over current contracts to find the path maximizing the total price.
        :return: a dictionary with the sublist of optimized contracts and the maximum income associated.
        """
        n = len(self.contracts)
        self.contracts = sorted(self.contracts, key=lambda c: c.start)

        # keep track of intermediate results: best path for contract c[i] is (c[i] + best path for contract c[i+1])
        best_path_by_contract: Dict[str, ContractPath] = {}

        # for each contract ci, find best successor cj
        for i in reversed(range(n)):
            ci = self.contracts[i]
            best_successor = ""
            best_total_price = 0
            successor_shortest_end = math.inf

            # iterates over all successors of contract ci
            for j in range(i + 1, n):
                cj = self.contracts[j]

                # not a successor of ci => skip
                if cj.start < ci.start + ci.duration:
                    continue
                # contract is a successor of ci
                elif cj.start + cj.duration < successor_shortest_end:
                    successor_shortest_end = cj.start + cj.duration
                # contract starts after another successor => all direct successors of ci have been found
                elif cj.start > successor_shortest_end:
                    break

                # track successor with maximum income
                if best_total_price < best_path_by_contract[cj.name].income:
                    best_total_price = best_path_by_contract[cj.name].income
                    best_successor = cj.name

            # store best price & path for contract ci
            best_path_by_contract[ci.name] = ContractPath(
                income=ci.price + best_total_price,
                path=[ci.name] + best_path_by_contract[best_successor].path
                if best_successor
                else [ci.name],
            )

        best_contract = max(
            best_path_by_contract, key=lambda c: best_path_by_contract[c].income
        )
        return best_path_by_contract[best_contract]._asdict()


class ContractOptimizerFast:
    """
    Entry class for contract optimization.

    Iterates over the list of contracts sorted by ascending start.
    For each contract, find the closest successor and store the best path found SO FAR:
    - if no closest successor found: best path with current contract is the sublist of contract itself;
    - if closest successor found: best path with current contract is the sublist of contract +
    best path of the closest successor.
    - if best path with contract has a lower income than best path without contract,
    store previous best path for the current contract instead.
    Result is the best path with the maximum income.
    Time complexity: O(n*log(n)) with n the number of contracts.
    """

    def __init__(self, contracts: List[Contract]):
        self.contracts = contracts

    @staticmethod
    def find_nearest_successor(contracts: List[Contract], index: int) -> int:
        """
        Returns the index of the closest successor of current contract, -1 if not found.
        Ci is a successor of Cj if Ci.start >= Cj.start + Cj.duration.
        NOTE: contract list should be properly sorted by ascending start.
        :param contracts: list of contracts to search in.
        :param index: position of the current contract in the input list.
        :return: position of the next non-overlapping contract in the input list.
        """
        # optimized with binary search
        left, right = index + 1, len(contracts) - 1
        current_end_time = contracts[index].start + contracts[index].duration
        result = -1

        while left <= right:
            mid = (left + right) // 2

            if contracts[mid].start >= current_end_time:
                right = mid - 1
                result = mid
            else:
                left = mid + 1

        return result

    def optimize(self) -> Dict[str, Any]:
        """
        Iterates over current contracts to find the path maximizing the total price.
        :return: a dictionary with the sublist of optimized contracts and the maximum income associated.
        """
        n = len(self.contracts)
        self.contracts = sorted(self.contracts, key=lambda c: c.start)

        # keeps track of intermediate results:
        # best path for contract c[i] is the path with maximum income among:
        # - best path with c[i] = c[i] + best path of nearest successor of c[i]
        # - best path without c[i] = best path of last known contract c[i+1]
        best_path_by_contract: Dict[str, ContractPath] = {}

        # for each contract ci, find best successor cj
        for i in reversed(range(n)):
            ci = self.contracts[i]
            current_income, current_path = ci.price, [ci.name]

            # best path of last known contract c[i+1]
            best_contract_path = (
                best_path_by_contract[self.contracts[i + 1].name] if i < n - 1 else None
            )
            best_income = best_contract_path.income if best_contract_path else 0

            # find closest successor of ci to form the best possible path with ci
            nearest_successor_id = self.find_nearest_successor(self.contracts, i)
            if nearest_successor_id != -1:
                nearest_successor = best_path_by_contract[
                    self.contracts[nearest_successor_id].name
                ]
                current_income += nearest_successor.income
                current_path += nearest_successor.path

            # compare best possible path with ci & best path without ci
            if current_income > best_income:
                best_contract_path = ContractPath(
                    income=current_income, path=current_path
                )

            # store best price & path for ci
            best_path_by_contract[ci.name] = best_contract_path     # type: ignore

        best_contract = max(
            best_path_by_contract, key=lambda c: best_path_by_contract[c].income
        )
        return best_path_by_contract[best_contract]._asdict()
