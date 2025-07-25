
from batch import OrderLine

class OutOfStock(Exception):
    pass

def allocate(line: OrderLine, batches):
    try:
        batch = next(
            b for b in sorted(batches) if b.can_allocate(line)
        )
        batch.allocate(line)
        return batch.reference
    except StopIteration:
        raise OutOfStock(f"Out of stock for sku {line.sku}")