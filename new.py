import tkinter as tk
from tkinter import ttk, messagebox
import random
import string

class PasswordGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Password Generator")
        self.root.geometry("400x450")
        
        # Variables
        self.length_var = tk.IntVar(value=12)
        self.password_var = tk.StringVar()
        self.upper_var = tk.BooleanVar(value=True)
        self.lower_var = tk.BooleanVar(value=True)
        self.digits_var = tk.BooleanVar(value=True)
        self.symbols_var = tk.BooleanVar(value=True)
        
        # Create UI
        self.create_widgets()
    
    def create_widgets(self):
        # Main container
        mainframe = ttk.Frame(self.root, padding="10")
        mainframe.pack(fill=tk.BOTH, expand=True)
        
        # Length control
        ttk.Label(mainframe, text="Password Length:").grid(row=0, column=0, sticky=tk.W)
        ttk.Scale(
            mainframe, 
            from_=6, 
            to=32, 
            orient=tk.HORIZONTAL,
            variable=self.length_var,
            command=lambda x: self.length_var.set(round(float(x)))
        ).grid(row=0, column=1, sticky=tk.EW)
        ttk.Label(mainframe, textvariable=self.length_var).grid(row=0, column=2, padx=5)
        
        # Character types
        ttk.Label(mainframe, text="Include:").grid(row=1, column=0, sticky=tk.W, pady=(10,0))
        ttk.Checkbutton(mainframe, text="Uppercase (A-Z)", variable=self.upper_var).grid(row=2, column=0, columnspan=3, sticky=tk.W)
        ttk.Checkbutton(mainframe, text="Lowercase (a-z)", variable=self.lower_var).grid(row=3, column=0, columnspan=3, sticky=tk.W)
        ttk.Checkbutton(mainframe, text="Digits (0-9)", variable=self.digits_var).grid(row=4, column=0, columnspan=3, sticky=tk.W)
        ttk.Checkbutton(mainframe, text="Symbols (!@#$)", variable=self.symbols_var).grid(row=5, column=0, columnspan=3, sticky=tk.W)
        
        # Generate button
        ttk.Button(mainframe, text="Generate Password", command=self.generate_password).grid(row=6, column=0, columnspan=3, pady=15)
        
        # Password display
        ttk.Entry(mainframe, textvariable=self.password_var, font=('Courier', 12), state='readonly').grid(row=7, column=0, columnspan=3, sticky=tk.EW)
        
        # Copy button (simplified without pyperclip)
        ttk.Button(mainframe, text="Copy", command=self.copy_password).grid(row=8, column=0, columnspan=3)
        
        # Strength indicator
        self.strength_var = tk.StringVar(value="")
        ttk.Label(mainframe, textvariable=self.strength_var).grid(row=9, column=0, columnspan=3)
    
    def generate_password(self):
        if not any([self.upper_var.get(), self.lower_var.get(), self.digits_var.get(), self.symbols_var.get()]):
            messagebox.showerror("Error", "Please select at least one character type!")
            return
        
        chars = []
        if self.upper_var.get(): chars.extend(list(string.ascii_uppercase))
        if self.lower_var.get(): chars.extend(list(string.ascii_lowercase))
        if self.digits_var.get(): chars.extend(list(string.digits))
        if self.symbols_var.get(): chars.extend(list("!@#$%^&*"))
        
        length = self.length_var.get()
        password = ''.join(random.choices(chars, k=length))
        self.password_var.set(password)
        self.assess_strength(password)
    
    def assess_strength(self, password):
        length = len(password)
        complexity = sum([
            1 if any(c in string.ascii_uppercase for c in password) else 0,
            1 if any(c in string.ascii_lowercase for c in password) else 0,
            1 if any(c in string.digits for c in password) else 0,
            1 if any(c in "!@#$%^&*" for c in password) else 0
        ])
        
        strength = min(100, (length * 3) + (complexity * 10))
        
        if strength < 40:
            self.strength_var.set("Strength: Weak")
        elif strength < 70:
            self.strength_var.set("Strength: Medium")
        else:
            self.strength_var.set("Strength: Strong")
    
    def copy_password(self):
        if self.password_var.get():
            self.root.clipboard_clear()
            self.root.clipboard_append(self.password_var.get())
            messagebox.showinfo("Copied", "Password copied to clipboard!")
        else:
            messagebox.showwarning("Error", "No password to copy")

if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordGeneratorApp(root)
    root.mainloop()
