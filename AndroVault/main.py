# main.py
import tkinter as tk
from auth.authentication import authenticate
from ui.main_window import MainWindow
from manager.account_manager import AccountManager
from logger import log_event, log_error
import sys
import traceback

def main():
    try:
        root = tk.Tk()
        root.withdraw()  # Hide root during authentication
        
        # Set basic window properties
        root.title("Password Manager")
        root.geometry("800x600")
        
        log_event("Application started")
        
        try:
            master_password = authenticate(root)
            if master_password:
                # Initialize account manager with decrypted data
                account_manager = AccountManager(master_password)
                
                # Show main window
                root.deiconify()
                root.update()  # Force window update
                
                # Launch main UI
                app = MainWindow(root, account_manager)
                root.mainloop()
            else:
                log_event("Authentication failed or cancelled")
                root.destroy()
        except Exception as auth_error:
            log_error(f"Authentication error: {str(auth_error)}")
            traceback.print_exc()
            root.destroy()
            
    except Exception as e:
        log_error(f"Critical application error: {str(e)}")
        traceback.print_exc()
        sys.exit(1)

    # Check if account_store is properly initialized
    print("Debug: account_store initialization")

if __name__ == "__main__":
    main()
