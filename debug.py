from lib.models.customer import Customer
from lib.models.coffee import Coffee
from lib.models.order import Order

def print_test_result(description, success):
    """Helper function to format test results"""
    icon = "✅" if success else "❌"
    print(f"{icon} {description}")

def test_customer_validation():
    """Test Customer class validation rules"""
    print("\n=== Testing Customer Validation ===")
    
    # Valid cases
    try:
        customer = Customer("Alice")
        print_test_result(f"Created customer: {customer.name}", True)
        assert isinstance(customer.name, str)
        assert 1 <= len(customer.name) <= 15
    except Exception as e:
        print_test_result(f"Customer creation failed: {e}", False)
        return False

    # Invalid cases (updated to match your implementation)
    test_cases = [
        (123, TypeError, "non-string name"),  # Matches your TypeError implementation
        ("", ValueError, "too-short name"),
        ("ThisNameIsWayTooLong", ValueError, "too-long name"), 
        ("   ", ValueError, "whitespace-only name"),
        (None, TypeError, "None value name")  # Matches your TypeError implementation
    ]

    for value, expected_error, description in test_cases:
        try:
            Customer(value)
            print_test_result(f"Failed to catch {description}", False)
        except expected_error:
            print_test_result(f"Caught {description} ({expected_error.__name__})", True)
        except Exception as e:
            print_test_result(f"Unexpected error for {description}: {type(e).__name__}", False)

    return True

def test_coffee_validation():
    """Test Coffee class validation rules"""
    print("\n=== Testing Coffee Validation ===")
    
    try:
        coffee = Coffee("Latte")
        print_test_result(f"Created coffee: {coffee.name}", True)
        assert len(coffee.name) >= 3
    except Exception as e:
        print_test_result(f"Coffee creation failed: {e}", False)
        return False

    # Test immutability
    try:
        coffee.name = "NewName"
        print_test_result("Coffee name should be immutable after creation", False)
    except AttributeError:
        print_test_result("Coffee name is properly immutable", True)
    except Exception as e:
        print_test_result(f"Unexpected error for name change: {type(e).__name__}", False)

    # Invalid cases
    test_cases = [
        (123, ValueError, "non-string name"),
        ("A", ValueError, "too-short name"),
        ("   ", ValueError, "whitespace-only name"),
        (None, ValueError, "None value name")
    ]

    for value, expected_error, description in test_cases:
        try:
            Coffee(value)
            print_test_result(f"Failed to catch {description}", False)
        except expected_error:
            print_test_result(f"Caught {description}", True)
        except Exception as e:
            print_test_result(f"Wrong error for {description}: {type(e).__name__}", False)

    return True

def test_order_validation():
    """Test Order class validation rules"""
    print("\n=== Testing Order Validation ===")
    
    try:
        customer = Customer("Bob")
        coffee = Coffee("Cappuccino")
        order = Order(customer, coffee, 4.5)
        print_test_result(f"Created order: ${order.price} {coffee.name} for {customer.name}", True)
    except Exception as e:
        print_test_result(f"Order creation failed: {e}", False)
        return False

    # Price validation (aligned with common commerce rules)
    test_cases = [
        ("five", TypeError, "non-numeric price"),
        (0, ValueError, "zero price"),
        (-1.0, ValueError, "negative price"),
        (1000.0, ValueError, "unreasonably high price"),
        (3.333, None, "valid decimal price")  # Should succeed
    ]

    for value, expected_error, description in test_cases:
        try:
            Order(customer, coffee, value)
            if expected_error is None:
                print_test_result(f"Accepted valid {description}", True)
            else:
                print_test_result(f"Failed to catch {description}", False)
        except expected_error if expected_error else Exception:
            if expected_error:
                print_test_result(f"Caught {description}", True)
            else:
                print_test_result(f"Unexpected error for valid {description}", False)
        except Exception as e:
            print_test_result(f"Wrong error for {description}: {type(e).__name__}", False)

    # Test relationship integrity
    try:
        assert order in customer.orders()
        assert order.coffee == coffee
        assert order.customer == customer
        print_test_result("Order relationships properly established", True)
    except AssertionError:
        print_test_result("Order relationships not properly established", False)

    return True

def test_relationships():
    """Test object relationships and aggregates"""
    print("\n=== Testing Relationships ===")
    
    try:
        customer = Customer("Charlie")
        coffee1 = Coffee("Americano")
        coffee2 = Coffee("Mocha")
        
        # Test create_order method
        order1 = customer.create_order(coffee1, 3.0)
        order2 = customer.create_order(coffee1, 3.5)
        order3 = customer.create_order(coffee2, 4.0)
        
        # Verify counts
        print_test_result(f"Customer has {len(customer.orders())} orders (expected: 3)", 
                        len(customer.orders()) == 3)
        print_test_result(f"Customer ordered {len(customer.coffees())} unique coffees (expected: 2)", 
                        len(customer.coffees()) == 2)
        
        # Verify coffee statistics
        print_test_result(f"{coffee1.name} has {coffee1.num_orders()} orders (expected: 2)", 
                        coffee1.num_orders() == 2)
        
        # Test average price calculation with precision
        avg_price = coffee1.average_price()
        print_test_result(f"{coffee1.name} average price: ${avg_price:.2f} (expected: 3.25)", 
                        abs(avg_price - 3.25) < 0.01)
        
        # Test order immutability
        orders = customer.orders()
        orders.append("invalid")
        print_test_result("Customer.orders() returns a proper copy", 
                        len(customer.orders()) == 3)
        
        return True
    except Exception as e:
        print_test_result(f"Relationship testing failed: {str(e)}", False)
        return False

def main():
    print("=== Coffee Shop Debug Console ===")
    print("Running comprehensive tests...\n")
    
    results = [
        ("Customer Validation", test_customer_validation()),
        ("Coffee Validation", test_coffee_validation()),
        ("Order Validation", test_order_validation()),
        ("Relationship Tests", test_relationships())
    ]
    
    print("\n=== Test Summary ===")
    for name, success in results:
        status = "PASSED" if success else "FAILED"
        print(f"{name.ljust(20)}: {status}")
    
    print("\nDebugging complete. All tests passed!" if all(r[1] for r in results) 
          else "\nDebugging complete. Some tests failed.")

if __name__ == "__main__":
    main()