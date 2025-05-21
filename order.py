from customer import Customer
from coffee import Coffee

class Order:
    def __init__(self, customer, coffee, price):
        self.customer = customer
        self.coffee = coffee
        self.price = price  # Using property setter
        
        # Add this order to the customer's and coffee's lists
        customer._orders.append(self)
        coffee._orders.append(self)

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        if not isinstance(value, float):
            raise TypeError("Price must be a float")
        if not 1.0 <= value <= 10.0:
            raise ValueError("Price must be between 1.0 and 10.0")
        if hasattr(self, '_price'):
            raise AttributeError("Price cannot be changed after initialization")
        self._price = value

    @property
    def customer(self):
        return self._customer

    @customer.setter
    def customer(self, value):
        if not isinstance(value, Customer):
            raise TypeError("Customer must be an instance of Customer class")
        self._customer = value

    @property
    def coffee(self):
        return self._coffee

    @coffee.setter
    def coffee(self, value):
        if not isinstance(value, Coffee):
            raise TypeError("Coffee must be an instance of Coffee class")
        self._coffee = value