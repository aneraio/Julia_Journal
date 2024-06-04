# ORB Setup

The ORB Setup is a Python application that assists in setting up user profiles and creating personalized journals. The application provides an interactive GUI for users to enter their information and generate journal files with customized titles. It also includes features like cloning the setup file for future use.

## Features

- Interactive GUI for user profile setup
- Customizable journal creation
- Cloning of the setup file for future use
- Encrypted storage of user data
- Automated creation of necessary directories and files

## Requirements

- Python 3.11
- Tkinter
- Pillow
- cryptography
- configparser

## Installation

1. **Clone the repository or download the source code.**

2. **Install the required Python packages:**

    ```sh
    pip install pillow cryptography
    ```

3. **Ensure the following directory structure exists:**

    ```
    .
    ├── admin
    │   ├── assets
    │   │   ├── scroll_orb.png
    │   │   ├── send.png
    │   └── logos
    │       └── logo.png
    ├── Julia_livegen.py
    └── ORBsetup.py
    ```

4. **Install Tcl/Tk:**

    Ensure Tcl/Tk is installed and the environment variables are set correctly:

    ```sh
    brew reinstall tcl-tk
    ```

    Add the following lines to your shell configuration file (`.zshrc` for zsh or `.bashrc` for bash):

    ```sh
    export PATH="/opt/homebrew/opt/tcl-tk/bin:$PATH"
    export LDFLAGS="-L/opt/homebrew/opt/tcl-tk/lib"
    export CPPFLAGS="-I/opt/homebrew/opt/tcl-tk/include"
    export PKG_CONFIG_PATH="/opt/homebrew/opt/tcl-tk/lib/pkgconfig"
    ```

    Reload your shell configuration:

    ```sh
    source ~/.zshrc  # For zsh
    # or
    source ~/.bashrc  # For bash
    ```

5. **Create and activate a virtual environment:**

    ```sh
    python3.11 -m venv /path/to/your/venv
    source /path/to/your/venv/bin/activate
    ```

6. **Install required packages in the virtual environment:**

    ```sh
    pip install pillow cryptography
    ```

## Usage

1. **Run the `ORBsetup.py` script:**

    ```sh
    python ORBsetup.py
    ```

2. **Follow the on-screen instructions to set up your profile and create your first journal.**

3. **After creating your journal, a `Journal_Creator.py` file will be generated in the root directory for future use.**

## Code Explanation

### ORBSetup Class

- **Initialization (`__init__`)**: Initializes the setup, loads the key, and sets up the UI.
- **UI Setup (`setup_ui`)**: Sets up the GUI elements for the application.
- **Load Logo (`load_logo`)**: Loads the logo image.
- **Add Kerning (`add_kerning`)**: Adds spacing between characters in a string.
- **Save User Name (`save_user_name`)**: Saves the user's name and prompts for journal creation.
- **Prompt Journal Name (`prompt_journal_name`)**: Prompts the user to enter a journal name.
- **Save Journal Name (`save_journal_name`)**: Saves the journal name, creates the journal file, and shows a success message.
- **Create Journal File (`create_journal_file`)**: Creates the journal file with the specified or default title.
- **Show Success Message (`show_success_message`)**: Displays a success message and closes the application after a delay.
- **Close and Run Journal (`close_and_run_journal`)**: Closes the setup and runs the created journal file.
- **Show Error Message (`show_error_message`)**: Displays an error message.
- **Generate Key (`generate_key`)**: Generates an encryption key.
- **Load Key (`load_key`)**: Loads the encryption key from the configuration file.
- **Generate and Save Key (`generate_and_save_key`)**: Generates and saves the encryption key.
- **Timestamp to Gen (`ts_to_gen`)**: Converts a timestamp to a unique identifier.
- **Create User Account (`create_user_account`)**: Creates a user account and saves the user data.
- **Clone Setup File (`clone_setup_file`)**: Clones the current setup file to `Journal_Creator.py`.

### Example Usage

Here's an example of how you can use the `ORBsetup.py` script to set up your profile and create a journal:

1. Run the script:

    ```sh
    python ORBsetup.py
    ```

2. Enter your name when prompted.
3. Enter the name for your first journal. If you don't provide a name, it defaults to "Julia AI".
4. The script will create the necessary directories and files, and display a success message.
5. The setup file will be cloned to `Journal_Creator.py` in the root directory.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.