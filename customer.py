from order import Order

class Customer:
    def __init__(self, name):
        self.name = name
        self._orders = []

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if isinstance(value, str) and 1 <= len(value) <= 15:
            self._name = value
        else:
            raise ValueError("Name must be a string between 1 and 15 characters.")

    def orders(self):
        return self._orders.copy()

    def coffees(self):
        return list({order.coffee for order in self._orders})

    def create_order(self, coffee, price):
        new_order = Order(self, coffee, price)
        self._orders.append(new_order)
        return new_order