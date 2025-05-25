import pytest
from decimal import Decimal
from lib.models.customer import Customer
from lib.models.coffee import Coffee
from lib.models.order import Order

@pytest.fixture
def sample_customer():
    """Fixture providing a basic Customer instance"""
    return Customer("Alice")

@pytest.fixture
def sample_coffee():
    """Fixture providing a basic Coffee instance"""
    return Coffee("Espresso")

class TestCustomer:
    """Test suite for Customer class functionality"""

    def test_initialization(self):
        """Test customer creation with valid name"""
        customer = Customer("Bob")
        assert customer.name == "Bob"
        assert len(customer.orders()) == 0

    @pytest.mark.parametrize("name,expected_error", [
        (123, TypeError),          # Not a string
        ("", ValueError),          # Too short
        ("A"*16, ValueError),     # Too long
        ("   ", ValueError),       # Whitespace only
        (None, TypeError)          # None value
    ])
    def test_name_validation(self, name, expected_error):
        """Test customer name validation"""
        with pytest.raises(expected_error):
            Customer(name)

    class TestCustomerMostAficionado:
        def test_no_orders_returns_none(self):
            """Test returns None when no orders exist for the coffee"""
            coffee = Coffee("Kopi Luwak")
            assert Customer.most_aficionado(coffee) is None

        def test_single_customer_single_order(self):
            """Test with one customer and one order"""
            coffee = Coffee("Espresso")
            customer = Customer("Alice")
            customer.create_order(coffee, 4.50)
            
            assert Customer.most_aficionado(coffee) == customer

        def test_multiple_customers_multiple_orders(self):
            """Test with multiple customers and orders"""
            coffee = Coffee("Latte")
            
            # Customer 1 - total spent: 15.50
            alice = Customer("Alice")
            alice.create_order(coffee, 5.00)
            alice.create_order(coffee, 5.25)
            alice.create_order(coffee, 5.25)
            
            # Customer 2 - total spent: 16.00
            bob = Customer("Bob")
            bob.create_order(coffee, 4.00)
            bob.create_order(coffee, 6.00)
            bob.create_order(coffee, 6.00)
            
            # Customer 3 - total spent: 10.00 (on different coffee)
            charlie = Customer("Charlie")
            charlie.create_order(Coffee("Mocha"), 10.00)
            
            assert Customer.most_aficionado(coffee) == bob

        def test_tie_returns_first_max(self):
            """Test returns first customer when there's a tie"""
            coffee = Coffee("Cappuccino")
            
            alice = Customer("Alice")
            alice.create_order(coffee, 5.00)
            
            bob = Customer("Bob")
            bob.create_order(coffee, 5.00)
            
            # Should return Alice since she was first
            assert Customer.most_aficionado(coffee) == alice

        def test_decimal_precision(self):
            """Test handles decimal precision correctly"""
            coffee = Coffee("Macchiato")
            
            alice = Customer("Alice")
            alice.create_order(coffee, 3.33)
            alice.create_order(coffee, 3.33)
            alice.create_order(coffee, 3.34)
            
            bob = Customer("Bob")
            bob.create_order(coffee, 10.00)
            
            assert Customer.most_aficionado(coffee) == alice

        def test_create_order(self, sample_customer, sample_coffee):
            """Test order creation through customer"""
            initial_order_count = len(sample_customer.orders())
            order = sample_customer.create_order(sample_coffee, 4.99)
            
            assert len(sample_customer.orders()) == initial_order_count + 1
            assert order in sample_customer.orders()
            assert order.price == 4.99
            assert order.coffee == sample_coffee
            assert order.customer == sample_customer

        def test_coffees_unique(self, sample_customer):
            """Test customer's coffee list contains unique items"""
            coffee1 = Coffee("Latte")
            coffee2 = Coffee("Latte")  # Same name, different instance
            coffee3 = Coffee("Cappuccino")
            
            sample_customer.create_order(coffee1, 3.50)
            sample_customer.create_order(coffee2, 3.50)
            sample_customer.create_order(coffee3, 4.00)
            
            assert len(sample_customer.coffees()) == 2  # Unique coffees
            assert {c.name for c in sample_customer.coffees()} == {"Latte", "Cappuccino"}

        def test_multiple_orders(self, sample_customer, sample_coffee):
            """Test handling multiple orders"""
            # Get initial count inside the test method
            initial_count = len(sample_customer.orders())
            
            for i in range(1, 6):
                sample_customer.create_order(sample_coffee, float(i))
            
            assert len(sample_customer.orders()) == initial_count + 5
            assert all(isinstance(o, Order) for o in sample_customer.orders())
            assert sum(o.price for o in sample_customer.orders()) == 15.0

        def test_relationship_integrity(self, sample_customer, sample_coffee):
            """Test order properly updates both customer and coffee"""
            order = sample_customer.create_order(sample_coffee, 5.99)
            
            # Verify customer side
            assert order in sample_customer.orders()
            assert sample_coffee in sample_customer.coffees()
            
            # Verify coffee side
            assert order in sample_coffee.orders()
            assert sample_customer in sample_coffee.customers()

        def test_order_immutability(self, sample_customer, sample_coffee):
            """Test orders list cannot be modified directly"""
            initial_count = len(sample_customer.orders())
            sample_customer.create_order(sample_coffee, 4.50)
            
            orders = sample_customer.orders()  # Get a copy
            orders.append("invalid")  # Try to modify the copy
            
            # Original should remain unchanged
            assert len(sample_customer.orders()) == initial_count + 1
            assert all(isinstance(o, Order) for o in sample_customer.orders())