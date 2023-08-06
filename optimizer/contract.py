from typing import NamedTuple, List


class Contract(NamedTuple):
    """Valuable object with a period of validity.

    Attributes:
        name        Label of the contract.
        start       Beginning of the contract period of validity.
        duration    Length of the contract period of validity.
        price       Weight of the contract.
    """
    name: str
    start: int
    duration: int
    price: int

    @property
    def end(self) -> int:
        """Returns the end of the contract period of validity."""
        return self.start + self.duration

    def intersects(self, other: "Contract") -> bool:
        """
        Returns True if instance period of validity overlaps argument, False otherwise.
        :raises TypeError if argument is not a Contract.
        """
        if not isinstance(other, Contract):
            raise TypeError(f"Cannot compute intersection between Contract and {other.__class__.__name__}")

        return self.start <= other.start < self.end or other.start <= self.start < other.end


class ContractPath(NamedTuple):
    """Ordered set of Contracts.

    Attributes:
        income      Total price of the contracts forming the path.
        path        List of names of the contracts forming the path.
    """
    income: int
    path: List[str]
