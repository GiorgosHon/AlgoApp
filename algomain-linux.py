import tkinter as tk
from product import Product
from inventory import Inventory
from starting_balance_window import StartingBalanceWindow
from stock_input_window import StockInputWindow
from algo_tab_window import AlgoTabWindow
from data_manager import DataManager


class AlgoApp:

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("AlgoApp")
        self.root.configure(background="black")
        self.root.geometry("700x650") # Set a default size if needed

        self.data_manager = DataManager()
        self.inventory = Inventory()
        self._initialize_products()

        self.start()

        self.root.mainloop()

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

    def _switch_frame(self, frame_class, *args, **kwargs):
        """Helper to destroy current frame and load new one"""
        # Extract geometry from kwargs if it exists, so it doesn't get passed to the frame
        geometry = kwargs.pop('geometry', None)

        # Clear old frames
        for widget in self.root.winfo_children():
            widget.destroy()

        if geometry:
            self.root.geometry(geometry)

        new_frame = frame_class(self.root, *args, **kwargs)
        new_frame.pack(fill="both", expand=True)
        return new_frame

    def start(self):
        # Get saved balance
        saved_balance = self.data_manager.get_current_balance()

        # Switch to the frame instead of creating a new window
        self._switch_frame(
            StartingBalanceWindow,
            self._on_balance_complete,
            saved_balance,
            geometry="350x200"
        )

    def _on_balance_complete(self, balance):
        """Handle balance entry completion"""
        self.inventory.set_starting_balance(balance)
        stocked_products = self.data_manager.get_products()
        self._switch_frame(
            StockInputWindow,
            self.inventory.get_products(),
            stocked_products,
            self.data_manager,
            self._on_products_complete,
            geometry="600x650"
        )

    def _on_products_complete(self):
        self._switch_frame(
            AlgoTabWindow,
            self.inventory,
            self.data_manager,
            geometry="920x700"
        )


if __name__ == "__main__":
    app = AlgoApp()