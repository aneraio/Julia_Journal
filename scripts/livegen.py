import os
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivy.core.window import Window
import math
import time

class LiveGenApp(App):
    def build(self):
        # Load the custom font
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.abspath(os.path.join(current_dir, ".."))
        custom_font_path = os.path.join(project_root, "admin", "assets", "century-gothic", "CenturyGothic.ttf")

        try:
            from kivy.core.text import LabelBase
            LabelBase.register(name='CenturyGothic', fn_regular=custom_font_path)

            # Set up the window for transparency
            Window.clearcolor = (0, 0, 0, 0)  # Fully transparent background
            Window.borderless = True

            # Create the main layout
            layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
            layout.canvas.before.clear()

            # Create the label with the custom font and transparent background
            self.label = Label(text="Live Gen: 0", font_name='CenturyGothic', font_size='20sp', color=(1, 1, 1, 1), markup=True)
            layout.add_widget(self.label)

            # Set up timer
            Clock.schedule_interval(self.update_gen, 0.001)  # Update every millisecond

            return layout
        except Exception as e:
            # Print an error message if there's an issue with font loading
            print(f"Font loading error: {e}")

    def ts_to_gen(self, ts):
        gen = math.pow(1.0002, (ts - 1675084800) / 3300)
        return gen

    def update_gen(self, dt):
        ts = time.time()
        gen = self.ts_to_gen(ts)
        formatted_gen = "{:.15f}".format(gen)  # Format with 15 decimal places
        self.label.text = f"[color=ffffff]{formatted_gen}[/color]"

if __name__ == '__main__':
    LiveGenApp().run()