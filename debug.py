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
    except Exception as e:
        print_test_result(f"Customer creation failed: {e}", False)
        return False

    # Invalid cases
    test_cases = [
        (123, TypeError, "non-string name"),
        ("", ValueError, "too-short name"),
        ("ThisNameIsWayTooLongForACustomer", ValueError, "too-long name"),
        ("   ", ValueError, "whitespace-only name")
    ]

    for value, exc_type, description in test_cases:
        try:
            Customer(value)
            print_test_result(f"Failed to catch {description}", False)
        except exc_type:
            print_test_result(f"Caught {description}", True)
        except Exception as e:
            print_test_result(f"Wrong error for {description}: {type(e).__name__}", False)

    return True

def test_coffee_validation():
    """Test Coffee class validation rules"""
    print("\n=== Testing Coffee Validation ===")
    
    try:
        coffee = Coffee("Latte")
        print_test_result(f"Created coffee: {coffee.name}", True)
    except Exception as e:
        print_test_result(f"Coffee creation failed: {e}", False)
        return False

    # Test immutability
    try:
        coffee.name = "NewName"
        print_test_result("Failed to enforce immutable coffee name", False)
    except AttributeError:
        print_test_result("Coffee name is immutable", True)
    except Exception as e:
        print_test_result(f"Wrong error for name change: {type(e).__name__}", False)

    # Invalid cases
    test_cases = [
        (123, TypeError, "non-string name"),
        ("A", ValueError, "too-short name"),
        ("   ", ValueError, "whitespace-only name")
    ]

    for value, exc_type, description in test_cases:
        try:
            Coffee(value)
            print_test_result(f"Failed to catch {description}", False)
        except exc_type:
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

    # Price validation
    test_cases = [
        ("five", TypeError, "non-float price"),
        (0.5, ValueError, "too-low price"),
        (15.0, ValueError, "too-high price"),
        (5, TypeError, "integer instead of float")
    ]

    for value, exc_type, description in test_cases:
        try:
            Order(customer, coffee, value)
            print_test_result(f"Failed to catch {description}", False)
        except exc_type:
            print_test_result(f"Caught {description}", True)
        except Exception as e:
            print_test_result(f"Wrong error for {description}: {type(e).__name__}", False)

    # Test immutability
    try:
        order.price = 5.0
        print_test_result("Failed to enforce immutable price", False)
    except AttributeError:
        print_test_result("Order price is immutable", True)
    except Exception as e:
        print_test_result(f"Wrong error for price change: {type(e).__name__}", False)

    return True

def test_relationships():
    """Test object relationships and aggregates"""
    print("\n=== Testing Relationships ===")
    
    try:
        customer = Customer("Charlie")
        coffee1 = Coffee("Americano")
        coffee2 = Coffee("Mocha")
        
        # Create orders
        orders = [
            Order(customer, coffee1, 3.0),
            Order(customer, coffee1, 3.5),
            Order(customer, coffee2, 4.0)
        ]
        
        # Test relationships
        print_test_result(f"Customer has {len(customer.orders())} orders (expected: 3)", 
                        len(customer.orders()) == 3)
        print_test_result(f"Customer ordered {len(customer.coffees())} unique coffees (expected: 2)", 
                        len(customer.coffees()) == 2)
        
        # Test coffee statistics
        print_test_result(f"{coffee1.name} has {coffee1.num_orders()} orders (expected: 2)", 
                        coffee1.num_orders() == 2)
        print_test_result(f"{coffee1.name} average price: ${coffee1.average_price():.2f} (expected: 3.25)", 
                        abs(coffee1.average_price() - 3.25) < 0.01)
        print_test_result(f"{coffee2.name} has {coffee2.num_orders()} orders (expected: 1)", 
                        coffee2.num_orders() == 1)
        
        # Test create_order method
        new_order = customer.create_order(coffee2, 4.5)
        print_test_result(f"Created order via method: ${new_order.price}", True)
        print_test_result(f"{coffee2.name} now has {coffee2.num_orders()} orders (expected: 2)", 
                        coffee2.num_orders() == 2)
        
        return True
    except Exception as e:
        print_test_result(f"Relationship testing failed: {e}", False)
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
    
    print("\nDebugging complete.")

if __name__ == "__main__":
    main()