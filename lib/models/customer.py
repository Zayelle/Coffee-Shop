from __future__ import annotations
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from lib.models.coffee import Coffee
    from lib.models.order import Order

class Customer:
    def __init__(self, name: str):
        self.name = name
        self._orders: List[Order] = []  # Explicit type annotation

    @property
    def name(self) -> str:
        """Get customer name"""
        return self._name

    @name.setter
    def name(self, value: str):
        """Set customer name with validation"""
        if not isinstance(value, str):
            raise TypeError("Name must be a string.")
        if not 1 <= len(value.strip()) <= 15:
            raise ValueError("Name must be a string between 1 and 15 characters.")
        self._name = value.strip()

    def orders(self) -> List[Order]:
        """Return a COPY of the orders list to prevent modification"""
        return self._orders.copy()

    def coffees(self) -> List[Coffee]:
        """Return a list of unique coffees ordered by the customer"""
        unique_coffees = {order.coffee.name: order.coffee for order in self._orders}
        return list(unique_coffees.values())

    def create_order(self, coffee: Coffee, price: float) -> Order:
        """Create a new order without adding it to orders list here"""
        from lib.models.order import Order
        return Order(self, coffee, price)  # Let Order.__init__ handle the relationship

    def __repr__(self):
        return f"<Customer name='{self.name}'>"