from batch import Batch, OrderLine
from datetime import date, timedelta
from model import allocate, OutOfStock
import pytest


def test_prefers_current_stock_batches_to_shipments():
    in_stock_batch = Batch('in-stock-batch', 'RETRO-CLOCK', 100, eta=None)
    shipment_batch = Batch('shipment-batch', 'RETRO-CLOCK', 100, eta=date.today())

    line = OrderLine('oref', 'RETRO-CLOCK', 10)

    allocate(line, [in_stock_batch, shipment_batch])

    assert in_stock_batch.available_quantity == 90
    assert shipment_batch.available_quantity == 100


def test_prefers_earlier_batches():
    earliest = Batch('speedy-batch', 'MINIMALIST-SPOON', 100, eta=date.today())
    medium = Batch('normal-batch', 'MINIMALIST-SPOON', 100, eta=date.today() + timedelta(days=1))
    latest = Batch('slow-batch', 'MINIMALIST-SPOON', 100, eta=date.today() + timedelta(days=2))

    line = OrderLine('oref', 'MINIMALIST-SPOON', 10)

    allocate(line, [earliest, medium, latest])

    assert earliest.available_quantity == 90
    assert medium.available_quantity == 100
    assert latest.available_quantity == 100


def test_returns_allocated_batch_ref():
    in_stock_batch = Batch('in-stock-batch', 'RETRO-CLOCK', 100, eta=None)
    shipment_batch = Batch('shipment-batch', 'RETRO-CLOCK', 100, eta=date.today())
    line = OrderLine('oref', 'RETRO-CLOCK', 10)

    allocation = allocate(line, [in_stock_batch, shipment_batch])

    assert allocation == in_stock_batch.reference

def test_raises_out_of_stock_exception_if_cannot_allocate():
    b1 = Batch('in-stock', 'PURPLE-LAMP', 10, eta=None)
    line1 = OrderLine('oref', 'PURPLE-LAMP', 10)

    allocate(line1, [b1])

    with pytest.raises(OutOfStock, match='PURPLE-LAMP'):
        allocate(OrderLine('oref2', 'PURPLE-LAMP', 1), [b1])