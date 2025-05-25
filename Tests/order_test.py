import pytest
from lib.models.customer import Customer
from lib.models.coffee import Coffee
from lib.models.order import Order

class TestOrder:
    """Test suite for Order class functionality"""

    @pytest.fixture
    def sample_customer(self):
        return Customer("Alice")

    @pytest.fixture
    def sample_coffee(self):
        return Coffee("Espresso")

    @pytest.fixture
    def sample_order(self, sample_customer, sample_coffee):
        return Order(sample_customer, sample_coffee, 5.99)

    # ----- Initialization Tests -----
    def test_valid_initialization(self, sample_customer, sample_coffee):
        order = Order(sample_customer, sample_coffee, 4.99)
        assert order.price == 4.99
        assert order.customer == sample_customer
        assert order.coffee == sample_coffee

    def test_invalid_price_initialization(self, sample_customer, sample_coffee):
        with pytest.raises(TypeError):
            Order(sample_customer, sample_coffee, "5")  # String price
        
        with pytest.raises(ValueError):
            Order(sample_customer, sample_coffee, 0.99)  # Too low

        with pytest.raises(ValueError):
            Order(sample_customer, sample_coffee, 10.01)  # Too high

    # ----- Property Tests -----
    def test_price_immutability(self, sample_order):
        """Test price cannot be modified after initialization"""
        with pytest.raises(AttributeError):
            sample_order.price = 6.99

    def test_customer_assignment(self, sample_order, sample_customer):
        new_customer = Customer("Bob")
        sample_order.customer = new_customer
        assert sample_order.customer == new_customer
        
        with pytest.raises(TypeError):
            sample_order.customer = "Not a customer"

    def test_coffee_assignment(self, sample_order, sample_coffee):
        new_coffee = Coffee("Latte")
        sample_order.coffee = new_coffee
        assert sample_order.coffee == new_coffee
        
        with pytest.raises(TypeError):
            sample_order.coffee = "Not a coffee"

    # ----- Relationship Tests -----
    def test_bidirectional_relationships(self, sample_customer, sample_coffee):
        """Test order properly updates both customer and coffee"""
        order = Order(sample_customer, sample_coffee, 3.50)
        
        # Check customer side
        assert len(sample_customer.orders()) == 1
        assert order in sample_customer.orders()
        assert sample_coffee in sample_customer.coffees()
        
        # Check coffee side
        assert len(sample_coffee.orders()) == 1
        assert order in sample_coffee.orders()
        assert sample_customer in sample_coffee.customers()

    def test_relationship_update(self, sample_order, sample_customer, sample_coffee):
        """Test changing customer/coffee updates relationships"""
        new_customer = Customer("Charlie")
        new_coffee = Coffee("Cappuccino")
        
        sample_order.customer = new_customer
        sample_order.coffee = new_coffee
        
        # Verify old relationships removed
        assert sample_order not in sample_customer.orders()
        assert sample_order not in sample_coffee.orders()
        
        # Verify new relationships established
        assert sample_order in new_customer.orders()
        assert sample_order in new_coffee.orders()

    # ----- Edge Case Tests -----
    def test_price_precision(self, sample_customer, sample_coffee):
        """Test floating point price handling"""
        order = Order(sample_customer, sample_coffee, 3.333333)
        assert order.price == pytest.approx(3.333, 0.001)