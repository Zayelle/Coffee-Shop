from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from lib.models.customer import Customer
    from lib.models.coffee import Coffee

class Order:
    def __init__(self, customer: Customer, coffee: Coffee, price: float):
        if not isinstance(price, (int, float)):
            raise TypeError("Price must be a number.")
        if price < 1.0:  # Minimum price validation
            raise ValueError("Price must be at least 1.0.")
        if price > 10.0:  # Maximum price validation
            raise ValueError("Price must not exceed 10.0.")
        self._price = float(price)

        self._customer = None
        self._coffee = None
        self.customer = customer
        self.coffee = coffee

    @property
    def price(self) -> float:
        """Get the price (read-only)"""
        return self._price

    @property
    def customer(self) -> 'Customer':
        """Get associated customer"""
        return self._customer

    @customer.setter
    def customer(self, value: 'Customer'):
        """Set customer with type validation"""
        from lib.models.customer import Customer  # Import here to avoid circular imports
        if not isinstance(value, Customer):
            raise TypeError("Invalid customer")
        
        # Remove the order from the old customer's orders list
        if self._customer is not None:
            self._customer._orders.remove(self)
        
        # Add the order to the new customer's orders list
        value._orders.append(self)
        self._customer = value

    @property
    def coffee(self) -> Coffee:
        """Get associated coffee"""
        return self._coffee

    @coffee.setter
    def coffee(self, value: 'Coffee'):
        """Set coffee with type validation"""
        from lib.models.coffee import Coffee  # Import here to avoid circular imports
        if not isinstance(value, Coffee):
            raise TypeError("Invalid coffee")
        
        # Remove the order from the old coffee's orders list
        if self._coffee is not None:
            self._coffee._orders.remove(self)
        
        # Add the order to the new coffee's orders list
        value._orders.append(self)
        self._coffee = value

    def __repr__(self):
        return f"<Order customer={self.customer.name} coffee={self.coffee.name} price={self.price}>"