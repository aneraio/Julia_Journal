import json
import os

class Setup:
    def __init__(self):
        self.settings_dir = os.path.join(os.path.dirname(__file__), "admin", "settings", "journal")
        self.settings_file = os.path.join(self.settings_dir, "journal_settings.json")
        self.load_settings()

    def load_settings(self):
        if not os.path.exists(self.settings_dir):
            os.makedirs(self.settings_dir)
            print(f"Created settings directory at: {self.settings_dir}")

        if not os.path.exists(self.settings_file):
            self.show_live_gen = False
            self.save_settings()  # Create the file with default settings
            print("Settings file created with live generation turned off by default.")
        else:
            with open(self.settings_file, "r") as f:
                settings_data = json.load(f)
                self.show_live_gen = settings_data.get("show_live_gen", False)
            print(f"Settings loaded. Live generation is {'enabled' if self.show_live_gen else 'disabled'}.")

    def save_settings(self):
        settings_data = {
            "show_live_gen": self.show_live_gen
        }
        with open(self.settings_file, "w") as f:
            json.dump(settings_data, f)
        print(f"Settings saved. Live generation is now {'enabled' if self.show_live_gen else 'disabled'}.")

    def is_live_gen_enabled(self):
        return self.show_live_gen

    def set_live_gen_enabled(self, value):
        self.show_live_gen = value
        self.save_settings()
        print(f"Live generation has been {'enabled' if value else 'disabled'}.")