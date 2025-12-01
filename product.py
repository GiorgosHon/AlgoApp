class Product:
    def __init__(self, name, price, quantity=0):
        self.name = name
        self.price = price
        self.quantity = quantity

    def set_quantity(self, number):
        self.quantity = number

    def get_quantity(self):
        return self.quantity

    def get_price(self):
        return self.price

    def get_name(self):
        return self.name

    def sell_product(self):
        self.quantity -= 1

    def buy_product(self):
        self.quantity += 1
    
    def __str__(self):
        return f"{self.name} : {self.price:.2f} X {self.quantity}"