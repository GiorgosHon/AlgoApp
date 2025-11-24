class Inventory:
    
    def __init__(self):
        self.products = []
        self.starting_balance = 0
    
    def set_starting_balance(self, balance):
        """Set the starting balance"""
        self.starting_balance = balance
    
    def add_product(self, product):
        """Add a product to inventory"""
        self.products.append(product)

    def add_to_total_inventory_value(self):
        pass
    
    def get_total_inventory_value(self):
        """Calculate total value of all products in stock"""
        return sum(product.get_total_value() for product in self.products)
    
    def get_products(self):
        """Return list of all products"""
        return self.products