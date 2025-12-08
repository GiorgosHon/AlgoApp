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
        defaultProducts = {
            "Καφές": 1,
            "Φραπές": 0.5,
            "Hell": 1,
            "Fanta": 1,
            "Coca Cola": 1,
            "Sprite": 1,
            "Μπύρα Μικρή": 1,
            "Μπύρα Μεσαία": 1.5,
            "Μπύρα Αλφα": 2,
            "Μπύρα Fix": 2,
            "Ποτό": 3,
            "Σφηνάκι": 1,
            "Κρουασαν": 0.5
        }

        if self.data_manager.data_exists():
            product_quantities = self.data_manager.get_products()
            product_quantities = self.data_manager.get_products()
            for product_name, product_price in defaultProducts.items():
                if product_name in product_quantities:
                    product_temp = Product(product_name, product_price, product_quantities[product_name])
                    self.inventory.add_product(product_temp)
                else:
                    product_temp = Product(product_name, product_price)
                    self.inventory.add_product(product_temp)
        else:
            for product_name, product_price in defaultProducts.items():
                product = Product(product_name, product_price)
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
            geometry="450x300"
        )

    def _on_balance_complete(self, balance):
        """Handle balance entry completion"""
        self.inventory.set_starting_balance(balance)
        self._switch_frame(
            StockInputWindow,
            self.inventory.get_products(),
            self.data_manager,
            self._on_products_complete,
            geometry="600x600"
        )

    def _on_products_complete(self):
        """Handle product entry completion and show main window"""
        self._switch_frame(
            AlgoTabWindow, 
            self.inventory, 
            self.data_manager,
            on_update_click=self._open_stock_update, # Pass the new callback here
            geometry="920x700"
        )

    def _open_stock_update(self):
        """Switch back to stock input window to update quantities"""
        self._switch_frame(
            StockInputWindow,
            self.inventory.get_products(),
            self.data_manager,
            self._on_products_complete, # When done, go back to main tab
            geometry="600x600"
        )

if __name__ == "__main__":
    app = AlgoApp()