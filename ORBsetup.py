#ORB Setup

import os
import json
import time
import math
import tkinter as tk
from tkinter import messagebox, font
from PIL import Image, ImageTk
import configparser
from cryptography.fernet import Fernet
import subprocess
import shutil

class ORBSetup:
    def __init__(self, root):
        self.root = root
        self.config = configparser.ConfigParser()
        self.load_key()

        self.setup_ui()



    def setup_ui(self):
        self.root.title("ORB Setup")
        self.root.geometry("1600x900")
        self.root.configure(bg="black")

        self.load_logo()

        frame = tk.Frame(self.root, bg="black", padx=230, pady=30)
        frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        custom_font = font.Font(family="Century Gothic", size=36, weight="normal", slant="roman", underline=0, overstrike=0)
        custom_font_large = font.Font(family="Century Gothic", size=48, weight="normal", slant="roman", underline=0, overstrike=0)

        if self.config.has_section('User'):
            user_name = self.config['User']['Name']
            welcome_label = tk.Label(frame, text=self.add_kerning(f"Hallo, {user_name.capitalize()}. Would you like to create another journal?", spacing=0.5), font=custom_font, fg="white", bg="black", wraplength=1140)
            prompt_label_text = ""
        else:
            welcome_label = tk.Label(frame, text=self.add_kerning("Hallo, I'm Julia, an autonomous cognitive entity.", spacing=0.5), font=custom_font, fg="white", bg="black", wraplength=1140)
            prompt_label_text = "Let's set up your profile first. What's your name?"
        welcome_label.pack(pady=5)

        if prompt_label_text:
            prompt_label = tk.Label(frame, text=self.add_kerning(prompt_label_text, spacing=0.5), font=custom_font, fg="white", bg="black", wraplength=1140)
            prompt_label.pack(pady=5)

        input_frame = tk.Frame(frame, bg="black")
        input_frame.pack(pady=30)

        scroll_orb_image = Image.open("admin/assets/scroll_orb.png")
        scroll_orb_image = scroll_orb_image.resize((33, 43))
        self.scroll_orb_image = ImageTk.PhotoImage(scroll_orb_image)
        self.scroll_orb_label = tk.Label(input_frame, image=self.scroll_orb_image, bg="black")
        self.scroll_orb_label.pack(side=tk.LEFT, padx=(0, 10))

        self.name_entry = tk.Entry(input_frame, font=custom_font_large, fg="white", bg="black", width=20, borderwidth=0, highlightthickness=0, insertbackground="white", justify='left')
        self.name_entry.pack(side=tk.LEFT)

        send_button_image = Image.open("admin/assets/send.png")
        send_button_image = send_button_image.resize((240, 86))
        self.send_button_image = ImageTk.PhotoImage(send_button_image)

        self.submit_button = tk.Label(frame, image=self.send_button_image, borderwidth=0)
        self.submit_button.pack(pady=5)
        self.submit_button.bind('<Button-1>', lambda event: self.save_user_name())
        self.root.bind('<Return>', lambda event: self.save_user_name())

    def load_logo(self):
        logo = Image.open("logo.png")
        width, height = logo.size
        aspect_ratio = width / height
        target_width = 100
        target_height = int(target_width / aspect_ratio)
        logo = logo.resize((target_width, target_height))
        self.logo = ImageTk.PhotoImage(logo)
        self.logo_label = tk.Label(self.root, image=self.logo, bg="black")
        self.logo_label.place(x=10, y=10)

    def add_kerning(self, text, spacing=0.5):
        return ''.join([char + ' ' * int(spacing) for char in text])

    def save_user_name(self):
        user_name = self.name_entry.get().strip().capitalize()
        if user_name:
            self.create_user_account(user_name, user_name)
            self.prompt_journal_name(user_name)
        else:
            self.show_error_message("Please enter a valid name.")

    def prompt_journal_name(self, user_name):
        for widget in self.root.winfo_children():
            widget.destroy()

        frame = tk.Frame(self.root, bg="black", padx=230, pady=30)
        frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        custom_font = font.Font(family="Century Gothic", size=36, weight="normal", slant="roman", underline=0, overstrike=0)
        custom_font_large = font.Font(family="Century Gothic", size=48, weight="normal", slant="roman", underline=0, overstrike=0)

        self.journal_frame = frame

        welcome_label = tk.Label(frame, text=self.add_kerning(f"Got it, {user_name}.", spacing=0.5), font=custom_font, fg="white", bg="black", wraplength=1140)
        welcome_label.pack(pady=5)

        journal_label = tk.Label(frame, text=self.add_kerning("Let's create your first journal. Do you have a name you want to give your first journal? You can change this at any time.", spacing=0.5), font=custom_font, fg="white", bg="black", wraplength=1140)
        journal_label.pack(pady=5)

        input_frame = tk.Frame(frame, bg="black")
        input_frame.pack(pady=30)

        self.scroll_orb_label = tk.Label(input_frame, image=self.scroll_orb_image, bg="black")
        self.scroll_orb_label.pack(side=tk.LEFT, padx=(0, 10))

        self.journal_entry = tk.Entry(input_frame, font=custom_font_large, fg="white", bg="black", width=20, borderwidth=0, highlightthickness=0, insertbackground="white", justify='left')
        self.journal_entry.pack(side=tk.LEFT)

        self.submit_button = tk.Label(frame, image=self.send_button_image, borderwidth=0)
        self.submit_button.pack(pady=5)
        self.submit_button.bind('<Button-1>', lambda event: self.save_journal_name())
        self.root.bind('<Return>', lambda event: self.save_journal_name())

    def save_journal_name(self):
        journal_name = self.journal_entry.get().strip()
        if journal_name:
            if 'Journal' not in self.config:
                self.config['Journal'] = {}
            self.config['Journal']['Name'] = journal_name
            with open('config.ini', 'w') as configfile:
                self.config.write(configfile)
            self.create_journal_file()
            self.show_success_message(f"Your first journal '{journal_name}' has been created!")
            self.run_journal(journal_name)
        else:
            self.show_error_message("Please enter a valid journal name.")


    def create_journal_file(self):
        if not os.path.exists('Journals'):
            os.makedirs('Journals')
        if not os.path.exists('founders'):
            os.makedirs('founders')

        with open('Julia_livegen.py', 'r') as template_file:
            template_content = template_file.read()

        user_name = self.config['User']['Name']
        journal_title = self.config['Journal']['Name'].strip() if self.config['Journal']['Name'].strip() else "Julia AI"
        # Replace the journal title in the content
        new_content = template_content.replace('JOURNAL_TITLE', journal_title)

        # Create assets directory for the journal
        journal_assets_dir = os.path.join('Journals', journal_title, 'assets')
        os.makedirs(journal_assets_dir, exist_ok=True)

        # Copy the scroll_orb.png and send.png files to the journal's assets directory
        shutil.copy('admin/assets/scroll_orb.png', journal_assets_dir)
        shutil.copy('admin/assets/send.png', journal_assets_dir)

        # Write new file in Journals directory
        journal_file_path = os.path.join('Journals', journal_title, f'{journal_title}.py')
        with open(journal_file_path, 'w') as new_journal_file:
            new_journal_file.write(new_content)

        # Write new file in the root directory
        root_journal_file_path = os.path.join(f'{journal_title}.py')
        with open(root_journal_file_path, 'w') as root_journal_file:
            root_journal_file.write(new_content)


    def show_success_message(self, message):
        for widget in self.journal_frame.winfo_children():
            widget.destroy()

        success_label = tk.Label(self.journal_frame, text=message, font=("Century Gothic", 36), fg="green", bg="black", wraplength=1140)
        success_label.pack(pady=5)

        self.submit_button.pack_forget()
        self.scroll_orb_label.pack_forget()
        self.root.after(8000, lambda: self.run_journal(self.config['Journal']['Name']))

    def run_journal(self, journal_name):
        self.root.destroy()
        journal_file_path = os.path.join(f'{journal_name}.py')
        subprocess.Popen(["python", journal_file_path])

    def show_error_message(self, message):
        error_label = tk.Label(self.root, text=message, font=("Century Gothic", 36), fg="red", bg="black")
        error_label.pack(pady=5)


    def generate_key(self):
        return Fernet.generate_key()

    def load_key(self):
        if os.path.exists('config.ini'):
            self.config.read('config.ini')
            if 'Encryption' in self.config and 'Key' in self.config['Encryption']:
                key = self.config['Encryption']['Key']
                self.key = key.encode()
            else:
                self.generate_and_save_key()
        else:
            self.generate_and_save_key()

    def generate_and_save_key(self):
        self.key = self.generate_key()
        if 'Encryption' not in self.config:
            self.config['Encryption'] = {}
        self.config['Encryption']['Key'] = self.key.decode()
        with open('config.ini', 'w') as configfile:
            self.config.write(configfile)

    def ts_to_gen(self, ts):
        gen = math.pow(1.0002, (ts - 1675084800) / 3300)
        return round(gen, 16)

    def create_user_account(self, name, handle):
        timestamp = int(time.time())
        user_gen = self.ts_to_gen(timestamp)

        user_data = {
            "name": name,
            "handle": handle,
            "registration_date": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(timestamp)),
            "gen_number": user_gen
        }

        folder_name = handle.lower()
        folder_path = os.path.join("accounts", folder_name)
        os.makedirs(folder_path, exist_ok=True)

        file_name = f"{user_gen:.16f}_{handle.lower()}.json"
        file_path = os.path.join(folder_path, file_name)
        with open(file_path, "w") as file:
            json.dump(user_data, file, indent=4)

        self.config['User'] = {"Name": name, "Handle": handle}
        with open('config.ini', 'w') as configfile:
            self.config.write(configfile)

    def run_journal(self, journal_name):
        self.root.after(8000, self._close_and_run_journal, journal_name)

    def _close_and_run_journal(self, journal_name):
        self.root.destroy()
        journal_file_path = os.path.join(f'{journal_name}.py')
        subprocess.Popen(["python", journal_file_path])

if __name__ == "__main__":
    root = tk.Tk()
    setup_julia = ORBSetup(root)
    root.mainloop()