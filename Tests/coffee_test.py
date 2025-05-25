import pytest
from lib.models.coffee import Coffee
from lib.models.order import Order
from lib.models.customer import Customer

class TestCoffee:
    """Test suite for Coffee class functionality"""

    @pytest.fixture
    def sample_coffee(self):
        """Fixture providing a basic Coffee instance"""
        return Coffee("Latte")

    @pytest.fixture
    def sample_customer(self):
        """Fixture providing a basic Customer instance"""
        return Customer("Alice")

    @pytest.fixture
    def sample_order(self, sample_coffee, sample_customer):
        """Fixture providing an Order linking coffee and customer"""
        return Order(sample_customer, sample_coffee, 5.99)

    # ----- Initialization Tests -----
    def test_valid_initialization(self):
        """Test coffee creation with valid name"""
        coffee = Coffee("Americano")
        assert coffee.name == "Americano"
        assert coffee.num_orders() == 0

    def test_invalid_initialization(self):
        """Test coffee creation with invalid names"""
        with pytest.raises(ValueError):
            Coffee("")  # Too short
        
        with pytest.raises(ValueError):
            Coffee(123)  # Wrong type

        with pytest.raises(ValueError):
            Coffee("A")  # Too short

    # ----- Property Tests -----
    def test_name_property(self, sample_coffee):
        """Test name getter/setter"""
        sample_coffee.name = "Mocha"
        assert sample_coffee.name == "Mocha"
        
        with pytest.raises(ValueError):
            sample_coffee.name = 123

    # ----- Order Relationship Tests -----
    def test_order_management(self, sample_coffee, sample_order):
        """Test order relationships are properly tracked"""
        assert len(sample_coffee.orders()) == 1
        assert sample_order in sample_coffee.orders()
        assert sample_coffee.num_orders() == 1

    def test_customer_relationships(self, sample_coffee, sample_customer, sample_order):
        """Test customer relationships through orders"""
        customers = sample_coffee.customers()
        assert len(customers) == 1
        assert sample_customer in customers

    # ----- Statistical Tests -----
    def test_average_price_no_orders(self, sample_coffee):
        """Test average price with no orders"""
        assert sample_coffee.average_price() == 0.0

    def test_average_price_with_orders(self, sample_coffee, sample_customer):
        """Test average price calculation"""
        Order(sample_customer, sample_coffee, 4.50)
        Order(sample_customer, sample_coffee, 5.50)
        
        assert sample_coffee.average_price() == 5.0  # (4.50 + 5.50) / 2
        assert sample_coffee.num_orders() == 2

    def test_average_price_precision(self, sample_coffee, sample_customer):
        """Test rounding of average price"""
        Order(sample_customer, sample_coffee, 3.333)
        Order(sample_customer, sample_coffee, 6.666)
        
        assert sample_coffee.average_price() == 5.0  # Rounded from 4.9995

    # ----- Edge Case Tests -----
    def test_multiple_customers(self, sample_coffee):
        """Test tracking multiple unique customers"""
        customer1 = Customer("Bob")
        customer2 = Customer("Charlie")
        
        Order(customer1, sample_coffee, 4.00)
        Order(customer2, sample_coffee, 5.00)
        
        assert len(sample_coffee.customers()) == 2

    # ----- Fixture Tests -----
    def test_sample_order_fixture(self, sample_order):
        """Test that the sample_order fixture creates a valid Order instance"""
        assert sample_order.customer.name == "Alice"
        assert sample_order.coffee.name == "Latte"
        assert sample_order.price == 5.99