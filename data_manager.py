import json
import os
from datetime import datetime


class DataManager:
    """Manages persistent settings for the AlgoTab application"""

    def __init__(self):
        # Get a user's home directory
        user_home = os.path.expanduser("~")

        # Create a settings directory
        self.data_dir = os.path.join(user_home, "Documents", "AlgoTab_Data")
        self.data_file = os.path.join(self.data_dir, "data.json")

        self.products = {
            "Hell": 0,
            "Fanta": 0,
            "Coca Cola": 0,
            "Sprite": 0,
            "Μπύρα Μικρή": 0,
            "Μπύρα Αλφα": 0,
            "Μπύρα Fix": 0,
            "Κρουασαν": 0
        }

        # Ensure directory exists
        os.makedirs(self.data_dir, exist_ok=True)

        # Load or create settings
        self.data = self._load_data()

    def data_exists(self):
        return os.path.exists(self.data_file)

    def _load_data(self):
        """Load settings from the file or return defaults"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading settings: {e}")
                return self._default_settings()
        else:
            return self._default_settings()

    def _default_settings(self):
        """Return default settings"""
        saved_info = dict()
        saved_info["current_balance"] = 0
        for product, value in self.products.items():
            saved_info[product] = value

        saved_info["last_updated"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return saved_info

    def save_settings(self):
        """Save current settings to a file"""
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, indent=4, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error saving settings: {e}")
            return False

    def get_current_balance(self):
        """Get the saved current balance"""
        return self.data.get("current_balance", 0.0)

    def set_current_balance(self, balance):
        """Set and save the current balance"""
        self.data["current_balance"] = balance
        self.data["last_updated"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return self.save_settings()

    def set_products(self, products):
        for product in products:
            self.data[product.get_name()] = product.get_quantity()
        return self.save_settings()

    def get_products(self):
        ans = dict()
        try:
            if self.data_exists():
                """Get the saved products"""
                for product in self.products.keys():
                    ans[product] = self.data[product]
        except KeyError as k:
            print(f"Error getting products: {k}")
        return ans

    def get_time(self):
        """Get the saved time"""
        return self.data["last_updated"]