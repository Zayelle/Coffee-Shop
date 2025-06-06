class Coffee:
    def __init__(self, name: str):
        """Initialize a Coffee with name and empty orders list"""
        if not isinstance(name, str) or len(name.strip()) < 3:
            raise ValueError("Coffee name must be a string with at least 3 characters.")
        self._name = name.strip()
        self._orders = []

    @property
    def name(self) -> str:
        """Get coffee name (read-only)"""
        return self._name

    def orders(self) -> list:
        """Return list of all orders for this coffee"""
        return self._orders.copy()  # Return copy to prevent external modification

    def customers(self) -> list:
        """Return unique list of customers who ordered this coffee"""
        from lib.models.customer import Customer  # Prevent circular import
        return list({order.customer for order in self._orders})

    def num_orders(self) -> int:
        """Return total number of orders for this coffee"""
        return len(self._orders)

    def average_price(self) -> float:
        """Calculate average price of orders for this coffee"""
        if not self._orders:
            return 0.0
        total = sum(order.price for order in self._orders)
        return round(total / len(self._orders), 2)

    def __repr__(self):
        return f"<Coffee name='{self.name}'>"