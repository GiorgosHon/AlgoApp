from product import Product
from inventory import Inventory
from starting_balance_window import StartingBalanceWindow
from stock_input_window import StockInputWindow
from algo_tab_window import AlgoTabWindow



class AlgoApp:

    def __init__(self):
        self.inventory = Inventory()
        self._initialize_products()
        self.start()

    def _initialize_products(self):
        """Initialize default products"""
        defaultProducts = [
            ("Καφές", 1),
            ("Φραπές", 0.5),
            ("Hell", 1),
            ("Fanta", 1),
            ("Coca Cola", 1),
            ("Sprite", 1),
            ("Μπύρα Μικρή", 1),
            ("Μπύρα Αλφα", 2),
            ("Μπύρα Fix", 2),
            ("Ποτό", 3),
            ("Σφηνάκι", 1),
            ("Κρουασάν", 0.5)
        ]

        for name, price in defaultProducts:
            product = Product(name, price)
            self.inventory.add_product(product)

    def start(self):
        """Start the application flow"""
        balance_window = StartingBalanceWindow(self._on_balance_complete)
        balance_window.show()

    def _on_balance_complete(self, balance):
        """Handle balance entry completion"""
        self.inventory.set_starting_balance(balance)
        entry_window = StockInputWindow(
            self.inventory.get_products(),
            self._on_products_complete
        )
        entry_window.show()

    def _on_products_complete(self):
        """Handle product entry completion and show main window"""
        summary_window = AlgoTabWindow(self.inventory)
        summary_window.show()


if __name__ == "__main__":
    app = AlgoApp()