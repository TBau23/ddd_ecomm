import unittest
from batch import Batch, OrderLine
from datetime import date, timedelta



class TestAllocate(unittest.TestCase):
    def test_prefers_current_stock_batches_to_shipments(self):
        in_stock_batch = Batch('in-stock-batch', 'RETRO-CLOCK', 100, eta=None)
        shipment_batch = Batch('shipment-batch', 'RETRO-CLOCK', 100, eta=date.today())

        line = OrderLine('oref', 'RETRO-CLOCK', 10)

        allocate(line, [in_stock_batch, shipment_batch])

        self.assertEqual(in_stock_batch.available_quantity, 90)
        self.assertEqual(shipment_batch.available_quantity, 100)
    
    def test_prefers_earlier_batches(self):
        earliest = Batch('speedy-batch', 'MINIMALIST-SPOON', 100, eta=date.today())
        medium = Batch('normal-batch', 'MINIMALIST-SPOON', 100, eta=date.today() + timedelta(days=1))
        latest = Batch('slow-batch', 'MINIMALIST-SPOON', 100, eta=date.today() + timedelta(days=2))

        line = OrderLine('oref', 'MINIMALIST-SPOON', 10)

        allocate(line, [earliest, medium, latest])

        self.assertEqual(earliest.available_quantity, 90)
        self.assertEqual(medium.available_quantity, 100)
        self.assertEqual(latest.available_quantity, 100)
    
    def test_returns_allocated_batch_ref(self):
        in_stock_batch = Batch('in-stock-batch', 'RETRO-CLOCK', 100, eta=None)
        shipment_batch = Batch('shipment-batch', 'RETRO-CLOCK', 100, eta=date.today())
        line = OrderLine('oref', 'RETRO-CLOCK', 10)

        allocation = allocate(line, [in_stock_batch, shipment_batch])

        self.assertEqual(allocation, in_stock_batch.reference)
