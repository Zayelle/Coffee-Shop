from customer import Customer
from coffee import Coffee

if __name__ == '__main__':
    alice = Customer("Alice")
    bob = Customer("Bob")

    latte = Coffee("Latte")
    mocha = Coffee("Mocha")

    alice.create_order(latte, 4.5)
    alice.create_order(mocha, 5.0)
    bob.create_order(latte, 3.5)

    print("Alice's Coffees:", [coffee.name for coffee in alice.coffees()])
    print("Latte Average Price:", latte.average_price())
    print("Latte Total Orders:", latte.num_orders())