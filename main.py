import tkinter as tk
from tkinter import ttk, messagebox
import re
import random
import string
import hashlib
import urllib.request
import math

# --- Logic Functions ---

def calculate_time_to_crack(password):
    if not password:
        return "N/A"
    
    pool_size = 0
    if re.search(r"[a-z]", password): pool_size += 26
    if re.search(r"[A-Z]", password): pool_size += 26
    if re.search(r"\d", password): pool_size += 10
    if re.search(r"[!@#$%^&*(),.?\":{}|<>]", password): pool_size += 32
    
    if pool_size == 0:
        return "Instantly"
    
    combinations = pool_size ** len(password)
    # Assuming 10 billion guesses per second (modern GPU)
    seconds = combinations / 10_000_000_000
    
    if seconds < 1:
        return "Instantly"
    elif seconds < 60:
        return f"{int(seconds)} seconds"
    elif seconds < 3600:
        return f"{int(seconds // 60)} minutes"
    elif seconds < 86400:
        return f"{int(seconds // 3600)} hours"
    elif seconds < 31536000:
        return f"{int(seconds // 86400)} days"
    elif seconds < 3153600000:
        return f"{int(seconds // 31536000)} years"
    else:
        return "Centuries 🛡️"

def check_pwned_password(password):
    if not password:
        return 0
    sha1_password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    prefix, suffix = sha1_password[:5], sha1_password[5:]
    
    url = f"https://api.pwnedpasswords.com/range/{prefix}"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Python-Password-Checker'})
        with urllib.request.urlopen(req, timeout=5) as response:
            hashes = response.read().decode('utf-8').splitlines()
            for line in hashes:
                h, count = line.split(':')
                if h == suffix:
                    return int(count)
    except Exception:
        return -1
    return 0

def check_password_strength(password):
    length_error = len(password) < 8
    digit_error = re.search(r"\d", password) is None
    uppercase_error = re.search(r"[A-Z]", password) is None
    lowercase_error = re.search(r"[a-z]", password) is None
    symbol_error = re.search(r"[!@#$%^&*(),.?\":{}|<>]", password) is None
    
    errors = [length_error, digit_error, uppercase_error, lowercase_error, symbol_error]
    failed_criteria = sum(errors)
    
    if len(password) == 0:
        return 0, "Please enter a password!", "#888888"
    elif failed_criteria == 0:
        return 100, "Strong Password! 💪", "#00FF66"
    elif failed_criteria <= 2:
        return 60, "Medium Strength ⚠️", "#FFBB00"
    else:
        return 25, "Weak Password! ❌", "#FF3333"

def evaluate_password(event=None):
    password = entry.get()
    score, feedback, color = check_password_strength(password)
    
    progress_bar['value'] = score
    result_label.config(text=feedback, fg=color)
    
    crack_time = calculate_time_to_crack(password)
    crack_label.config(text=f"Estimated Time to Crack: {crack_time}")
    pwned_label.config(text="")

def check_breach():
    password = entry.get()
    if not password:
        messagebox.showwarning("Warning", "Please enter a password first!")
        return
    
    pwned_label.config(text="Checking API...", fg="#AAAAAA")
    root.update_idletasks()
    
    count = check_pwned_password(password)
    if count > 0:
        pwned_label.config(text=f"🚨 Seen {count} times in data breaches!", fg="#FF3333")
    elif count == 0:
        pwned_label.config(text="✅ Not found in known breaches.", fg="#00FF66")
    else:
        pwned_label.config(text="⚠️ Network error checking API.", fg="#888888")

def generate_strong_password():
    length = length_slider.get()
    
    char_pool = ""
    if use_letters.get(): char_pool += string.ascii_letters
    if use_numbers.get(): char_pool += string.digits
    if use_symbols.get(): char_pool += "!@#$%^&*()"
    
    if not char_pool:
        messagebox.showwarning("Warning", "Select at least one character type!")
        return
        
    strong_pwd = ''.join(random.choice(char_pool) for _ in range(length))
    entry.delete(0, tk.END)
    entry.insert(0, strong_pwd)
    evaluate_password()

def copy_to_clipboard():
    password = entry.get()
    if password:
        root.clipboard_clear()
        root.clipboard_append(password)
        messagebox.showinfo("Success", "Password copied to clipboard! 📋")
    else:
        messagebox.showwarning("Warning", "No password to copy!")

def toggle_password_visibility():
    entry.config(show="" if show_pass_var.get() else "*")

def save_password_to_file():
    password = entry.get()
    if not password:
        messagebox.showwarning("Warning", "No password to save!")
        return
    with open("saved_passwords.txt", "a") as f:
        f.write(f"{password}\n")
    messagebox.showinfo("Saved", "Password saved to saved_passwords.txt! 💾")

# --- UI Setup (Dark Theme) ---

root = tk.Tk()
root.title("Password Security Suite Pro")
root.geometry("500x540")  # Correct
root.configure(bg="#1E1E1E")
root.resizable(False, False)

# Main Title
title_label = tk.Label(root, text="Password Strength Checker", font=("Segoe UI", 14, "bold"), bg="#1E1E1E", fg="#FFFFFF")
title_label.pack(pady=(15, 5))

# Input Field
entry = tk.Entry(root, show="*", font=("Consolas", 12), width=30, bg="#2D2D2D", fg="#FFFFFF", insertbackground="white", bd=0, relief="flat")
entry.pack(pady=8, ipady=6)
entry.bind("<KeyRelease>", evaluate_password)

# Show Password Checkbox
show_pass_var = tk.BooleanVar()
show_pass_check = tk.Checkbutton(root, text="Show Password", variable=show_pass_var, command=toggle_password_visibility, bg="#1E1E1E", fg="#AAAAAA", selectcolor="#2D2D2D", activebackground="#1E1E1E", activeforeground="#FFFFFF")
show_pass_check.pack()

# Progress Bar
progress_bar = ttk.Progressbar(root, length=340, mode='determinate')
progress_bar.pack(pady=12)

# Feedback Labels
result_label = tk.Label(root, text="Please enter a password!", font=("Segoe UI", 10, "bold"), bg="#1E1E1E", fg="#888888")
result_label.pack()

crack_label = tk.Label(root, text="Estimated Time to Crack: N/A", font=("Segoe UI", 9), bg="#1E1E1E", fg="#CCCCCC")
crack_label.pack(pady=4)

pwned_label = tk.Label(root, text="", font=("Segoe UI", 9, "bold"), bg="#1E1E1E", fg="#888888")
pwned_label.pack()

# --- Customization Options Frame ---
options_frame = tk.LabelFrame(root, text=" Generation Options ", font=("Segoe UI", 9), bg="#1E1E1E", fg="#888888", bd=1, relief="solid")
options_frame.pack(pady=10, padx=20, fill="x")

# Slider
length_label = tk.Label(options_frame, text="Length: 16", font=("Segoe UI", 9), bg="#1E1E1E", fg="#FFFFFF")
length_label.pack(anchor="w", padx=10, pady=(5, 0))

def update_slider_label(val):
    length_label.config(text=f"Length: {int(float(val))}")

length_slider = tk.Scale(options_frame, from_=8, to=32, orient="horizontal", bg="#1E1E1E", fg="#FFFFFF", highlightthickness=0, command=update_slider_label)
length_slider.set(16)
length_slider.pack(fill="x", padx=10, pady=2)

# Checkboxes
use_letters = tk.BooleanVar(value=True)
use_numbers = tk.BooleanVar(value=True)
use_symbols = tk.BooleanVar(value=True)

chk_frame = tk.Frame(options_frame, bg="#1E1E1E")
chk_frame.pack(pady=5)

tk.Checkbutton(chk_frame, text="A-z", variable=use_letters, bg="#1E1E1E", fg="#FFFFFF", selectcolor="#2D2D2D", activebackground="#1E1E1E", activeforeground="#FFFFFF").pack(side="left", padx=5)
tk.Checkbutton(chk_frame, text="0-9", variable=use_numbers, bg="#1E1E1E", fg="#FFFFFF", selectcolor="#2D2D2D", activebackground="#1E1E1E", activeforeground="#FFFFFF").pack(side="left", padx=5)
tk.Checkbutton(chk_frame, text="!@#", variable=use_symbols, bg="#1E1E1E", fg="#FFFFFF", selectcolor="#2D2D2D", activebackground="#1E1E1E", activeforeground="#FFFFFF").pack(side="left", padx=5)

# --- Control Buttons ---
btn_frame = tk.Frame(root, bg="#1E1E1E")
btn_frame.pack(pady=10)

btn_style = {"font": ("Segoe UI", 9, "bold"), "bg": "#007ACC", "fg": "#FFFFFF", "bd": 0, "padx": 10, "pady": 5, "activebackground": "#005999", "activeforeground": "#FFFFFF"}

tk.Button(btn_frame, text="🔑 Generate", command=generate_strong_password, **btn_style).grid(row=0, column=0, padx=4)
tk.Button(btn_frame, text="📋 Copy", command=copy_to_clipboard, **btn_style).grid(row=0, column=1, padx=4)
tk.Button(btn_frame, text="🔍 Check Breach", command=check_breach, **btn_style).grid(row=0, column=2, padx=4)
tk.Button(btn_frame, text="💾 Save", command=save_password_to_file, **btn_style).grid(row=0, column=3, padx=4)

root.mainloop()