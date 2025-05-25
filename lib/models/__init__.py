from __future__ import annotations
from typing import TYPE_CHECKING

# Import all models to make them available at package level
from .customer import Customer
from .coffee import Coffee
from .order import Order

__all__ = ['Customer', 'Coffee', 'Order']

if TYPE_CHECKING:
    # For type checkers only - helps with circular imports during development
    from .customer import Customer as CustomerType
    from .coffee import Coffee as CoffeeType
    from .order import Order as OrderType