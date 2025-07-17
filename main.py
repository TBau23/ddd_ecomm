from dataclasses import dataclass
from datetime import date
from typing import Optional

@dataclass(frozen=True)
class OrderLine:
    orderid: str
    sku: str
    qty: int


class Batch:
    def __init__(self, ref: str, sku: str, qty: int, eta: Optional[date]):
        self.reference = ref
        self.sku = sku
        self.available_quantity = qty
        self.eta = eta

    def allocate(self, line: OrderLine):
        self.available_quantity -= line.qty

    def can_allocate(self, line: OrderLine):
        if self.sku != line.sku:
            return False
        if self.available_quantity < line.qty:
            return False
        return True

    def allocate(self, line: OrderLine):
        if self.can_allocate(line):
            self.available_quantity -= line.qty
