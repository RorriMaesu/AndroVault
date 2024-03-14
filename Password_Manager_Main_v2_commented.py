from tkinter import *  # Import all classes and functions from the tkinter module for creating the GUI
from random import choice, randint, shuffle  # Import specific functions from the random module for generating random passwords
from tkinter import messagebox  # Import the messagebox module from tkinter for displaying message boxes
import pyperclip  # Import the pyperclip module for copying generated passwords to the clipboard
import json  # Import the json module for loading and saving password data to a JSON file
import re  # Import the re module for email validation using regular expressions
import datetime  # Import the datetime module for handling password expiration dates

# Define constants for colors and font settings used in the GUI
BG_COLOR = "#1F1F1F"  # Background color of the window
FIELD_COLOR = "#2B2B2B"  # Background color of input fields
BUTTON_COLOR = "#4CAF50"  # Background color of buttons
TEXT_COLOR = "#FFFFFF"  # Text color
FONT_NAME = "Arial"  # Font name
FONT_SIZE = 12  # Font size

# -----------------------------Search Function--------------------------------------
def find_password():
    website = website_input.get().title()  # Get the website name from the input field and convert it to title case

    try:
        with open("data.json", "r") as file:  # Open the data.json file in read mode
            data = json.load(file)  # Load the JSON data from the file into the 'data' variable
        if website in data:  # Check if the entered website exists in the loaded data
            email = data[website]['email']  # Retrieve the email associated with the website
            password = data[website]['password']  # Retrieve the password associated with the website
            pyperclip.copy(password)  # Copy the password to the clipboard
            messagebox.showinfo(title=website, message=f"{website}\nEmail: {email}\nPassword: {password}")  # Display the website, email, and password in a message box
        elif not website:  # Check if the website input field is empty
            messagebox.showinfo(title="Oops!", message="Please enter a website.")  # Display a message to enter a website if the field is empty
        else:  # If the website is not found in the loaded data
            messagebox.showinfo(title="Oops!", message=f"No information found for {website}.")  # Display a message indicating that no information was found for the entered website
    except FileNotFoundError:  # If the data.json file is not found
        messagebox.showinfo(title="Oops!", message="No data file found.")  # Display a message indicating that no data file was found
    except json.JSONDecodeError:  # If there is an error decoding the JSON data
        messagebox.showerror(title="Error", message="Invalid JSON data in the file.")  # Display an error message indicating invalid JSON data in the file

# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    password_input.delete(0, END)  # Clear the password input field
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']  # List of letters for generating passwords
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']  # List of numbers for generating passwords
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']  # List of symbols for generating passwords

    password_letters = [choice(letters) for _ in range(randint(8, 10))]  # Randomly select 8 to 10 letters from the letters list
    password_symbols = [choice(symbols) for _ in range(randint(2, 4))]  # Randomly select 2 to 4 symbols from the symbols list
    password_numbers = [choice(numbers) for _ in range(randint(2, 4))]  # Randomly select 2 to 4 numbers from the numbers list

    password_list = password_letters + password_symbols + password_numbers  # Combine the selected letters, symbols, and numbers into a single list
    shuffle(password_list)  # Shuffle the password list to randomize the order of characters

    password = "".join(password_list)  # Join the characters in the password list to form a string
    pyperclip.copy(password)  # Copy the generated password to the clipboard
    password_input.insert(0, password)  # Insert the generated password into the password input field
    check_password_strength(password)  # Check the strength of the generated password

# ---------------------------- PASSWORD STRENGTH INDICATOR ------------------------------- #
def check_password_strength(password):
    strength_criteria = [
        len(password) >= 8,  # Check if the password length is at least 8 characters
        bool(re.search("[a-z]", password)),  # Check if the password contains lowercase letters
        bool(re.search("[A-Z]", password)),  # Check if the password contains uppercase letters
        bool(re.search("[0-9]", password)),  # Check if the password contains numbers
        bool(re.search("[!@#$%^&*()]", password))  # Check if the password contains special characters
    ]
    strength = sum(strength_criteria)  # Calculate the password strength by summing the boolean values of the criteria

    if strength == 5:  # If the password meets all the strength criteria
        strength_label.config(text="Strong", fg="green")  # Update the strength label to display "Strong" in green color
    elif strength == 3 or strength == 4:  # If the password meets 3 or 4 strength criteria
        strength_label.config(text="Medium", fg="orange")  # Update the strength label to display "Medium" in orange color
    else:  # If the password meets less than 3 strength criteria
        strength_label.config(text="Weak", fg="red")  # Update the strength label to display "Weak" in red color

# ---------------------------- PASSWORD INPUT VALIDATION ------------------------------- #
def validate_password(event):
    password = password_input.get()  # Get the password from the password input field
    check_password_strength(password)  # Check the strength of the entered password

# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    website = website_input.get().title()  # Get the website name from the input field and convert it to title case
    password = password_input.get()  # Get the password from the password input field
    email = email_input.get()  # Get the email from the email input field
    creation_date = datetime.date.today().strftime("%Y-%m-%d")  # Get the current date in the format "YYYY-MM-DD"

    new_data = {
        website: {
            "email": email,
            "password": password,
            "creation_date": creation_date,
            "history": []
        }
    }  # Create a dictionary with the website as the key and a nested dictionary containing email, password, creation date, and an empty history list

    if not website or not password:  # If the website or password fields are empty
        messagebox.showinfo(title="Oops!", message="Please fill in all fields!")  # Display a message to fill in all fields
    elif not validate_email(email):  # If the email is not valid
        messagebox.showerror(title="Invalid Email", message="Please enter a valid email address.")  # Display an error message to enter a valid email address
    else:  # If all fields are filled and the email is valid
        try:
            with open("data.json", "r") as file:  # Open the data.json file in read mode
                data = json.load(file)  # Load the existing JSON data from the file into the 'data' variable
        except FileNotFoundError:  # If the data.json file is not found
            data = {}  # Initialize an empty dictionary for data

        if website in data:  # If the website already exists in the loaded data
            if not messagebox.askyesno(title="Confirm Override", message=f"Password for {website} already exists. Do you want to override it?"):  # Ask for confirmation to override the existing password
                return  # If the user chooses not to override, return from the function without saving
            data[website]["history"].append(data[website]["password"])  # Append the existing password to the password history list
            if len(data[website]["history"]) > 5:  # If the password history list exceeds 5 entries
                data[website]["history"].pop(0)  # Remove the oldest password from the history list
        
        data.update(new_data)  # Update the loaded data with the new website, email, and password information

        with open("data.json", "w") as file:  # Open the data.json file in write mode
            json.dump(data, file, indent=4)  # Save the updated data to the file in JSON format with indentation

        website_input.delete(0, END)  # Clear the website input field
        password_input.delete(0, END)  # Clear the password input field
        website_input.focus()  # Set the focus back to the website input field

# ---------------------------- DATA VALIDATION ------------------------------- #
def validate_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'  # Regular expression pattern for email validation
    return re.match(pattern, email)  # Check if the email matches the pattern and return True or False

# ---------------------------- PASSWORD VISIBILITY TOGGLE ------------------------------- #
def toggle_password_visibility():
    if password_input.cget('show') == '':  # If the password input field is currently showing the password
        password_input.config(show='*')  # Change the password input field to show asterisks
        toggle_button.config(text='Show')  # Change the toggle button text to 'Show'
    else:  # If the password input field is currently showing asterisks
        password_input.config(show='')  # Change the password input field to show the actual password
        toggle_button.config(text='Hide')  # Change the toggle button text to 'Hide'

# ---------------------------- PASSWORD EXPIRATION CHECK ------------------------------- #
def check_password_expiration():
    try:
        with open("data.json", "r") as file:  # Open the data.json file in read mode
            data = json.load(file)  # Load the JSON data from the file into the 'data' variable
        for website in data:  # Iterate over each website in the loaded data
            if "creation_date" in data[website]:  # If the website has a creation date
                creation_date = datetime.datetime.strptime(data[website]["creation_date"], "%Y-%m-%d").date()  # Parse the creation date string into a datetime.date object
                expiration_date = creation_date + datetime.timedelta(days=90)  # Calculate the expiration date by adding 90 days to the creation date
                if expiration_date <= datetime.date.today():  # If the expiration date is less than or equal to the current date
                    messagebox.showwarning(title="Password Expired", message=f"The password for {website} has expired. Please update it.")  # Display a warning message indicating that the password has expired
    except FileNotFoundError:  # If the data.json file is not found
        pass  # Do nothing and continue

# ---------------------------- UI SETUP ------------------------------- #
window = Tk()  # Create the main window of the application
window.title("AndroVault")  # Set the title of the window
window.config(padx=30, pady=30, bg=BG_COLOR)  # Set the padding and background color of the window

# Create a frame to hold the logo image
logo_frame = Frame(window, bg=BG_COLOR)  # Create a frame for the logo image with the same background color as the window
logo_frame.grid(column=0, row=0, columnspan=4, pady=(0, 20))  # Position the logo frame in the grid layout

# Load and display the logo image
logo_img = PhotoImage(file="logo.png")  # Load the logo image file
logo_label = Label(logo_frame, image=logo_img, bg=BG_COLOR)  # Create a label to display the logo image
logo_label.pack(pady=10)  # Position the logo label inside the logo frame with some padding

# Create labels for website, email/username, and password
website_label = Label(text="Website:", font=(FONT_NAME, FONT_SIZE), fg=TEXT_COLOR, bg=BG_COLOR)  # Create a label for the website field
website_label.grid(column=0, row=1, sticky="e", padx=(0, 10))  # Position the website label in the grid layout
email_username_label = Label(text="Email/Username:", font=(FONT_NAME, FONT_SIZE), fg=TEXT_COLOR, bg=BG_COLOR)  # Create a label for the email/username field
email_username_label.grid(column=0, row=2, sticky="e", padx=(0, 10))  # Position the email/username label in the grid layout
password_label = Label(text="Password:", font=(FONT_NAME, FONT_SIZE), fg=TEXT_COLOR, bg=BG_COLOR)  # Create a label for the password field
password_label.grid(column=0, row=3, sticky="e", padx=(0, 10))  # Position the password label in the grid layout

# Create input fields for website, email, and password
website_input = Entry(width=35, font=(FONT_NAME, FONT_SIZE), bg=FIELD_COLOR, fg=TEXT_COLOR, insertbackground=TEXT_COLOR)  # Create an input field for the website
website_input.grid(column=1, row=1, columnspan=2, padx=(0, 10), pady=(0, 10), sticky="w")  # Position the website input field in the grid layout
website_input.focus()  # Set the focus to the website input field

email_input = Entry(width=35, font=(FONT_NAME, FONT_SIZE), bg=FIELD_COLOR, fg=TEXT_COLOR, insertbackground=TEXT_COLOR)  # Create an input field for the email
email_input.grid(column=1, row=2, columnspan=2, padx=(0, 10), pady=(0, 10), sticky="w")  # Position the email input field in the grid layout
email_input.insert(0, "youremail@youremailprovider.com")  # Insert a default email address into the email input field

password_input = Entry(width=35, font=(FONT_NAME, FONT_SIZE), bg=FIELD_COLOR, fg=TEXT_COLOR, insertbackground=TEXT_COLOR, show='*')  # Create an input field for the password with the characters masked
password_input.grid(column=1, row=3, columnspan=2, padx=(0, 10), pady=(0, 10), sticky="w")  # Position the password input field in the grid layout
password_input.bind('<KeyRelease>', validate_password)  # Bind the 'validate_password' function to the 'KeyRelease' event of the password input field

# Create a frame for the password strength indicator
strength_frame = Frame(window, bg=BG_COLOR)  # Create a frame for the password strength indicator with the same background color as the window
strength_frame.grid(column=1, row=4, columnspan=2, sticky="w")  # Position the strength frame in the grid layout
strength_label = Label(strength_frame, text="Strength:", font=(FONT_NAME, FONT_SIZE), fg=TEXT_COLOR, bg=BG_COLOR)  # Create a label for the strength indicator
strength_label.pack(side="left")  # Position the strength label inside the strength frame on the left side
strength_bar = Canvas(strength_frame, width=200, height=20, bg=FIELD_COLOR, highlightthickness=0)  # Create a canvas for the strength bar
strength_bar.pack(side="left", padx=(10, 0))  # Position the strength bar inside the strength frame on the left side with some padding

# Create buttons for generating password, adding data, searching, and toggling password visibility
generate_password_button = Button(text="Generate Password", command=generate_password, font=(FONT_NAME, FONT_SIZE), bg=BUTTON_COLOR, fg=TEXT_COLOR, activebackground=BUTTON_COLOR, activeforeground=TEXT_COLOR, relief="flat", padx=10, pady=5)  # Create a button for generating passwords
generate_password_button.grid(column=3, row=3, padx=(10, 0), pady=(0, 10), sticky="w")  # Position the generate password button in the grid layout

add_button = Button(text="Add", width=35, command=save, font=(FONT_NAME, FONT_SIZE), bg=BUTTON_COLOR, fg=TEXT_COLOR, activebackground=BUTTON_COLOR, activeforeground=TEXT_COLOR, relief="flat", padx=10, pady=5)  # Create a button for adding data
add_button.grid(column=1, row=5, columnspan=2, padx=(0, 10), pady=(0, 10), sticky="w")  # Position the add button in the grid layout

search_button = Button(text="Search", width=14, command=find_password, font=(FONT_NAME, FONT_SIZE), bg=BUTTON_COLOR, fg=TEXT_COLOR, activebackground=BUTTON_COLOR, activeforeground=TEXT_COLOR, relief="flat", padx=10, pady=5)  # Create a button for searching passwords
search_button.grid(column=3, row=1, padx=(10, 0), pady=(0, 10), sticky="w")  # Position the search button in the grid layout

toggle_button = Button(text='Show', width=14, command=toggle_password_visibility, font=(FONT_NAME, FONT_SIZE), bg=BUTTON_COLOR, fg=TEXT_COLOR, activebackground=BUTTON_COLOR, activeforeground=TEXT_COLOR, relief="flat", padx=10, pady=5)  # Create a button for toggling password visibility
toggle_button.grid(column=3, row=2, padx=(10, 0), pady=(0, 10), sticky="w")  # Position the toggle button in the grid layout

check_password_expiration()  # Call the function to check for expired passwords

#Bind keyboard shortcuts to functions
window.bind('<Control-g>', lambda event: generate_password())  # Bind the 'generate_password' function to the 'Ctrl+G' keyboard shortcut
window.bind('<Control-s>', lambda event: save())  # Bind the 'save' function to the 'Ctrl+S' keyboard shortcut
window.bind('<Control-f>', lambda event: find_password())  # Bind the 'find_password' function to the 'Ctrl+F' keyboard shortcut

window.mainloop()  # Start the main event loop of the application