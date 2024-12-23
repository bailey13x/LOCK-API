import tkinter as tk
from tkinter import messagebox


def validate_and_save_key_gui():
    def submit_key():
        key = key_entry.get()
        if validate_key_local(key, "LOCK"):
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


# Example usage
if __name__ == "__main__":
    validate_and_save_key_gui()
