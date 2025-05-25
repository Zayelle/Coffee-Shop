from __future__ import annotations
from typing import TYPE_CHECKING, List, ClassVar, Dict, Optional
from decimal import Decimal

if TYPE_CHECKING:
    from lib.models.coffee import Coffee
    from lib.models.order import Order

class Customer:
     # Class variable to track all customer instances
    _all_customers: ClassVar[List[Customer]] = []
    customer_count: ClassVar[int] = 0  # Shared across all instances

    def __init__(self, name: str):
        self.name = name
        self._orders: List[Order] = []  # Explicit type annotation
        Customer._all_customers.append(self)
        Customer.customer_count += 1

    @classmethod
    def most_aficionado(cls, coffee: Coffee) -> Optional['Customer']:
        """
        Returns the customer who has spent the most on the given coffee.
        """
        max_spent = Decimal('0')
        top_customer = None

        for customer in cls._all_customers:
            # Calculate total spent by this customer on the given coffee
            total = sum(Decimal(str(order.price)) for order in customer.orders() if order.coffee == coffee)
            if total > max_spent:
                max_spent = total
                top_customer = customer

        return top_customer
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
        """Create a new order and add it to the orders list"""
        from lib.models.order import Order
        order = Order(self, coffee, price)
        if order not in self._orders:  # Prevent duplicates
            print(f"Creating order for {self.name} with coffee {coffee.name} at price {price}")
            self._orders.append(order)
        return order

    def __repr__(self):
        return f"<Customer name='{self.name}'>"


    def get_customer_name(customer_id: int) -> Optional[str]:
       # Returns a string if the customer exists, otherwise None
      if customer_id == 1:
        return "Alice"
      return None

# Define a sample customer and coffee before creating the order
sample_customer = Customer("Sample Customer")
from lib.models.coffee import Coffee
sample_coffee = Coffee("Sample Coffee")

order = sample_customer.create_order(sample_coffee, 4.99)