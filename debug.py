from customer import Customer
from coffee import Coffee
from order import Order

def main():
    print("=== Coffee Shop Debugging ===")
    
    # Test Customer initialization and properties
    try:
        customer1 = Customer("Alice")
        print(f"✅ Created customer: {customer1.name}")
        
        # Test invalid names
        try:
            customer_bad = Customer(123)
            print("❌ Failed to catch non-string name")
        except TypeError:
            print("✅ Caught non-string name")
        
        try:
            customer_bad = Customer("")
            print("❌ Failed to catch too-short name")
        except ValueError:
            print("✅ Caught too-short name")
            
        try:
            customer_bad = Customer("ThisNameIsWayTooLongForACustomer")
            print("❌ Failed to catch too-long name")
        except ValueError:
            print("✅ Caught too-long name")
            
    except Exception as e:
        print(f"❌ Customer initialization failed: {e}")

    # Test Coffee initialization and properties
    try:
        coffee1 = Coffee("Latte")
        print(f"✅ Created coffee: {coffee1.name}")
        
        # Test invalid names
        try:
            coffee_bad = Coffee(123)
            print("❌ Failed to catch non-string coffee name")
        except TypeError:
            print("✅ Caught non-string coffee name")
        
        try:
            coffee_bad = Coffee("A")
            print("❌ Failed to catch too-short coffee name")
        except ValueError:
            print("✅ Caught too-short coffee name")
            
        # Test immutability
        try:
            coffee1.name = "NewName"
            print("❌ Failed to enforce immutable coffee name")
        except AttributeError:
            print("✅ Coffee name is immutable")
            
    except Exception as e:
        print(f"❌ Coffee initialization failed: {e}")

    # Test Order creation and relationships
    try:
        customer2 = Customer("Bob")
        coffee2 = Coffee("Cappuccino")
        
        order1 = Order(customer2, coffee2, 4.5)
        print(f"✅ Created order: ${order1.price} {order1.coffee.name} for {order1.customer.name}")
        
        # Test invalid prices
        try:
            Order(customer2, coffee2, "five")
            print("❌ Failed to catch non-float price")
        except TypeError:
            print("✅ Caught non-float price")
            
        try:
            Order(customer2, coffee2, 0.5)
            print("❌ Failed to catch too-low price")
        except ValueError:
            print("✅ Caught too-low price")
            
        try:
            Order(customer2, coffee2, 15.0)
            print("❌ Failed to catch too-high price")
        except ValueError:
            print("✅ Caught too-high price")
            
        # Test price immutability
        try:
            order1.price = 5.0
            print("❌ Failed to enforce immutable price")
        except AttributeError:
            print("✅ Order price is immutable")
            
    except Exception as e:
        print(f"❌ Order creation failed: {e}")

    # Test relationships and aggregates
    try:
        customer3 = Customer("Charlie")
        coffee3 = Coffee("Americano")
        coffee4 = Coffee("Mocha")
        
        # Create multiple orders
        order2 = Order(customer3, coffee3, 3.0)
        order3 = Order(customer3, coffee3, 3.5)
        order4 = Order(customer3, coffee4, 4.0)
        
        # Test customer-coffee relationships
        print(f"✅ Customer orders: {len(customer3.orders())} (expected: 3)")
        print(f"✅ Unique coffees: {len(customer3.coffees())} (expected: 2)")
        
        # Test coffee statistics
        print(f"✅ {coffee3.name} orders: {coffee3.num_orders()} (expected: 2)")
        print(f"✅ {coffee3.name} avg price: ${coffee3.average_price():.2f} (expected: 3.25)")
        print(f"✅ {coffee4.name} orders: {coffee4.num_orders()} (expected: 1)")
        
        # Test create_order method
        new_order = customer3.create_order(coffee4, 4.5)
        print(f"✅ Created order via method: ${new_order.price}")
        print(f"✅ Updated {coffee4.name} orders: {coffee4.num_orders()} (expected: 2)")
        
    except Exception as e:
        print(f"❌ Relationship testing failed: {e}")

if __name__ == "__main__":
    main()