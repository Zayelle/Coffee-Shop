# Coffee Shop Models

Python classes representing a coffee shop's customers, coffees, and orders.

## Classes

- **Customer**: Represents a coffee shop customer
  - Has a name (1-15 characters)
  - Can create orders
  - Tracks all orders and unique coffees ordered

- **Coffee**: Represents a coffee type
  - Has a name (3+ characters)
  - Tracks all orders and customers
  - Calculates order statistics

- **Order**: Links customers to coffees
  - Has a price ($1.0-$10.0)
  - Connects one customer to one coffee

## Basic Usage

```python
# Create objects
customer = Customer("Sam")
coffee = Coffee("Espresso")

# Create order
order = Order(customer, coffee, 3.5)

# Get customer's orders
print(customer.orders())

# Get coffee statistics
print(coffee.num_orders())