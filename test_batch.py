import unittest
from batch import Batch, OrderLine
from datetime import date


class TestBatch(unittest.TestCase):

    def make_batch_and_line(self, sku, batch_qty, line_qty):
        return (
            Batch("batch-001", sku, batch_qty, eta=date.today()),
            OrderLine("order-123", sku, line_qty),
        )

    def test_allocating_to_a_batch_reduces_the_available_quantity(self):
        large_batch, small_line = self.make_batch_and_line("ELEGANT-LAMP", 20, 2)

        large_batch.allocate(small_line)

        self.assertEqual(large_batch.available_quantity, 18)

    def test_can_allocate_if_available_greater_than_required(self):
        large_batch, small_line = self.make_batch_and_line("ELEGANT-LAMP", 20, 2)

        self.assertEqual(large_batch.can_allocate(small_line), True)

    def test_cannot_allocate_if_available_smaller_than_required(self):
        small_batch, large_line = self.make_batch_and_line("ELEGANT-LAMP", 2, 20)

        self.assertEqual(small_batch.can_allocate(large_line), False)

    def test_can_allocate_if_available_equal_to_required(self):
        batch, line = self.make_batch_and_line("ELEGANT-LAMP", 2, 2)

        self.assertEqual(batch.can_allocate(line), True)

    def test_cannot_allocate_if_skus_do_not_match(self):
        batch = Batch("batch-001", "UGLY-CHAIR", 100, eta=None)
        different_sku_line = OrderLine("order-123", "KITCHEN-GIZMO", 10)

        self.assertEqual(batch.can_allocate(different_sku_line), False)

    def test_can_only_deallocate_allocated_lines(self):
        batch, unallocated_line = self.make_batch_and_line("ELEGANT-LAMP", 20, 2)
        batch.deallocate(unallocated_line)

        self.assertEqual(batch.available_quantity, 20)

    def test_allocation_is_idempotent(self):
        batch, line = self.make_batch_and_line("GRAND-PIANO", 20, 2)
        batch.allocate(line)
        batch.allocate(line)
        self.assertEqual(batch.available_quantity, 18)
    


    