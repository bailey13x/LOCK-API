# lock/gui.py

import tkinter as tk
from tkinter import messagebox
from .key_manager import validate_key_local, save_key_encrypted, load_key_decrypted

def validate_and_save_key_gui(app_id: str = "LOCK"):
    """Show a GUI for validating and saving a product key."""
    def submit_key():
        key = key_entry.get()
        if validate_key_local(key, app_id):
            save_key_encrypted(key)
            messagebox.showinfo("Success", "Product key saved successfully!")
            root.destroy()
        else:
            messagebox.showerror("Error", "Invalid product key.")

    root = tk.Tk()
    root.title("Enter Product Key")
    tk.Label(root, text="Enter Product Key:").pack(pady=5)
    key_entry = tk.Entry(root, width=30)
    key_entry.pack(pady=5)
    tk.Button(root, text="Submit", command=submit_key).pack(pady=10)
    root.mainloop()
