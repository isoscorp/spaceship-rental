from typing import List, Dict, Any

from fastapi import FastAPI
from pydantic import BaseModel

from optimizer.contract import Contract
from optimizer.contract_optimizer import ContractOptimizerFast

app = FastAPI(
    title="Spaceship Rental API",
    description="Spaceship rental API with high profitability",
    version="1.0",
)


class ContractModel(BaseModel):
    name: str
    start: int
    duration: int
    price: int


@app.post(
    "/spaceship/optimize",
    summary="Returns the sublist of non-overlapping contracts maximizing the income.",
)
async def optimize_contracts(contracts_model: List[ContractModel]) -> Dict[str, Any]:
    contracts = [
        Contract(name=c.name, start=c.start, duration=c.duration, price=c.price)
        for c in contracts_model
    ]
    return ContractOptimizerFast(contracts).optimize()
