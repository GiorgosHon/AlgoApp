class Product:
    def __init__(self, name, price):
        self.name = name
        self.price = price
        self.quantity = 0

    def set_quantity(self, number):
        self.quantity = number

    def sell_product(self):
        self.quantity -= 1

    def buy_product(self):
        self.quantity += 1

    def get_total_value(self):
        return self.quantity * self.price
    
    def __str__(self):
        return f"{self.name} - {self.price:.2f} X {self.quantity}"