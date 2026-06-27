import re

# ----------------------------
# PRODUCT CLASS
# ----------------------------
class Product:
    def __init__(self, name, price, quantity, discount=0, stock=0):
        self.name = self.validate_name(name)
        self.price = self.validate_price(price)
        self.quantity = self.validate_quantity(quantity)
        self.discount = self.validate_discount(discount)
        self.stock = stock  

    def validate_name(self, name):

     if not isinstance(name, str):
        raise ValueError("Invalid product name.")

     name = name.strip()

     if len(name) < 2:
        raise ValueError("Invalid product name.")
     return name

    def validate_price(self, price):
        if not isinstance(price, (int, float)) or price <= 0:
            raise ValueError("Invalid price.")
        return price

    def validate_quantity(self, quantity):
        if not isinstance(quantity, int) or quantity <= 0:
            raise ValueError("Invalid quantity.")
        return quantity

    def validate_discount(self, discount):
        if not isinstance(discount, (int, float)) or not (0 <= discount <= 100):
            raise ValueError("Invalid discount.")
        return discount

    def get_total_price(self):
        total = self.price * self.quantity
        discount_amount = total * (self.discount / 100)
        return round(total - discount_amount, 2)


# ----------------------------
# CART CLASS
# ----------------------------
class Cart:
    def __init__(self):
        self.products = []
    def add_product(self, product, store_products):
     if not isinstance(product, Product):
        raise ValueError("Only Product objects allowed.")

     for item in store_products:
            if item.name.lower() == product.name.lower():
            # check existing product in cart first
             for p in self.products:
                if p.name.lower() == product.name.lower():

                 if p.quantity + product.quantity > item.stock:
                        print(f"Only {item.stock} items available in stock!")
                        return

                p.quantity += product.quantity
                item.stock -= product.quantity
                print(f"{product.name} quantity updated in cart.")
                return

            # new product stock check
            if product.quantity > item.stock:
                print(f"Only {item.stock} items available in stock!")
                return

            item.stock -= product.quantity
            self.products.append(product)
            print(f"{product.name} added to cart.")
            return

    def remove_product(self, product_name):
        if not self.products:
            print("Cart is empty! Nothing to remove.")
            return

        for product in self.products:
         if product.name.lower() == product_name.lower():
            self.products.remove(product)
            print(f"{product.name} removed from cart.")
            return

        print("Product not found in cart.") 

    def calculate_total(self):
        return sum(p.get_total_price() for p in self.products)

    def show_cart(self):
        if not self.products:
            print("Cart is empty.")
            return

        print("\n--- CART ITEMS ---")
        for p in self.products:
            print(f"{p.name} | Qty: {p.quantity} | Price: {p.price} | Discount: {p.discount}%")

    def generate_invoice(self):
        print("\n===== INVOICE =====")
        if not self.products:
            print("Cart is empty! Add products first.")
            return
        total_qty = sum(p.quantity for p in self.products)
        total_price = self.calculate_total()

        for p in self.products:
            print(f"{p.name} - Qty: {p.quantity} - Final Price: {p.get_total_price()}")

        print("\n-------------------")
        print(f"Total Quantity: {total_qty}")
        print(f"Total Bill: {total_price}")
        print("===================\n")


# ----------------------------
# CUSTOMER CLASS
# ----------------------------
class Customer:
    def __init__(self, name, email):
        self.name = self.validate_name(name)
        self.email = self.validate_email(email)
        self.cart = Cart()  # Each customer has their own cart

    def validate_name(self, name):
      if not isinstance(name, str) or len(name.strip()) < 2:
        raise ValueError("Invalid customer name.")
      if not name.replace(" ", "").isalpha():
        raise ValueError("Name must contain only letters and spaces.")
      return name.strip()

    def validate_email(self, email):
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        if not re.match(pattern, email):
            raise ValueError("Invalid email format.")
        return email           
       
# ----------------------------
# MAIN PROGRAM
# ----------------------------
def main():
    print("===== WELCOME TO ONLINE SHOP =====")

    # Customer input with validation
    while True:
        try:
            name = input("Enter your name: ")
            email = input("Enter your email: ")
            customer = Customer(name, email)
            break
        except ValueError as e:
            print("Error:", e)

    print(f"\nWelcome {customer.name}! Happy Shopping 🎉")

    # Product list (fixed store items)
    store_products = [
        Product("Laptop", 100000, 1, 10,8),
        Product("Phone", 50000, 1, 5,5),
        Product("Headphones", 1000, 1, 15,20),
        Product("Mouse", 1500, 1, 20,7)
    ]

    while True:
        print("\n--- AVAILABLE PRODUCTS ---")
        for i, p in enumerate(store_products, 1):
            print(f"{i}. {p.name} | Price: {p.price} | Discount: {p.discount}%|  Stock: {p.stock}|")

        print("\nOptions:")
        print("1. Add product to cart")
        print("2. Remove product from cart")
        print("3. Show cart")
        print("4. Generate invoice")
        print("5. Exit")

        choice = input("Enter choice: ").strip()
        print("Choice received =", choice)

        if choice == "1":
         while True:
            try:
                index = int(input("Enter product number from 1 to 4: ")) - 1
                quantity = int(input("Enter quantity: "))

                if quantity <= 0:
                 print("Quantity must be greater than 0.")
                continue

                selected = store_products[index]
                product = Product(selected.name, selected.price, quantity, selected.discount, selected.stock)
                customer.cart.add_product(product, store_products)
                break # Exit the loop after successful addition

            except (IndexError, ValueError):
                print("Invalid input!")

        elif choice == "2":
            name = input("Enter product name to remove: ")
            customer.cart.remove_product(name)

        elif choice == "3":
            customer.cart.show_cart()

        elif choice == "4":
            customer.cart.generate_invoice()

        elif choice == "5":
            print("\nThanks for visiting the website ")
            print("Goodbye!")
            break

        else:
            print("Invalid choice!")


# Run program
if __name__ == "__main__":
    main()