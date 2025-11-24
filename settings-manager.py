import json
import os


class SettingsManager:
    """Manages persistent settings for the AlgoTab application"""

    def __init__(self):
        # Get user's home directory
        user_home = os.path.expanduser("~")

        # Create settings directory
        self.settings_dir = os.path.join(user_home, "Documents", "AlgoTab_Data")
        self.settings_file = os.path.join(self.settings_dir, "settings.json")

        # Ensure directory exists
        os.makedirs(self.settings_dir, exist_ok=True)

        # Load or create settings
        self.settings = self._load_settings()

    def _load_settings(self):
        """Load settings from file or return defaults"""
        if os.path.exists(self.settings_file):
            try:
                with open(self.settings_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading settings: {e}")
                return self._default_settings()
        else:
            return self._default_settings()

    def _default_settings(self):
        """Return default settings"""
        return {
            "current_balance": 0.0,
            "last_updated": None
        }

    def save_settings(self):
        """Save current settings to file"""
        try:
            with open(self.settings_file, 'w', encoding='utf-8') as f:
                json.dump(self.settings, f, indent=4, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error saving settings: {e}")
            return False

    def get_current_balance(self):
        """Get the saved current balance"""
        return self.settings.get("current_balance", 0.0)

    def set_current_balance(self, balance):
        """Set and save the current balance"""
        from datetime import datetime
        self.settings["current_balance"] = balance
        self.settings["last_updated"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return self.save_settings()

    def reset_balance(self):
        """Reset balance to 0"""
        self.settings["current_balance"] = 0.0
        return self.save_settings()